"""Render one still per narration beat (at frac of each beat) and tile them into contact sheets in <ep>/work/beats.
Run from the repo root: python3 pipeline/beats.py episodes/<id> long 0.8   (or short_a 0.85 [sid,sid])"""
import sys, os, glob
ep, cut, frac = sys.argv[1], sys.argv[2], float(sys.argv[3]); only = sys.argv[4].split(",") if len(sys.argv) > 4 else None
sys.argv = ["build.py", ep, "plan", "--names", cut]
sys.path.insert(0, "pipeline")
import importlib.util
spec = importlib.util.spec_from_file_location("build", "pipeline/build.py"); B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
from multiprocessing import Pool
pl, T = B.plan(cut)
out = f"{B.WORK}/beats"; os.makedirs(out, exist_ok=True)
for f in glob.glob(f"{out}/{cut}_*"): os.remove(f)
def job(sc):
    from engine import render_scene
    m = B.load("scenes"); fn = m.SCENES[sc["sid"]]
    W, H = (1920, 1080) if cut == "long" else (1080, 1920)
    if cut != "long" and sc["sid"] in B.LONG_D:
        from shorts import vframe; fn = vframe(fn, getattr(m, "SHORT_VIEW", {}).get(sc["sid"], "auto"))
    cues = sc["cues"]; ts = []
    for i, c0 in enumerate(cues):
        c1 = cues[i + 1] if i + 1 < len(cues) else sc["dur"]; ts.append(c0 + (c1 - c0) * frac)
    caps = B.caps_for(sc) if cut != "long" else None
    render_scene(fn, sc["dur"], cues, f"{out}/{cut}_{sc['sid']}", W, H, captions=caps, still=ts)
    return sc["sid"]
jobs = [s for s in pl if not only or s["sid"] in only]
with Pool(2) as p:
    for s in p.imap_unordered(job, jobs): pass
from PIL import Image
files = sorted(glob.glob(f"{out}/{cut}_*.png"), key=lambda f: ([s["sid"] for s in pl].index(os.path.basename(f)[len(cut) + 1:].rsplit("_", 1)[0]), f))
tw_ = 640 if cut == "long" else 360; th = 360 if cut == "long" else 640; cols = 3 if cut == "long" else 5; per = 12 if cut == "long" else 10
for k in range(0, len(files), per):
    chunk = files[k:k + per]; rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw_, rows * th))
    for i, f in enumerate(chunk):
        im = Image.open(f).convert("RGB").resize((tw_, th)); sheet.paste(im, ((i % cols) * tw_, (i // cols) * th))
    sheet.save(f"{out}/sheet_{cut}_{k // per:02d}.jpg", quality=85)
print(len(files), "stills")
