import math, random, subprocess, os, numpy as np, skia

INK = "#0b0c10"; NIGHT = "#161924"; PAPER = "#eadfc8"; PAPER2 = "#d9cba9"
GOLD = "#d4a94e"; RED = "#c0392b"; DIM = "#6d7284"; WHITE = "#f4efe4"; GREEN = "#5fa873"
FPS = 30


def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def seg(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def eo(x): x = clamp(x); return 1 - (1 - x) ** 3
def eio(x): x = clamp(x); return 4 * x * x * x if x < .5 else 1 - (-2 * x + 2) ** 3 / 2
def back(x):
    x = clamp(x); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
def lerp(a, b, x): return a + (b - a) * x


def col(h, a=1.0):
    h = h.lstrip("#")
    return skia.Color(int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(255 * clamp(a)))

def fill(h, a=1.0, blur=0):
    p = skia.Paint(Color=col(h, a), AntiAlias=True)
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p

def stroke(h, w, a=1.0, cap=True, blur=0):
    p = skia.Paint(Color=col(h, a), AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w)
    if cap: p.setStrokeCap(skia.Paint.kRound_Cap); p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur: p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p

_TF = {}
FAM = {"serif": ("Lora", False), "serifb": ("Lora", True), "sans": ("Inter", False), "sansb": ("Inter", True),
       "type": ("Courier 10 Pitch", False), "typeb": ("Courier 10 Pitch", True), "disp": ("TeX Gyre Pagella", True)}
def font(kind, size):
    if kind not in _TF:
        fam, b = FAM[kind]
        _TF[kind] = skia.Typeface(fam, skia.FontStyle.Bold() if b else skia.FontStyle.Normal())
    f = skia.Font(_TF[kind], size); f.setSubpixel(True); f.setEdging(skia.Font.Edging.kAntiAlias)
    return f

def tw(s, kind, size): return font(kind, size).measureText(s)

def text(c, s, x, y, size, kind="serif", color=WHITE, a=1.0, align="c", spacing=0, glow=0):
    if a <= 0 or not s: return 0
    f = font(kind, size)
    if spacing:
        widths = [f.measureText(ch) + spacing for ch in s]; w = sum(widths) - spacing
    else:
        w = f.measureText(s)
    x0 = x - w / 2 if align == "c" else (x - w if align == "r" else x)
    if glow:
        c.drawString(s, x0, y, f, fill(color, a * .6, glow)) if not spacing else None
    if spacing:
        xx = x0
        for ch, wd in zip(s, widths):
            c.drawString(ch, xx, y, f, fill(color, a)); xx += wd
    else:
        c.drawString(s, x0, y, f, fill(color, a))
    return w

def typed(c, s, x, y, size, p, kind="type", color=INK, a=1.0, align="l", cursor=False):
    n = int(len(s) * clamp(p)); sub = s[:n]
    f = font(kind, size); full = f.measureText(s)
    x0 = x - full / 2 if align == "c" else x
    c.drawString(sub, x0, y, f, fill(color, a))
    if cursor and 0 < p < 1:
        c.drawRect(skia.Rect.MakeXYWH(x0 + f.measureText(sub) + 2, y - size * .75, size * .5, size * .85), fill(color, a * .7))

def wrap(s, kind, size, maxw):
    words = s.split(); lines = []; cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(t, kind, size) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


class Ctx:
    def __init__(s, c, W, H, t, dur, cues):
        s.c = c; s.W = W; s.H = H; s.t = t; s.dur = dur; s.cues = cues
        s.cx = W / 2; s.cy = H / 2; s.u = min(W, H) / 1080; s.vert = H > W
    def ph(s, i, xf=0.3):
        """(local t, alpha) for narration line i; crossfades at boundaries"""
        a0 = s.cues[i]; a1 = s.cues[i + 1] if i + 1 < len(s.cues) else s.dur
        first = i == 0; last = i + 1 >= len(s.cues)
        al = (1 if first else seg(s.t, a0 - .05, a0 + xf)) * (1 if last else 1 - seg(s.t, a1 - xf, a1 - .05))
        return s.t - a0, al, a1 - a0
    def layer(s, a):
        if a >= .999: s.c.save()
        else: s.c.saveLayerAlpha(None, int(255 * clamp(a)))


# ---------- static plates ----------
_cache = {}
def bg_image(W, H, warm=0.0):
    key = ("bg", W, H, round(warm, 2))
    if key not in _cache:
        surf = skia.Surface(W, H); c = surf.getCanvas()
        c.clear(col("#07080b"))
        c0 = "#232838" if warm == 0 else "#4a3a34"
        sh = skia.GradientShader.MakeRadial(center=(W / 2, H * .46), radius=max(W, H) * .72,
                                            colors=[col(c0), col("#12141c"), col("#06070a")], positions=[0, .55, 1])
        p = skia.Paint(Shader=sh); c.drawPaint(p)
        rnd = random.Random(7)
        for _ in range(900):  # paper fibres
            x = rnd.uniform(0, W); y = rnd.uniform(0, H); l = rnd.uniform(10, 60); an = rnd.uniform(0, math.pi)
            c.drawLine(x, y, x + math.cos(an) * l, y + math.sin(an) * l, stroke("#ffffff", 1, rnd.uniform(.006, .022)))
        _cache[key] = surf.makeImageSnapshot()
    return _cache[key]

def vignette(W, H):
    key = ("vig", W, H)
    if key not in _cache:
        surf = skia.Surface(W, H); c = surf.getCanvas(); c.clear(0)
        sh = skia.GradientShader.MakeRadial(center=(W / 2, H / 2), radius=max(W, H) * .68,
                                            colors=[col("#000000", 0), col("#000000", 0), col("#000000", .78)], positions=[0, .55, 1])
        c.drawPaint(skia.Paint(Shader=sh)); _cache[key] = surf.makeImageSnapshot()
    return _cache[key]

def grain(W, H, i):
    key = ("gr", W, H)
    if key not in _cache:
        rs = np.random.RandomState(3); ims = []
        for k in range(6):
            n = rs.randint(0, 255, (H // 2, W // 2), dtype=np.uint8)
            arr = np.zeros((H // 2, W // 2, 4), np.uint8)
            v = (n > 127).astype(np.uint8) * 255
            al = (np.abs(n.astype(np.int16) - 127) // 9).astype(np.uint8)
            pm = (v.astype(np.uint16) * al // 255).astype(np.uint8)
            arr[..., 0] = pm; arr[..., 1] = pm; arr[..., 2] = pm; arr[..., 3] = al
            ims.append(skia.Image.fromarray(arr, colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType))
        _cache[key] = ims
    return _cache[key][i % 6]


# ---------- shared shapes ----------
def tower_path(h):
    """Eiffel-like silhouette, base centred at (0,0), height h (up = -y)."""
    def w(y):  # y 0 top..1 base
        return 0.006 + 0.205 * (y ** 2.35)
    P = skia.Path(); n = 60
    P.moveTo(0, -h * 1.04); P.lineTo(-0.004 * h, -h)
    for i in range(n + 1):
        y = i / n; P.lineTo(-w(y) * h, -h * (1 - y))
    P.lineTo(w(1) * h, 0)
    for i in range(n, -1, -1):
        y = i / n; P.lineTo(w(y) * h, -h * (1 - y))
    P.lineTo(0.004 * h, -h); P.close()
    cut = skia.Path()
    cut.addOval(skia.Rect.MakeLTRB(-0.135 * h, -0.15 * h, 0.135 * h, 0.2 * h))        # base arch
    c2 = skia.Path(); c2.moveTo(-0.045 * h, -0.215 * h); c2.lineTo(0.045 * h, -0.215 * h)
    c2.lineTo(0.016 * h, -0.34 * h); c2.lineTo(-0.016 * h, -0.34 * h); c2.close()
    out = skia.Op(P, cut, skia.PathOp.kDifference_PathOp)
    out = skia.Op(out, c2, skia.PathOp.kDifference_PathOp)
    for (yy, ww, th) in ((0.172, 0.158, 0.02), (0.352, 0.078, 0.014), (0.84, 0.02, 0.01)):  # platforms
        out.addRect(skia.Rect.MakeLTRB(-ww * h, -(yy + th) * h, ww * h, -yy * h))
    return out

def tower(c, x, y, h, color=INK, a=1.0, lattice=None, reveal=1.0, glow=0, la=.55):
    P = tower_path(h)
    c.save(); c.translate(x, y)
    if reveal < 1: c.clipRect(skia.Rect.MakeLTRB(-h, -h * 1.06 * reveal, h, 5))
    if glow: c.drawPath(P, fill(lattice or GOLD, a * .35, glow))
    c.drawPath(P, fill(color, a))
    if lattice:
        c.save(); c.clipPath(P, True)
        st = stroke(lattice, max(1, h * .0026), a * la, cap=False); step = h * .034
        k = -h * 1.3
        while k < h * 1.3:
            c.drawLine(k, 0, k + h * .55, -h * 1.1, st); c.drawLine(k, 0, k - h * .55, -h * 1.1, st); k += step
        c.restore()
        c.drawPath(P, stroke(lattice, max(1.2, h * .004), a * .9))
    c.restore()

def skyline(c, W, y, seed, color, a=1.0, hmin=40, hmax=150, shift=0, lit=0.0):
    rnd = random.Random(seed); x = -200 + shift
    while x < W + 200:
        bw = rnd.uniform(70, 170); bh = rnd.uniform(hmin, hmax)
        c.drawRect(skia.Rect.MakeXYWH(x, y - bh, bw, bh + 400), fill(color, a))
        roof = skia.Path(); roof.moveTo(x, y - bh); roof.lineTo(x + bw * .12, y - bh - 22); roof.lineTo(x + bw * .88, y - bh - 22); roof.lineTo(x + bw, y - bh); roof.close()
        c.drawPath(roof, fill(color, a))
        for k in range(rnd.randint(1, 3)):
            cxh = x + rnd.uniform(.2, .8) * bw
            c.drawRect(skia.Rect.MakeXYWH(cxh, y - bh - 44, 10, 26), fill(color, a))
        if lit:
            for wy in range(int(y - bh + 18), int(y - 6), 34):
                for wx in range(int(x + 14), int(x + bw - 16), 30):
                    if rnd.random() < lit:
                        c.drawRect(skia.Rect.MakeXYWH(wx, wy, 9, 15), fill(GOLD, a * rnd.uniform(.25, .7)))
        x += bw + rnd.uniform(-4, 6)

def figure(c, x, y, s, color=INK, a=1.0, hat=True, wide=1.0, rim=None, bow=0.0):
    """Bust silhouette; (x,y) = bottom centre; s = scale (height ~ 300*s)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    P = skia.Path()
    sw = 150 * wide
    P.moveTo(-sw, 0); P.cubicTo(-sw, -110, -80 * wide, -150, -34, -160); P.lineTo(-30, -190)
    P.lineTo(30, -190); P.lineTo(34, -160); P.cubicTo(80 * wide, -150, sw, -110, sw, 0); P.close()
    H = skia.Path(); H.addOval(skia.Rect.MakeLTRB(-52, -292 + bow * 14, 52, -172 + bow * 14))
    paints = [fill(color, a)]
    if rim: c.drawPath(P, fill(rim, a * .5, 16)); c.drawPath(H, fill(rim, a * .5, 16))
    c.drawPath(P, paints[0]); c.drawPath(H, paints[0])
    if hat:
        c.save(); c.translate(0, bow * 14)
        c.drawOval(skia.Rect.MakeLTRB(-84, -272, 84, -246), fill(color, a))
        cr = skia.Path(); cr.moveTo(-50, -258); cr.cubicTo(-56, -330, -30, -338, 0, -330); cr.cubicTo(30, -338, 56, -330, 50, -258); cr.close()
        c.drawPath(cr, fill(color, a))
        if rim: c.drawRect(skia.Rect.MakeLTRB(-50, -274, 50, -264), fill(rim, a * .8))
        c.restore()
    if rim:
        c.drawPath(P, stroke(rim, 2.5, a * .8)); c.drawPath(H, stroke(rim, 2.5, a * .8))
    c.restore()

def card(c, x, y, w, h, rot=0, a=1.0, color=PAPER, r=6):
    """Paper card centred at x,y. Leaves canvas translated to card's top-left; caller must c.restore()."""
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + 10, -h / 2 + 18, w, h), r, r, fill("#000000", .55 * a, 22))
    sh = skia.GradientShader.MakeLinear(points=[(0, -h / 2), (0, h / 2)], colors=[col(color, a), col(PAPER2, a)])
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), r, r, skia.Paint(Shader=sh, AntiAlias=True))
    c.translate(-w / 2, -h / 2)

def stamp(c, s, x, y, size, p, rot=-9, color=RED, a=.92):
    if p <= 0: return
    sc = lerp(2.6, 1, eo(seg(p, 0, 1))); al = a * seg(p, 0, .5)
    f = "sansb"; w = tw(s, f, size) + size * .9; h = size * 1.55
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sc, sc)
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 8, 8, stroke(color, size * .1, al))
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + size * .16, -h / 2 + size * .16, w - size * .32, h - size * .32), 5, 5, stroke(color, size * .035, al))
    text(c, s, 0, size * .36, size, f, color, al, spacing=size * .04)
    c.restore()

def label(c, s, x, y, size, p, color=GOLD, a=1.0, rule=True, align="c"):
    """small caps tracked label with typed reveal + rule"""
    if p <= 0: return
    n = int(len(s) * clamp(p * 1.3)); sp = size * .22
    wfull = sum(font("sansb", size).measureText(ch) + sp for ch in s) - sp
    x0 = x - wfull / 2 if align == "c" else x
    text(c, s[:n], x0, y, size, "sansb", color, a, align="l", spacing=sp)
    if rule: c.drawLine(x0, y + size * .7, x0 + wfull * eo(p), y + size * .7, stroke(color, max(1.5, size * .07), a * .7, cap=False))

def bar(c, x, y, w, h, p, color, a=1.0, track="#ffffff"):
    c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), h / 2, h / 2, fill(track, .12 * a))
    if p > 0: c.drawRoundRect(skia.Rect.MakeXYWH(x, y, max(h, w * clamp(p)), h), h / 2, h / 2, fill(color, a))

def banknote(c, x, y, w, rot=0, a=1.0, txt="100", color="#9db58a"):
    h = w * .44
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + 4, -h / 2 + 6, w, h), 4, 4, fill("#000000", .4 * a, 6))
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 4, 4, fill(color, a))
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + w * .04, -h / 2 + w * .04, w * .92, h - w * .08), 3, 3, stroke("#3f5a3a", max(1, w * .012), a * .8))
    c.drawOval(skia.Rect.MakeXYWH(-h * .28, -h * .32, h * .56, h * .64), stroke("#3f5a3a", max(1, w * .012), a * .8))
    text(c, txt, -w * .33, h * .12, h * .3, "serifb", "#2f4a2c", a); text(c, txt, w * .33, h * .12, h * .3, "serifb", "#2f4a2c", a)
    c.restore()

def envelope(c, x, y, w, rot=0, a=1.0, seal=True):
    h = w * .62
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawRect(skia.Rect.MakeXYWH(-w / 2 + 5, -h / 2 + 8, w, h), fill("#000000", .45 * a, 8))
    c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), fill(PAPER, a))
    P = skia.Path(); P.moveTo(-w / 2, -h / 2); P.lineTo(0, h * .08); P.lineTo(w / 2, -h / 2)
    c.drawPath(P, stroke("#a8997a", max(1.5, w * .012), a))
    if seal: c.drawCircle(0, h * .06, w * .07, fill(RED, a))
    c.restore()

def dashed(c, pts, p, color=GOLD, w=4, dash=16, a=1.0):
    """draw polyline progressively as dashes; returns head position"""
    segs = []; total = 0
    for i in range(len(pts) - 1):
        d = math.dist(pts[i], pts[i + 1]); segs.append(d); total += d
    target = total * clamp(p); done = 0; head = pts[0]; st = stroke(color, w, a)
    for i, d in enumerate(segs):
        if done >= target: break
        l = min(d, target - done); ux = (pts[i + 1][0] - pts[i][0]) / d; uy = (pts[i + 1][1] - pts[i][1]) / d
        k = 0
        while k < l:
            e = min(k + dash * .55, l)
            c.drawLine(pts[i][0] + ux * k, pts[i][1] + uy * k, pts[i][0] + ux * e, pts[i][1] + uy * e, st); k += dash
        head = (pts[i][0] + ux * l, pts[i][1] + uy * l); done += l
    return head

def arc_pts(a, b, lift, n=40):
    pts = []
    for i in range(n + 1):
        x = i / n; pts.append((lerp(a[0], b[0], x), lerp(a[1], b[1], x) - math.sin(x * math.pi) * lift))
    return pts

def pin(c, x, y, s, name, p, color=GOLD, a=1.0, below=True):
    if p <= 0: return
    c.drawCircle(x, y, 22 * s * eo(p), fill(color, .18 * a)); c.drawCircle(x, y, 8 * s * back(p), fill(color, a))
    label(c, name, x, y + (46 if below else -34) * s, 20 * s, seg(p, .2, 1), color, a, rule=False)

def caption(ctx, lines, p_in, a=1.0):
    c = ctx.c; size = 54 * ctx.u if ctx.vert else 44 * ctx.u
    y0 = ctx.H * (.745 if ctx.vert else .9) - (len(lines) - 1) * size * 1.25
    for i, l in enumerate(lines):
        y = y0 + i * size * 1.25; w = tw(l, "sansb", size)
        c.drawRoundRect(skia.Rect.MakeXYWH(ctx.cx - w / 2 - 22, y - size * .95, w + 44, size * 1.3), 10, 10, fill("#000000", .62 * a * p_in))
        text(c, l, ctx.cx, y, size, "sansb", WHITE, a * p_in)


# ---------- render ----------
def render_scene(fn, dur, cues, out, W=1920, H=1080, warm=0.0, captions=None, fade_in=.35, fade_out=.35, still=None, crf=17, overlay=None):
    surf = skia.Surface(W, H); c = surf.getCanvas()
    n = int(round(dur * FPS)); vig = vignette(W, H)
    frames = range(n) if still is None else [int(s * FPS) for s in still]
    proc = None
    if still is None:
        tmp = out.replace(".mp4", ".part.mp4")
        proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                 "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p", "-r", str(FPS), tmp], stdin=subprocess.PIPE)
    for fi in frames:
        t = fi / FPS; ctx = Ctx(c, W, H, t, dur, cues)
        w = warm(t, dur) if callable(warm) else warm
        c.drawImage(bg_image(W, H, 0), 0, 0)
        if w > 0: c.drawImage(bg_image(W, H, 1), 0, 0, skia.SamplingOptions(), skia.Paint(Alphaf=clamp(w)))
        c.save(); z = 1 + .035 * (t / max(dur, .1)); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-W / 2, -H / 2)
        fn(ctx); c.restore()
        c.drawImage(vig, 0, 0)
        c.save(); c.scale(2, 2); c.drawImage(grain(W, H, fi // 2), 0, 0, skia.SamplingOptions(), skia.Paint(Alphaf=.5)); c.restore()
        if overlay: overlay(ctx, t)
        if captions:
            for (a0, a1, lines) in captions:
                if a0 <= t < a1: caption(ctx, lines, eo(seg(t, a0, a0 + .18)))
        f = min(seg(t, 0, fade_in) if fade_in else 1, seg(dur - t, 0, fade_out) if fade_out else 1)
        if f < 1: c.drawPaint(skia.Paint(Color=col("#000000", 1 - f)))
        if still is not None:
            surf.makeImageSnapshot().save(f"{out}_{t:06.2f}.png", skia.kPNG); continue
        proc.stdin.write(surf.toarray(colorType=skia.kRGBA_8888_ColorType).tobytes())
    if proc:
        proc.stdin.close(); rc = proc.wait()
        if rc != 0: raise SystemExit("ffmpeg failed")
        os.replace(tmp, out)
