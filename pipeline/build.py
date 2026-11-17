"""Build one Case Closed Files episode.

usage: python3 pipeline/build.py episodes/<id> [stage] [--only a,b] [--at 0.3,0.7]
stages: tts | plan | stills | render | audio | final | thumbs | qa | all (default)
An episode folder holds: script.py (LONG, SHORTS, PHONEME_FIX), scenes.py (SCENES,
HITS, SHORT_HITS, SHORT_VIEW, WARM, thumbnail(), THUMB_WORDS), meta.json, description.txt.
SHORTS = {"a": [(sid, lines), ...], "b": ..., "c": ...}: every short 60-90 s. lines=None reuses
the LONG lines of that scene verbatim; long scenes are shown through shorts.vframe.
--names long,short_a limits render/audio/final/qa to those cuts (old single SHORT still works).
Outputs go to <episode>/work (scratch, not committed) and media/<id>/ (committed).
"""
import sys, os, re, json, glob, importlib.util, subprocess, shutil
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import config as C

EP = os.path.abspath(sys.argv[1]); EID = os.path.basename(EP)
ROOT = os.path.dirname(os.path.dirname(EP)); MEDIA = os.path.join(ROOT, "media", EID)
WORK = os.path.join(EP, "work"); AUD = os.path.join(WORK, "audio")
sys.path.insert(0, EP)
def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(EP, name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
S = load("script")
def arg(flag):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else None
def sh(cmd): subprocess.run(cmd, shell=True, check=True)
LONG_D = dict(S.LONG)
def cuts():
    """name -> list of (sid, lines) for every video this episode makes"""
    out = {"long": S.LONG}
    if hasattr(S, "SHORTS"):
        for k, seq in S.SHORTS.items(): out[f"short_{k}"] = [(sid, LONG_D[sid] if ls is None else ls) for sid, ls in seq]
    else: out["short"] = S.SHORT
    return out
CUTS = cuts()
def names():
    n = arg("--names"); return [x for x in CUTS if not n or x in n.split(",")]
def is_short(name): return name != "long"

# ---------------------------------------------------------------- narration
def tts():
    import numpy as np, soundfile as sf
    from kokoro_onnx import Kokoro
    k = Kokoro(f"{C.KOKORO_DIR}/kokoro.onnx", f"{C.KOKORO_DIR}/voices.bin")
    fix = getattr(S, "PHONEME_FIX", [])
    os.makedirs(AUD, exist_ok=True); meta = {}
    cache = json.load(open(f"{AUD}/meta.json")) if os.path.exists(f"{AUD}/meta.json") else {}
    bytext = {v["text"]: k_ for k_, v in cache.items()}
    for name, seq in CUTS.items():
        for sid, lines in seq:
            for i, l in enumerate(lines):
                t = l[0] if isinstance(l, tuple) else l
                if not t: continue
                key = f"{name}_{sid}_{i}"; fn = f"{AUD}/{key}.wav"
                if key in cache and cache[key]["text"] == t and os.path.exists(fn):
                    meta[key] = cache[key]; continue
                if t in bytext and os.path.exists(f"{AUD}/{bytext[t]}.wav"):   # same line already spoken in another cut
                    shutil.copy(f"{AUD}/{bytext[t]}.wav", fn); meta[key] = dict(cache[bytext[t]]); continue
                outs = []
                for sent in re.split(r'(?<=[.?!:])\s+', t):
                    if not sent.strip(): continue
                    ph = k.tokenizer.phonemize(sent, "en-us")
                    for a, b in fix: ph = ph.replace(a, b)
                    s, sr = k.create(ph, voice=C.VOICE, speed=C.SPEED, is_phonemes=True)
                    idx = np.where(np.abs(s) > 0.004)[0]
                    if len(idx): s = s[max(0, idx[0] - 600):idx[-1] + 2400]
                    outs += [s, np.zeros(int(sr * C.SENT_PAUSE), np.float32)]
                w = np.concatenate(outs[:-1]); sf.write(fn, w, sr)
                meta[key] = {"text": t, "dur": len(w) / sr}; print("tts", key, round(len(w) / sr, 2), flush=True)
    json.dump(meta, open(f"{AUD}/meta.json", "w"), indent=1)
    words = sum(len(v["text"].split()) for k_, v in meta.items() if k_.startswith("long"))
    secs = sum(v["dur"] for k_, v in meta.items() if k_.startswith("long"))
    print(f"narration {words} words, {secs:.0f}s, {words / secs * 60:.0f} wpm")

# ---------------------------------------------------------------- timeline
def plan(name):
    from engine import FPS
    meta = json.load(open(f"{AUD}/meta.json"))
    seq = CUTS[name]
    pad = C.LONG_PAD if name == "long" else C.SHORT_PAD; out = []; T = 0
    for sid, lines in seq:
        if sid in C.FIXED and not any((l[0] if isinstance(l, tuple) else l) for l in lines):
            out.append(dict(sid=sid, dur=C.FIXED[sid], cues=[0], start=T, lines=[])); T += C.FIXED[sid]; continue
        t = pad["lead"]; cues = []; ls = []
        for i, l in enumerate(lines):
            d = meta[f"{name}_{sid}_{i}"]["dur"]; cues.append(t)
            ls.append(dict(key=f"{name}_{sid}_{i}", at=T + t, dur=d, cap=(l[1] if isinstance(l, tuple) else None), rel=t)); t += d + pad["gap"]
        dur = round((t - pad["gap"] + pad["tail"]) * FPS) / FPS
        out.append(dict(sid=sid, dur=dur, cues=cues, start=T, lines=ls)); T += dur
    return out, T

def caps_for(sc):
    from engine import wrap
    caps = []
    for l in sc["lines"]:
        from shorts import auto_chunks, years
        if l["cap"]: parts = l["cap"].split("|")
        else: parts = auto_chunks(years(json.load(open(f"{AUD}/meta.json"))[l["key"]]["text"]))
        tot = sum(len(p) for p in parts); t = l["rel"]
        for j, p in enumerate(parts):
            dd = l["dur"] * len(p) / tot; caps.append((t, t + dd + (.25 if j == len(parts) - 1 else 0), wrap(p, "sansb", 54, 960))); t += dd
    return caps

def _job(a):
    name, sc, still, hdr = a
    from engine import render_scene, seg
    sc_mod = load("scenes"); W, H = (1920, 1080) if name == "long" else (1080, 1920)
    w = getattr(sc_mod, "WARM", {}).get(sc["sid"], 0.0)
    warm = (lambda t, d, w=w, c=sc["cues"]: w(t, d, c)) if callable(w) else w
    caps = caps_for(sc) if is_short(name) else None
    fn = sc_mod.SCENES[sc["sid"]]; overlay = None
    if is_short(name) and sc["sid"] in LONG_D:
        from shorts import vframe
        fn = vframe(fn, getattr(sc_mod, "SHORT_VIEW", {}).get(sc["sid"], "auto"))
    if hdr:
        from shorts import header
        overlay = header(hdr[0], hdr[1], hdr[2], sc["start"], hdr[3])
    out = f"{name}_{sc['sid']}"
    if still:
        os.makedirs(f"{WORK}/stills", exist_ok=True)
        render_scene(fn, sc["dur"], sc["cues"], f"{WORK}/stills/{out}", W, H, warm=warm, captions=caps, still=[f * sc["dur"] for f in still], overlay=overlay)
    else:
        os.makedirs(f"{WORK}/{name}", exist_ok=True)
        render_scene(fn, sc["dur"], sc["cues"], f"{WORK}/{name}/{sc['sid']}.mp4", W, H, warm=warm, captions=caps, overlay=overlay)
    return out

def render(still=None):
    only = arg("--only"); jobs = []
    shorts = [n for n in CUTS if n.startswith("short_")]; case = int(EID.split("-")[0])
    for name in names():
        pl, T = plan(name)
        hdr = (case, shorts.index(name) + 1, len(shorts), T) if name in shorts else None
        for sc in pl:
            if only and sc["sid"] not in only.split(","): continue
            jobs.append((name, sc, still, hdr))
    jobs.sort(key=lambda j: -j[1]["dur"])
    with Pool(os.cpu_count()) as p:
        for sid in p.imap_unordered(_job, jobs): print("rendered", sid, flush=True)
    if still:
        for name in names():
            for f in glob.glob(f"{WORK}/sheet_{name}_*.jpg"): os.remove(f)
            fs = sorted(glob.glob(f"{WORK}/stills/{name}_*.png"))
            fs = [f for f in fs if name != "short" or not os.path.basename(f).startswith("short_")]
            per = 12 if name == "long" else 10
            for i in range(0, len(fs), per):
                ins = " ".join(f"-i {f}" for f in fs[i:i + per]); n = len(fs[i:i + per])
                cols = 4 if name == "long" else 5
                lay = "|".join(f"{(j % cols)}*w0_{(j // cols)}*h0".replace("0*w0", "0").replace("_0*h0", "_0") for j in range(n))
                lay = "|".join(("0" if j % cols == 0 else "+".join(["w0"] * (j % cols))) + "_" + ("0" if j // cols == 0 else "+".join(["h0"] * (j // cols))) for j in range(n))
                sc = 480 if name == "long" else 216
                fc = ";".join(f"[{j}]scale={sc}:-1[v{j}]" for j in range(n)) + ";" + "".join(f"[v{j}]" for j in range(n)) + (f"xstack=inputs={n}:layout={lay}:fill=black" if n > 1 else "null")
                sh(f'ffmpeg -y -loglevel error {ins} -filter_complex "{fc}" -q:v 3 {WORK}/sheet_{name}_{i // per + 1:02d}.jpg')
        print("contact sheets in", WORK)

# ---------------------------------------------------------------- sound
def audio(name):
    import numpy as np, soundfile as sf
    pl, T = plan(name); SR = 44100; N = int((T + .5) * SR)
    voice = np.zeros(N, np.float32)
    for s in pl:
        for l in s["lines"]:
            w, sr = sf.read(f"{AUD}/{l['key']}.wav", dtype="float32")
            w2 = np.interp(np.arange(0, len(w), sr / SR), np.arange(len(w)), w).astype(np.float32)
            a = int(l["at"] * SR); w2 = w2[:max(0, N - a)]; voice[a:a + len(w2)] += w2
    t = np.arange(N) / SR; rs = np.random.RandomState(1); mus = np.zeros(N + SR * 12)
    def note(f, dur, kind):
        n = int(dur * SR); tt = np.arange(n) / SR; out = np.zeros(n)
        if kind == "pad":
            for det in (-.004, 0, .005):
                for h in range(1, 7): out += np.sin(2 * np.pi * f * (1 + det) * h * tt + h) / h ** 1.9
            return out * np.minimum(1, tt / 2.2) * np.minimum(1, (dur - tt) / 2.2) / 3
        if kind == "pluck":
            for h in range(1, 6): out += np.sin(2 * np.pi * f * h * tt) / h ** 1.4 * np.exp(-tt * (5 + h * 3))
            return out * np.minimum(1, tt / .004)
        return (np.sin(2 * np.pi * f * tt) + .3 * np.sin(4 * np.pi * f * tt)) * np.minimum(1, tt / .02) * np.exp(-tt * 2.2)
    def add(x, at, g=1.0):
        a = max(0, int(at * SR)); x = x[:max(0, len(mus) - a)]; mus[a:a + len(x)] += x * g
    hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    chords = getattr(S, "CHORDS", [(50, 53, 57, 62), (46, 50, 53, 58), (43, 46, 50, 55), (45, 49, 52, 57)])
    beat = 60 / C.BPM; bar = beat * 4
    for b in range(int(T / bar) + 2):
        ch = chords[(b // 2) % len(chords)]; t0 = b * bar
        if b % 2 == 0:
            for m in ch[:3]: add(note(hz(m), bar * 2 + 2.5, "pad"), t0, .16)
            add(note(hz(ch[0] + 19), bar * 2 + 2.5, "pad"), t0, .05)
        pat = [0, None, 2, 1, None, 2, 3, None] if (b // 2) % 2 == 0 else [0, 2, None, 1, 3, None, 2, None]
        for i, p in enumerate(pat):
            if p is not None: add(note(hz(ch[p] + 12), .9, "pluck"), t0 + i * beat / 2 + rs.uniform(-.006, .006), .16 if i % 2 == 0 else .1)
        add(note(hz(ch[0] - 12), 1.4, "bass"), t0, .32); add(note(hz(ch[0] - 12), 1.0, "bass"), t0 + beat * 2.5, .2)
        for i in range(8):
            n = int(.03 * SR); tick = np.diff(rs.randn(n) * np.exp(-np.arange(n) / SR * 160), prepend=0)
            add(tick, t0 + i * beat / 2, .035 if i % 2 else .015)
    mus = mus[:N]
    # stamp hits: (scene, line index or -1 for whole scene, offset s, fraction of that span)
    sc_mod = load("scenes"); Sd = {s["sid"]: s for s in pl}; sfx = np.zeros(N)
    hits = getattr(sc_mod, "HITS", []) if name == "long" else getattr(sc_mod, "SHORT_HITS", []) + (getattr(sc_mod, "HITS", []) if name != "short" else [])
    for sid, li, off, frac in hits:
        if sid not in Sd: continue
        s = Sd[sid]
        if li < 0: a, d = s["start"], s["dur"]
        else:
            c = s["cues"]; a = s["start"] + c[li]; d = (c[li + 1] if li + 1 < len(c) else s["dur"]) - c[li]
        h = a + off + d * frac; n = int(.5 * SR); tt = np.arange(n) / SR
        th = np.sin(2 * np.pi * (95 * np.exp(-tt * 9) + 42) * tt) * np.exp(-tt * 11) + rs.randn(n) * np.exp(-tt * 70) * .35
        k = int((h + .12) * SR); th = th[:max(0, N - k)]; sfx[k:k + len(th)] += th * .5
    m = mus / np.max(np.abs(mus)) * .5 * np.minimum(1, t / 1.5) * np.minimum(1, (T - t).clip(0) / 2.5)
    for nm, arr in (("voice", voice), ("music", m), ("sfx", sfx)): sf.write(f"{WORK}/{name}_{nm}.wav", arr.astype(np.float32), SR)
    sh(f'ffmpeg -y -loglevel error -i {WORK}/{name}_voice.wav -i {WORK}/{name}_music.wav -i {WORK}/{name}_sfx.wav -filter_complex '
       f'"[0:a]highpass=f=75,acompressor=threshold=-20dB:ratio=3:attack=8:release=160:makeup=2,loudnorm=I=-16:TP=-1.5:LRA=9,aresample=44100,asplit=2[v][vk];'
       f'[1:a]lowpass=f=5200,volume=0.55[mm];[mm][vk]sidechaincompress=threshold=0.03:ratio=5:attack=40:release=700[md];'
       f'[2:a]volume=0.9[s];[v][md][s]amix=inputs=3:normalize=0,alimiter=limit=0.9:level=false[o]" -map "[o]" -t {T:.3f} -ar 44100 {WORK}/{name}_mix.wav')
    print("audio", name, round(T, 1))

# ---------------------------------------------------------------- assemble
def final():
    os.makedirs(MEDIA, exist_ok=True)
    for name in names():
        cap = C.LONG_MAX_MB if name == "long" else C.SHORT_MAX_MB
        pl, T = plan(name)
        open(f"{WORK}/{name}.txt", "w").write("".join(f"file '{WORK}/{name}/{s['sid']}.mp4'\n" for s in pl))
        sh(f"ffmpeg -y -loglevel error -f concat -safe 0 -i {WORK}/{name}.txt -c copy {WORK}/{name}_video.mp4")
        kbps = int(cap * 8e6 / T / 1000 * .92) - 192
        tmp = f"{MEDIA}/{name}.part.mp4"
        sh(f"ffmpeg -y -loglevel error -i {WORK}/{name}_video.mp4 -i {WORK}/{name}_mix.wav -map 0:v -map 1:a -c:v libx264 -preset fast -crf 22 "
           f"-maxrate {kbps}k -bufsize {kbps * 2}k -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart -shortest {tmp}")
        os.replace(tmp, f"{MEDIA}/{name}.mp4"); print(name, f"{os.path.getsize(f'{MEDIA}/{name}.mp4') / 1e6:.1f} MB")

def thumbs():
    import skia
    from engine import vignette
    sc_mod = load("scenes"); os.makedirs(MEDIA, exist_ok=True)
    for i, word in enumerate(sc_mod.THUMB_WORDS):
        s = skia.Surface(1280, 720); c = s.getCanvas(); sc_mod.thumbnail(c, 1280, 720, word); c.drawImage(vignette(1280, 720), 0, 0)
        png = f"{WORK}/thumb_{i + 1}.png"; s.makeImageSnapshot().save(png, skia.kPNG)
        sh(f"ffmpeg -y -loglevel error -i {png} -q:v 2 {MEDIA}/thumb_{i + 1}.jpg")
    # phone-size greyscale check sheet
    ins = " ".join(f"-i {WORK}/thumb_{i + 1}.png" for i in range(len(sc_mod.THUMB_WORDS)))
    n = len(sc_mod.THUMB_WORDS)
    fc = ";".join(f"[{i}]scale=168:-1,hue=s=0[g{i}]" for i in range(n)) + ";" + "".join(f"[g{i}]" for i in range(n)) + f"hstack={n}"
    sh(f'ffmpeg -y -loglevel error {ins} -filter_complex "{fc}" {WORK}/thumb_check.png'); print("thumbs ok")

def qa():
    for name in names():
        f = f"{MEDIA}/{name}.mp4"
        out = subprocess.run(f"ffprobe -v error -show_entries format=duration,size -of csv=p=0 {f}", shell=True, capture_output=True, text=True).stdout.strip()
        lu = subprocess.run(f"ffmpeg -hide_banner -i {f} -af ebur128=framelog=quiet -f null - 2>&1 | grep -E ' I:' | tail -1", shell=True, capture_output=True, text=True).stdout.strip()
        print(name, out, lu)
    pl, T = plan("long")
    for s in pl: print(f"  {int(s['start'] // 60)}:{int(s['start'] % 60):02d}  {s['sid']}")
    d = os.path.join(EP, "description.txt")
    if os.path.exists(d): print("description words:", len(open(d).read().split()))

if __name__ == "__main__":
    stage = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "all"
    if stage in ("tts", "all"): tts()
    if stage == "plan":
        for n in names():
            pl, T = plan(n); [print(n, s["sid"], round(s["start"], 1), s["dur"]) for s in pl]; print(n, "TOTAL", round(T, 1))
    if stage == "stills": render(still=[float(x) for x in (arg("--at") or "0.3,0.65,0.95").split(",")])
    if stage in ("render", "all"): render()
    if stage in ("audio", "all"):
        for n in names(): audio(n)
    if stage in ("final", "all"): final()
    if stage in ("thumbs", "all"): thumbs()
    if stage in ("qa", "all"): qa()
