"""Reusable drawing pieces for Case Closed Files episodes. Built on engine.py."""
from engine import *

def ap(t, s, d=.5): return eo(seg(t, s, s + d))

def mark(c, x, y, size, p, ok):
    if p <= 0: return
    if ok:
        P = skia.Path(); P.moveTo(x - size * .5, y); P.lineTo(x - size * .15, y + size * .4); P.lineTo(x + size * .55, y - size * .45)
        c.save(); c.clipRect(skia.Rect.MakeLTRB(x - size, y - size, x - size * .6 + size * 1.3 * eo(p), y + size)); c.drawPath(P, stroke(GOLD, size * .2)); c.restore()
    else:
        q = eo(p)
        c.drawLine(x - size * .45, y - size * .45, x - size * .45 + size * .9 * q, y - size * .45 + size * .9 * q, stroke(RED, size * .2))
        if p > .4:
            q2 = eo(seg(p, .4, 1)); c.drawLine(x + size * .45, y - size * .45, x + size * .45 - size * .9 * q2, y - size * .45 + size * .9 * q2, stroke(RED, size * .2))

def item(c, s, x, y, size, t, t0, ok=None, color=WHITE, kind="sansb"):
    p = seg(t, t0, t0 + .5)
    if p <= 0: return
    text(c, s, x + (1 - eo(p)) * 30, y, size, kind, color, eo(p), align="l", spacing=size * .06)
    if ok is not None: mark(c, x - size * 1.1, y - size * .32, size * .8, seg(t, t0 + .35, t0 + .8), ok)

# ------------------------------------------------------------------ shared comps
def paris(ctx, a=1.0, shift=0, tower_gold=0.0, tx=.66, lit=.16, sun=0.0):
    c = ctx.c; W, H = ctx.W, ctx.H; base = H * .8
    if sun > 0:
        sy = lerp(base + 60, base - 260, eo(sun))
        c.drawCircle(W * tx, sy, 420, fill("#ffb45e", .25 * a * sun, 120)); c.drawCircle(W * tx, sy, 150, fill("#ffd28a", .9 * a * sun, 8))
    else:
        c.drawCircle(W * .88, H * .2, 190, fill("#f1e6c8", .1 * a, 70)); c.drawCircle(W * .88, H * .2, 58, fill("#f1e6c8", .92 * a))
    skyline(c, W, base - 14, 11, "#1b1f2d" if not sun else "#3a2a2a", a, 60, 190, shift * .4)
    tower(c, W * tx + shift * .6, base, H * .62, color="#10121a", a=a, lattice=GOLD if tower_gold else "#3a4055", glow=30 * tower_gold, la=.35 + .4 * tower_gold)
    skyline(c, W, base + 40, 5, "#0a0b10", a, 50, 150, shift, lit=lit)
    c.drawRect(skia.Rect.MakeLTRB(0, base + 38, W, H), fill("#0a0b10", a))

def letter(ctx, t, d, x, y, a=1.0, h=900):
    c = ctx.c; w = 780
    card(c, x, y, w, h, rot=-1.6, a=a)
    text(c, "RÉPUBLIQUE FRANÇAISE", w / 2, 78, 20, "serif", "#5a4d38", a, spacing=6)
    text(c, "MINISTÈRE DES POSTES", w / 2, 132, 38, "serifb", INK, a, spacing=2)
    text(c, "ET TÉLÉGRAPHES", w / 2, 178, 38, "serifb", INK, a, spacing=2)
    c.drawLine(120, 208, w - 120, 208, stroke(INK, 2, a, cap=False)); c.drawLine(120, 215, w - 120, 215, stroke(INK, 1, a, cap=False))
    text(c, "Paris, 1925", w - 80, 276, 24, "type", "#3b3324", a, align="r")
    body = ["Monsieur,", "", "You are invited to a confidential", "meeting regarding a government", "contract of the highest importance.", "",
            "Hôtel de Crillon,", "Place de la Concorde.", "", "Strictly private."]
    tot = sum(len(b) for b in body); done = 0; pp = seg(t, .5, d * .62) * tot
    for i, b in enumerate(body):
        if b: typed(c, b, 80, 340 + i * 44, 28, clamp((pp - done) / len(b)), color="#1d1a14", a=a, cursor=True)
        done += len(b)
    sy = h - 150
    if t > d * .64:
        c.drawLine(w - 400, sy, w - 80, sy, stroke(INK, 1.5, a, cap=False))
        typed(c, "Deputy Director General", w - 400, sy + 36, 22, seg(t, d * .64, d * .74), color="#1d1a14", a=a)
    text(c, "RECONSTRUCTION", 80, h - 40, 14, "sansb", "#8c7d60", a, align="l", spacing=3)
    stamp(c, "FORGED", w * .42, sy - 30, 74, seg(t, d * .8, d * .8 + .35), rot=-12)
    c.restore()

def two(ctx, a=1.0, sp=330, env=None, lrim=GOLD, rrim="#7d8fb3", bow=0.0):
    c = ctx.c; cx, cy = ctx.cx, ctx.cy; y = cy + 360
    L = skia.Path(); L.moveTo(cx - 60, cy - 620); L.lineTo(cx + 60, cy - 620); L.lineTo(cx + 560, y); L.lineTo(cx - 560, y); L.close()
    sh = skia.GradientShader.MakeLinear(points=[(0, cy - 620), (0, y)], colors=[col("#ffe2a0", .22 * a), col("#ffe2a0", .02 * a)])
    c.drawPath(L, skia.Paint(Shader=sh, AntiAlias=True))
    figure(c, cx - sp, y, 1.12, a=a, rim=lrim); figure(c, cx + sp, y, 1.12, a=a, hat=False, rim=rrim, bow=bow)
    c.drawRoundRect(skia.Rect.MakeXYWH(cx - 250, y - 96, 500, 22), 6, 6, fill("#3a261c", a)); c.drawRect(skia.Rect.MakeXYWH(cx - 14, y - 76, 28, 80), fill("#2a1b14", a))
    if env is not None and env > 0:
        envelope(c, lerp(cx + 180, cx - 170, eio(env)), y - 120, 120, rot=lerp(8, -6, env), a=a * seg(env, 0, .15))

def suspicion(ctx, v, y, a=1.0, w=560):
    c = ctx.c; colr = RED if v > .4 else GREEN
    label(c, "SUSPICION", ctx.cx, y - 26, 22, 1, colr, a, rule=False)
    bar(c, ctx.cx - w / 2, y, w, 22, v, colr, a)

def route(ctx, p, A, B, a=1.0, rev=False, sp=400):
    c = ctx.c; cx, cy = ctx.cx, ctx.cy
    for i in range(-6, 7):
        c.drawLine(cx + i * 150, cy - 420, cx + i * 150 + 40, cy + 420, stroke("#ffffff", 1, .05 * a, cap=False))
    for j in range(-3, 4):
        c.drawLine(cx - 900, cy + j * 130, cx + 900, cy + j * 130 - 30, stroke("#ffffff", 1, .05 * a, cap=False))
    pa = (cx - sp, cy + 70); pb = (cx + sp, cy - 50)
    pts = arc_pts(pa, pb, 150)
    if rev: pts = pts[::-1]
    pin(c, pa[0], pa[1], 1.5, A, 1, a=a); pin(c, pb[0], pb[1], 1.5, B, seg(p, .0, .3) if not rev else 1, a=a)
    hx, hy = dashed(c, pts, eio(p), w=5, a=a)
    c.drawRoundRect(skia.Rect.MakeXYWH(hx - 34, hy - 16, 68, 32), 8, 8, fill(GOLD, a))
    for k in (-18, 0, 18): c.drawRect(skia.Rect.MakeXYWH(hx + k - 6, hy - 9, 12, 10), fill(INK, a))

def notes_pile(ctx, p, x, y, n=14, a=1.0, w=250):
    rnd = random.Random(4)
    for i in range(n):
        q = seg(p, i / n * .85, i / n * .85 + .15); r = rnd.uniform(-16, 16); ox = rnd.uniform(-60, 60); oy = -i * 9
        if q > 0: banknote(ctx.c, x + ox, lerp(y - 700, y + oy, eo(q)), w, rot=lerp(r * 4, r, q), a=a * seg(q, 0, .3))

def liner(ctx, t, d, a=1.0, lab="THE ATLANTIC"):
    c = ctx.c; W, H = ctx.W, ctx.H; sea = H * .68
    c.drawCircle(W * .8, H * .22, 50, fill("#f1e6c8", .9 * a)); c.drawCircle(W * .8, H * .22, 170, fill("#f1e6c8", .08 * a, 60))
    x = lerp(W * .16, W * .58, t / d); y = sea + math.sin(t * 1.4) * 5
    for k in range(4):
        fx = x - 150 + k * 95
        for j in range(5):
            age = (t * .6 + j * .2 + k * .13) % 1
            c.drawCircle(fx - age * 150, y - 205 - age * 90, 16 + age * 40, fill("#8d93a8", .16 * a * (1 - age), 10))
        c.drawRect(skia.Rect.MakeXYWH(fx - 22, y - 200, 44, 110), fill("#0c0d12", a)); c.drawRect(skia.Rect.MakeXYWH(fx - 22, y - 200, 44, 20), fill(RED, a * .9))
    c.drawRect(skia.Rect.MakeXYWH(x - 250, y - 100, 440, 46), fill("#14161f", a))
    for k in range(13): c.drawRect(skia.Rect.MakeXYWH(x - 232 + k * 32, y - 86, 12, 12), fill(GOLD, a * .8))
    P = skia.Path(); P.moveTo(x - 340, y - 56); P.lineTo(x + 330, y - 56); P.lineTo(x + 260, y + 40); P.lineTo(x - 300, y + 40); P.close()
    c.drawPath(P, fill("#0c0d12", a))
    for k in range(20): c.drawCircle(x - 270 + k * 27, y - 26, 4, fill(GOLD, a * .7))
    c.drawRect(skia.Rect.MakeLTRB(0, sea + 18, W, H), fill("#0b0e17", a))
    for j in range(5):
        P = skia.Path(); yy = sea + 18 + j * 46
        for i in range(0, int(W) + 40, 40):
            v = yy + math.sin(i * .012 + t * (1.2 + j * .2) + j) * (7 + j * 2)
            P.moveTo(i, v) if i == 0 else P.lineTo(i, v)
        c.drawPath(P, stroke("#2c3550", 3, a * (.9 - j * .12)))
    label(c, lab, ctx.cx, H * .12, 26, seg(t, .3, 1.5), a=a)

def checklist_tower(ctx, t, a, x):
    pass

# ------------------------------------------------------------------ long-form scenes
def moneybox(ctx, t0, d0, t1, d1, a=1.0):
    c = ctx.c; cx, cy = ctx.cx, ctx.cy; bw, bh = 560, 320; x0, y0 = cx - bw / 2, cy - bh / 2 + 20
    def bill(x, y, r=0, al=1): banknote(c, x, y, 230, rot=r, a=a * al)
    # bill going in (left)
    pin_ = seg(t0, d0 * .24, d0 * .42)
    if 0 < pin_ < 1:
        c.save(); c.clipRect(skia.Rect.MakeLTRB(0, 0, x0 + 6, ctx.H)); bill(lerp(cx - 760, x0 + 120, eio(pin_)), cy + 30); c.restore()
    # bills out (right)
    outs = [(d0 * .86, 0)] + [(d0 * .93, 1)]
    outs2 = [(d1 * .16, 2), (d1 * .24, 3), (d1 * .32, 4)]
    c.save(); c.clipRect(skia.Rect.MakeLTRB(x0 + bw - 6, 0, ctx.W, ctx.H))
    for (ts, i) in outs:
        q = seg(t0, ts, ts + .9)
        if q > 0: bill(lerp(x0 + bw - 110, cx + 520 + i * 26, eo(q)), cy + 30 - i * 30 + (i % 2) * 8, r=(i - 2) * 5)
    for (ts, i) in outs2:
        q = seg(t1, ts, ts + .9)
        if q > 0: bill(lerp(x0 + bw - 110, cx + 520 + i * 20, eo(q)), cy + 30 - i * 30, r=(i - 2) * 5)
    c.restore()
    c.drawRoundRect(skia.Rect.MakeXYWH(x0 + 12, y0 + 22, bw, bh), 18, 18, fill("#000000", .6 * a, 26))
    sh = skia.GradientShader.MakeLinear(points=[(0, y0), (0, y0 + bh)], colors=[col("#6b3a26", a), col("#3a1d13", a)])
    c.drawRoundRect(skia.Rect.MakeXYWH(x0, y0, bw, bh), 18, 18, skia.Paint(Shader=sh, AntiAlias=True))
    for k in range(7): c.drawLine(x0 + 20, y0 + 30 + k * 42, x0 + bw - 20, y0 + 36 + k * 42, stroke("#2a140c", 2, .35 * a, cap=False))
    for (px, py) in ((x0, y0), (x0 + bw, y0), (x0, y0 + bh), (x0 + bw, y0 + bh)):
        c.save(); c.clipRect(skia.Rect.MakeXYWH(x0, y0, bw, bh)); c.drawCircle(px, py, 46, fill(GOLD, a)); c.restore()
    dead = t1 > d1 * .62
    for k, dx in enumerate((-130, 130)):
        c.drawCircle(cx + dx, cy - 20, 56, fill("#1c1210", a)); c.drawCircle(cx + dx, cy - 20, 56, stroke(GOLD, 6, a))
        an = (t0 * (60 + k * 30) if not dead else 200) * math.pi / 180
        c.drawLine(cx + dx, cy - 20, cx + dx + math.cos(an) * 40, cy - 20 + math.sin(an) * 40, stroke(GOLD, 6, a))
    c.drawRoundRect(skia.Rect.MakeXYWH(cx - 110, cy + 80, 220, 50), 6, 6, fill(GOLD, a)); text(c, "MONEY BOX", cx, cy + 115, 24, "sansb", "#2a140c", a, spacing=4)
    c.drawRect(skia.Rect.MakeXYWH(x0 - 4, cy + 14, 14, 36), fill("#0a0605", a)); c.drawRect(skia.Rect.MakeXYWH(x0 + bw - 10, cy + 14, 14, 36), fill("#0a0605", a))
    c.drawCircle(cx, y0 + 40, 10, fill(RED if dead else GREEN, a)); c.drawCircle(cx, y0 + 40, 22, fill(RED if dead else GREEN, .3 * a, 10))

def newspaper(ctx, x, y, w, h, rot, head, sub, kicker, a=1.0, hp=1.0, circle=0.0):
    c = ctx.c; card(c, x, y, w, h, rot=rot, a=a, r=2)
    text(c, kicker, w / 2, 62, 22, "serif", "#3b3324", a, spacing=8)
    c.drawLine(40, 84, w - 40, 84, stroke(INK, 3, a, cap=False)); c.drawLine(40, 92, w - 40, 92, stroke(INK, 1, a, cap=False))
    for i, hl in enumerate(head): typed(c, hl, w / 2, 170 + i * 74, 62, clamp(hp * len(head) - i), "serifb", "#14110c", a, align="c")
    y0 = 170 + len(head) * 74 - 20
    text(c, sub, w / 2, y0 + 10, 26, "serif", "#3b3324", a * seg(hp, .9, 1))
    cols = 3; cw = (w - 80 - (cols - 1) * 30) / cols; rnd = random.Random(2)
    for k in range(cols):
        yy = y0 + 60
        while yy < h - 50:
            c.drawRect(skia.Rect.MakeXYWH(40 + k * (cw + 30), yy, cw * rnd.uniform(.7, 1), 7), fill("#8a7c62", .55 * a)); yy += 19
    if circle > 0:
        P = skia.Path(); P.addOval(skia.Rect.MakeXYWH(30, 104, w - 60, len(head) * 74 + 30))
        pm = skia.PathMeasure(P, False); seg_ = skia.Path(); pm.getSegment(0, pm.getLength() * eo(circle), seg_, True)
        c.drawPath(seg_, stroke(RED, 7, a * .9))
    text(c, "ILLUSTRATION", 40, h - 20, 13, "sansb", "#8c7d60", a, align="l", spacing=3)
    c.restore()

def hotel(ctx, a=1.0, t=0):
    c = ctx.c; W, H, cx = ctx.W, ctx.H, ctx.cx; base = H * .86; w = 1420; h = 520; x0 = cx - w / 2
    c.drawCircle(cx, base - h, 500, fill("#ffd48a", .07 * a, 120))
    c.drawRect(skia.Rect.MakeXYWH(x0, base - h, w, h), fill("#171a26", a))
    c.drawRect(skia.Rect.MakeXYWH(x0 - 20, base - h - 26, w + 40, 26), fill("#20243300" if False else "#202433", a))
    for k in range(40): c.drawRect(skia.Rect.MakeXYWH(x0 + k * (w / 40) + 8, base - h - 60, 8, 34), fill("#202433", a))
    c.drawRect(skia.Rect.MakeXYWH(x0 - 10, base - h - 66, w + 20, 8), fill("#202433", a))
    n = 13; rnd = random.Random(3)
    for k in range(n):
        xx = x0 + 50 + k * ((w - 100) / (n - 1))
        c.drawRect(skia.Rect.MakeXYWH(xx - 12, base - h + 40, 24, 270), fill("#2a2f42", a))
        c.drawRect(skia.Rect.MakeXYWH(xx - 18, base - h + 30, 36, 14), fill("#2f3550", a))
    for k in range(n - 1):
        xx = x0 + 50 + (k + .5) * ((w - 100) / (n - 1)); g = .35 + .6 * rnd.random()
        fl = .85 + .15 * math.sin(t * 2 + k)
        c.drawRect(skia.Rect.MakeXYWH(xx - 22, base - h + 70, 44, 110), fill("#ffcf7a", a * g * fl)); c.drawRect(skia.Rect.MakeXYWH(xx - 22, base - h + 200, 44, 80), fill("#ffcf7a", a * g * .7))
        P = skia.Path(); P.addRoundRect(skia.Rect.MakeXYWH(xx - 30, base - 170, 60, 170), 30, 30); c.drawPath(P, fill("#ffcf7a", a * (.3 + g * .5)))
    c.drawRect(skia.Rect.MakeXYWH(x0, base - 196, w, 10), fill("#2a2f42", a))
    c.drawRect(skia.Rect.MakeLTRB(0, base, W, H), fill("#0a0b10", a))

def table(ctx, rims=(0, 0, 0, 0, 0), envs=0.0):
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy
    c.drawCircle(cx, cy - 200, 560, fill("#ffd48a", .06, 140))
    figure(c, cx, cy + 190, 1.25, rim=GOLD)
    c.drawOval(skia.Rect.MakeLTRB(cx - 760, cy + 150, cx + 760, cy + 470), fill("#2c1c15")); c.drawOval(skia.Rect.MakeLTRB(cx - 760, cy + 150, cx + 760, cy + 470), stroke("#4a3024", 5))
    for k in range(-2, 3):
        x = cx + k * 300; y = H + 150 - (2 - abs(k)) * 16
        if envs > 0: envelope(c, x, cy + 300 - (2 - abs(k)) * 20, 110, rot=k * 5, a=seg(envs, (k + 2) * .15, (k + 2) * .15 + .3))
        r = rims[k + 2]
        figure(c, x, y, 1.35, hat=False, rim=GOLD if r > 0 else "#2b3044", a=1)
        if r > 0: c.drawCircle(x, y - 330, 150, fill(GOLD, .12 * r, 60))

def col_fade(h, f): return h if f >= 1 else "#%02x%02x%02x" % tuple(int(int(h[i:i + 2], 16) * (.25 + .75 * f)) for i in (1, 3, 5))

def poisson_alone(ctx, t, a, txt="TOO HUMILIATED TO TELL ANYONE"):
    c = ctx.c; cx, cy = ctx.cx, ctx.cy
    c.drawCircle(cx, cy - 60, 420, fill("#5d76b0", .1 * a, 120))
    figure(c, cx, cy + 420, 1.9, hat=False, rim="#7d8fb3", bow=eo(seg(t, .2, 1.6)) * 1.5, a=a)
    label(c, txt, cx, cy - 400, 28, seg(t, .8, 2.2), "#b8c4e0", a)

def ny(ctx, a=1.0):
    c = ctx.c; W, H = ctx.W, ctx.H; rnd = random.Random(21); x = -40
    while x < W + 40:
        bw = rnd.uniform(70, 150); bh = rnd.uniform(160, 560)
        c.drawRect(skia.Rect.MakeXYWH(x, H - bh, bw, bh), fill("#10131c", a))
        if rnd.random() < .4: c.drawRect(skia.Rect.MakeXYWH(x + bw * .3, H - bh - 50, bw * .4, 50), fill("#10131c", a)); c.drawRect(skia.Rect.MakeXYWH(x + bw * .48, H - bh - 110, 4, 60), fill("#10131c", a))
        for wy in range(int(H - bh + 16), int(H), 30):
            for wx in range(int(x + 10), int(x + bw - 12), 22):
                if rnd.random() < .18: c.drawRect(skia.Rect.MakeXYWH(wx, wy, 8, 13), fill(GOLD, a * rnd.uniform(.2, .55)))
        x += bw + 4

def chip(c, s, x, y, a=1.0, color=GOLD, size=44):
    w = tw(s, "sansb", size) + 60
    c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2, y - size * .9, w, size * 1.6), size * .8, size * .8, fill("#000000", .5 * a, 12))
    c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2, y - size * .9, w, size * 1.6), size * .8, size * .8, fill(color, a))
    text(c, s, x, y + size * .22, size, "sansb", INK, a)

def climber(c, x, y, s, t, wipe=False, run=False):
    c.save(); c.translate(x, y); c.scale(s, s); p = fill(GOLD); st = stroke(GOLD, 9)
    sw = math.sin(t * 9) * (18 if run else 5)
    c.drawCircle(0, -62, 13, p); c.drawRoundRect(skia.Rect.MakeXYWH(-11, -50, 22, 42), 8, 8, p)
    c.drawLine(-5, -10, -8 - sw, 26, st); c.drawLine(5, -10, 8 + sw, 26, st)
    if wipe:
        hx = 34 + math.sin(t * 6) * 12; hy = -70 + math.cos(t * 6) * 10
        c.drawLine(8, -42, hx, hy, st); c.drawLine(-8, -42, -4, -78, st); c.drawRect(skia.Rect.MakeXYWH(hx - 8, hy - 8, 18, 14), fill(PAPER))
    elif run: c.drawLine(8, -42, 26, -24 + sw, st); c.drawLine(-8, -42, -26, -24 - sw, st)
    else: c.drawLine(8, -42, 3, -80 + sw, st); c.drawLine(-8, -42, -3, -72 - sw, st)
    c.restore()

def alcatraz(ctx, t, a=1.0):
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy; sea = H * .7
    c.drawCircle(W * .76, H * .2, 60, fill("#f1e6c8", .9 * a)); c.drawCircle(W * .76, H * .2, 220, fill("#f1e6c8", .08 * a, 70))
    P = skia.Path(); P.moveTo(cx - 620, sea + 10); P.cubicTo(cx - 520, sea - 90, cx - 300, sea - 150, cx - 80, sea - 150); P.lineTo(cx + 300, sea - 150)
    P.cubicTo(cx + 460, sea - 130, cx + 560, sea - 60, cx + 640, sea + 10); P.close(); c.drawPath(P, fill("#0b0c11", a))
    c.drawRect(skia.Rect.MakeXYWH(cx - 280, sea - 250, 520, 104), fill("#0b0c11", a))
    for k in range(16): c.drawRect(skia.Rect.MakeXYWH(cx - 262 + k * 32, sea - 226, 12, 20), fill(GOLD, a * (.25 + .3 * ((k * 7) % 3 == 0))))
    c.drawRect(skia.Rect.MakeXYWH(cx + 330, sea - 320, 22, 180), fill("#0b0c11", a)); c.drawRect(skia.Rect.MakeXYWH(cx + 322, sea - 340, 38, 24), fill("#0b0c11", a))
    an = t * .9; L = skia.Path(); L.moveTo(cx + 341, sea - 328); L.lineTo(cx + 341 + math.cos(an) * 900, sea - 328 - abs(math.sin(an)) * 200 - 60); L.lineTo(cx + 341 + math.cos(an) * 900, sea - 328 - abs(math.sin(an)) * 200 + 60); L.close()
    c.drawPath(L, fill("#ffe2a0", .12 * a, 12)); c.drawCircle(cx + 341, sea - 328, 9, fill("#ffe2a0", a))
    c.drawRect(skia.Rect.MakeLTRB(0, sea, W, H), fill("#090c15", a))
    for j in range(5):
        Pw = skia.Path(); yy = sea + 16 + j * 54
        for i in range(0, int(W) + 40, 40):
            v = yy + math.sin(i * .011 + t * (1 + j * .2) + j) * (6 + j * 2); Pw.moveTo(i, v) if i == 0 else Pw.lineTo(i, v)
        c.drawPath(Pw, stroke("#27304a", 3, a * (.9 - j * .13)))

# generic alias: a lone figure, head bowed, with a caption above
figure_alone = poisson_alone

# ---- thumbnail helpers (pass the thumbnail-design checks: bold, outlined, readable in greyscale at 168 px)
def solid_stamp(c, s, x, y, size, rot=-12, color="#d0342c", ink="#f6e7c8"):
    c.save(); c.translate(x, y); c.rotate(rot)
    f = font("sansb", size); w = f.measureText(s) + size * .7; h = size * 1.3
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + 8, -h / 2 + 12, w, h), 14, 14, fill("#000000", .7, 14))
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 14, 14, fill(color))
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + 12, -h / 2 + 12, w - 24, h - 24), 9, 9, stroke(ink, 5))
    c.drawString(s, -f.measureText(s) / 2, size * .36, f, fill(ink)); c.restore()

def big_word(c, t, x, y, size, colr):
    f = font("sansb", size); w = f.measureText(t)
    c.drawString(t, x - w / 2 + 6, y + 8, f, fill("#000000", .9, 8))
    c.drawString(t, x - w / 2, y, f, stroke("#000000", size * .09))
    c.drawString(t, x - w / 2, y, f, fill(colr))


# ======================= added for 002, reusable =======================
def painting(c, x, y, w, h, a=1.0, seed=0, reveal=1.0, crack=0.0, ink=0.0, glow=0.0, frame=True, label=None, lab_a=1.0):
    """An invented old-master-style painting (abstract figures, blue + yellow light).
    Never a copy of a real artwork. (x, y) = centre."""
    if a <= 0: return
    rnd = random.Random(seed); fw = w * .07 if frame else 0
    if glow: c.drawRect(skia.Rect.MakeXYWH(x - w / 2 - 30, y - h / 2 - 30, w + 60, h + 60), fill("#ffcf7a", .18 * glow * a, 60))
    c.drawRect(skia.Rect.MakeXYWH(x - w / 2 + 10, y - h / 2 + 16, w, h), fill("#000000", .6 * a, 22))
    if frame:
        sh = skia.GradientShader.MakeLinear(points=[(x - w / 2, y - h / 2), (x + w / 2, y + h / 2)], colors=[col("#e7c46a", a), col("#8a6326", a), col("#d9b25a", a)])
        c.drawRect(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), skia.Paint(Shader=sh, AntiAlias=True))
        c.drawRect(skia.Rect.MakeXYWH(x - w / 2 + fw * .45, y - h / 2 + fw * .45, w - fw * .9, h - fw * .9), stroke("#5a3e14", 3, a, cap=False))
    ix, iy, iw, ih = x - w / 2 + fw, y - h / 2 + fw, w - 2 * fw, h - 2 * fw
    c.save(); c.clipRect(skia.Rect.MakeXYWH(ix, iy, iw, ih))
    c.drawRect(skia.Rect.MakeXYWH(ix, iy, iw, ih), fill("#2a2016", a))
    if reveal > 0:
        c.save(); c.clipRect(skia.Rect.MakeXYWH(ix, iy, iw, ih * clamp(reveal)))
        lx = ix + iw * rnd.uniform(.25, .4)
        sh = skia.GradientShader.MakeRadial(center=(lx, iy + ih * .3), radius=iw * .9, colors=[col("#c9a46a", a), col("#5a4126", a), col("#1d150d", a)], positions=[0, .45, 1])
        c.drawRect(skia.Rect.MakeXYWH(ix, iy, iw, ih), skia.Paint(Shader=sh))
        c.drawRect(skia.Rect.MakeXYWH(ix, iy + ih * .66, iw, ih * .34), fill("#3a2a1a", .9 * a))       # table
        c.drawRect(skia.Rect.MakeXYWH(ix, iy + ih * .64, iw, ih * .04), fill("#efe4c9", .85 * a))      # cloth edge
        n = rnd.randint(2, 4); cols = ["#2e4f8f", "#c8a23c", "#7a2b22", "#3b5a3a"]
        for k in range(n):
            fx = ix + iw * (k + .5) / n + rnd.uniform(-.05, .05) * iw; fy = iy + ih * .68
            P = skia.Path(); P.moveTo(fx - iw * .13, fy + ih * .1); P.cubicTo(fx - iw * .12, fy - ih * .25, fx + iw * .12, fy - ih * .25, fx + iw * .13, fy + ih * .1); P.close()
            c.drawPath(P, fill(cols[(k + seed) % 4], .9 * a))
            c.drawCircle(fx, fy - ih * .3, iw * .045, fill("#d7b083", a)); c.drawCircle(fx - iw * .01, fy - ih * .32, iw * .02, fill("#f3dcb0", .5 * a, 4))
        c.drawOval(skia.Rect.MakeXYWH(ix + iw * .44, iy + ih * .58, iw * .12, ih * .07), fill("#efe4c9", a))  # jug/plate
        c.restore()
        if 0 < reveal < 1:  # wet edge
            c.drawRect(skia.Rect.MakeXYWH(ix, iy + ih * reveal - 4, iw, 8), fill("#e8d2a0", .5 * a, 4))
    if crack > 0:
        r2 = random.Random(seed + 99); st = stroke("#0d0906" if ink > .5 else "#d8c6a0", 1.6, a * (.35 + .5 * ink) * clamp(crack * 1.5))
        for k in range(int(70 * crack)):
            px, py = ix + r2.uniform(0, iw), iy + r2.uniform(0, ih)
            P = skia.Path(); P.moveTo(px, py)
            for j in range(4): px += r2.uniform(-28, 28); py += r2.uniform(-28, 28); P.lineTo(px, py)
            c.drawPath(P, st)
    if ink > 0: c.drawRect(skia.Rect.MakeXYWH(ix, iy, iw, ih), fill("#120c06", .25 * ink * a))
    c.restore()
    if label: label_plate(c, label, x, y + h / 2 + 46, a * lab_a)

def label_plate(c, s, x, y, a=1.0, size=22):
    w = tw(s, "sansb", size) + len(s) * 2 + 44
    c.drawRect(skia.Rect.MakeXYWH(x - w / 2, y - size * 1.1, w, size * 1.7), fill("#e9dfc6", a))
    text(c, s, x, y + size * .1, size, "sansb", "#2a2216", a, spacing=2)

def easel(c, x, y, s=1.0, a=1.0, color="#5a3a22"):
    st = stroke(color, 14 * s, a)
    c.drawLine(x - 170 * s, y, x - 40 * s, y - 760 * s, st); c.drawLine(x + 170 * s, y, x + 40 * s, y - 760 * s, st)
    c.drawLine(x, y - 40 * s, x, y - 700 * s, st); c.drawLine(x - 230 * s, y - 210 * s, x + 230 * s, y - 210 * s, stroke(color, 18 * s, a))

def mine(ctx, t, a=1.0, beam=None, crates=True):
    """Salt-mine tunnel receding into the dark. beam=(x,y) torch target."""
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy
    for k in range(7, -1, -1):
        s = .25 + k * .14; w = 900 * s; h = 760 * s; y0 = cy + 300 * s - 120
        P = skia.Path(); P.moveTo(cx - w / 2, y0 + h * .2); P.lineTo(cx - w / 2, y0 - h * .35)
        P.cubicTo(cx - w / 2, y0 - h * .85, cx + w / 2, y0 - h * .85, cx + w / 2, y0 - h * .35); P.lineTo(cx + w / 2, y0 + h * .2)
        c.drawPath(P, stroke("#6b6458", 26 * s, a * (.25 + .09 * k), cap=False))
    c.drawRect(skia.Rect.MakeLTRB(0, cy + 330, W, H), fill("#0b0b0e", a))
    if crates:
        rnd = random.Random(5)
        for k in range(9):
            x = 120 + k * 210 + rnd.uniform(-30, 30); s = rnd.uniform(.8, 1.15); y = cy + 340
            for j in range(rnd.randint(1, 3)):
                bw, bh = 180 * s, 120 * s; yy = y - (j + 1) * bh
                c.drawRect(skia.Rect.MakeXYWH(x - bw / 2, yy, bw, bh), fill("#2a2219", a)); c.drawRect(skia.Rect.MakeXYWH(x - bw / 2, yy, bw, bh), stroke("#4a3b28", 4, a, cap=False))
                c.drawLine(x - bw / 2, yy, x + bw / 2, yy + bh, stroke("#4a3b28", 3, a * .7, cap=False))
    if beam:
        bx, by = beam; P = skia.Path(); P.moveTo(W * .08, H * .95); P.lineTo(bx - 260, by - 220); P.lineTo(bx + 260, by + 220); P.close()
        c.drawPath(P, fill("#ffe2a0", .16 * a, 24)); c.drawCircle(bx, by, 330, fill("#ffe2a0", .12 * a, 90))

def oven(c, x, y, s=1.0, a=1.0, heat=0.0, temp=None):
    w, h = 520 * s, 420 * s
    c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2 + 10, y - h / 2 + 14, w, h), 18, 18, fill("#000000", .6 * a, 20))
    c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), 18, 18, fill("#3a3d48", a))
    c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2 + 40 * s, y - h / 2 + 90 * s, w - 80 * s, h - 140 * s), 10, 10, fill("#0d0e12", a))
    if heat > 0:
        c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2 + 40 * s, y - h / 2 + 90 * s, w - 80 * s, h - 140 * s), 10, 10, fill("#ff7a2a", .55 * heat * a, 18))
        for k in range(5): c.drawLine(x - w / 2 + 70 * s + k * 90 * s, y + h / 2 - 70 * s, x - w / 2 + 110 * s + k * 90 * s, y + h / 2 - 70 * s, stroke("#ffb35a", 8 * s, heat * a))
    for k in range(3): c.drawCircle(x - w / 2 + 80 * s + k * 70 * s, y - h / 2 + 45 * s, 18 * s, fill("#20222a", a))
    if temp is not None:
        text(c, f"{int(temp)}°C", x + w / 2 - 50 * s, y - h / 2 + 60 * s, 46 * s, "sansb", "#ffb35a", a, align="r")

def vial(c, x, y, s=1.0, a=1.0, fillc="#7fd1c7", level=.6):
    w, h = 70 * s, 240 * s
    P = skia.Path(); P.addRoundRect(skia.Rect.MakeXYWH(x - w / 2, y - h, w, h), w / 2, w / 2)
    c.save(); c.clipPath(P, True); c.drawRect(skia.Rect.MakeXYWH(x - w / 2, y - h * level, w, h * level), fill(fillc, .8 * a)); c.restore()
    c.drawPath(P, stroke("#d9e6ee", 5 * s, a)); c.drawRect(skia.Rect.MakeXYWH(x - w / 2 - 8 * s, y - h - 10 * s, w + 16 * s, 16 * s), fill("#d9e6ee", a))

def bar_chart(c, x, y, rows, p, w=900, row_h=86, a=1.0, hi=1):
    """rows = [(label, value 0..1)]; hi = index highlighted in gold."""
    for i, (lab, v) in enumerate(rows):
        yy = y + i * row_h; q = eo(seg(p, i * .12, i * .12 + .6))
        text(c, lab, x - 24, yy + row_h * .42, 34, "sansb", GOLD if i == hi else WHITE, a * seg(p, i * .12, i * .12 + .3), align="r")
        bar(c, x, yy + row_h * .1, w, row_h * .5, v * q, GOLD if i == hi else "#8a93ad", a)

def villa(c, x, y, s=1.0, a=1.0):
    c.drawRect(skia.Rect.MakeXYWH(x - 330 * s, y - 260 * s, 660 * s, 260 * s), fill("#e9dcc0", a))
    P = skia.Path(); P.moveTo(x - 370 * s, y - 260 * s); P.lineTo(x, y - 380 * s); P.lineTo(x + 370 * s, y - 260 * s); P.close(); c.drawPath(P, fill("#b9583a", a))
    for r in range(2):
        for k in range(6):
            c.drawRect(skia.Rect.MakeXYWH(x - 290 * s + k * 100 * s, y - 230 * s + r * 110 * s, 50 * s, 70 * s), fill("#2e4f8f" if (k + r) % 3 else "#ffcf7a", a))
    for k in (-1, 1): c.drawCircle(x + k * 420 * s, y - 120 * s, 70 * s, fill("#2f5a3a", a)); c.drawRect(skia.Rect.MakeXYWH(x + k * 420 * s - 8 * s, y - 70 * s, 16 * s, 70 * s), fill("#3a2a1a", a))


# ======================= added for 003, reusable =======================
def sea(ctx, t, y, a=1.0, color="#0b0e17", wave="#2c3550", n=5):
    c = ctx.c; W, H = ctx.W, ctx.H
    c.drawRect(skia.Rect.MakeLTRB(-400, y, W + 400, H + 400), fill(color, a))
    for j in range(n):
        P = skia.Path(); yy = y + 14 + j * 46
        for i in range(-400, int(W) + 440, 40):
            v = yy + math.sin(i * .012 + t * (1.2 + j * .2) + j) * (7 + j * 2)
            P.moveTo(i, v) if i == -400 else P.lineTo(i, v)
        c.drawPath(P, stroke(wave, 3, a * (.9 - j * .12)))

def sailship(c, x, y, s=1.0, a=1.0, t=0.0, color="#0c0d12", sail="#d8cdb4", flag=None, sails=1.0):
    """Three-masted sailing ship; (x, y) = waterline centre. flag: 'poyais' or None."""
    c.save(); c.translate(x, y + math.sin(t * 1.3) * 4 * s); c.rotate(math.sin(t * .9) * 1.2); c.scale(s, s)
    P = skia.Path(); P.moveTo(-260, -60); P.lineTo(250, -60); P.lineTo(300, -100); P.lineTo(200, 30); P.lineTo(-220, 30); P.lineTo(-280, -90); P.close()
    c.drawPath(P, fill(color, a))
    for k in range(9): c.drawRect(skia.Rect.MakeXYWH(-200 + k * 46, -46, 14, 10), fill(GOLD, .55 * a))
    for mx, mh in ((-130, 360), (20, 420), (160, 330)):
        c.drawRect(skia.Rect.MakeXYWH(mx - 5, -60 - mh, 10, mh), fill(color, a))
        if sails > 0:
            for j, (sw, sy) in enumerate(((150, .25), (125, .52), (95, .76))):
                yy = -60 - mh * (1 - sy) - 10; hh = mh * .2
                Q = skia.Path(); Q.moveTo(mx - sw / 2, yy - hh); Q.lineTo(mx + sw / 2, yy - hh)
                Q.quadTo(mx + sw / 2 + 14, yy - hh / 2, mx + sw / 2 - 4, yy); Q.lineTo(mx - sw / 2 + 4, yy); Q.quadTo(mx - sw / 2 + 14, yy - hh / 2, mx - sw / 2, yy - hh); Q.close()
                c.drawPath(Q, fill(sail, a * sails * .92))
    if flag == "poyais":
        fx, fy = 20, -60 - 420
        poyais_flag(c, fx + 4, fy, 90, a, t)
    c.restore()

def poyais_flag(c, x, y, w, a=1.0, t=0.0):
    """White field, green St George-style cross. (x, y) = top of pole side."""
    h = w * .62; P = skia.Path(); n = 12
    top = [(x + w * i / n, y + math.sin(t * 4 + i * .7) * w * .04 * i / n) for i in range(n + 1)]
    for i, (px, py) in enumerate(top): P.moveTo(px, py) if i == 0 else P.lineTo(px, py)
    for px, py in reversed(top): P.lineTo(px, py + h)
    P.close(); c.drawPath(P, fill("#f2efe6", a))
    c.save(); c.clipPath(P, True)
    c.drawRect(skia.Rect.MakeXYWH(x + w * .42, y - w, w * .16, h + 2 * w), fill("#2f7a45", a))
    c.drawRect(skia.Rect.MakeXYWH(x - 10, y + h * .4 + math.sin(t * 4 + 5) * w * .02, w + 20, h * .2), fill("#2f7a45", a))
    c.restore()

def palm(c, x, y, s=1.0, a=1.0, color="#07090d", t=0.0, lean=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    P = skia.Path(); P.moveTo(-12, 0); P.quadTo(20 + lean * 60, -200, 30 + lean * 120, -380); P.lineTo(46 + lean * 120, -378); P.quadTo(36 + lean * 60, -200, 12, 0); P.close()
    c.drawPath(P, fill(color, a)); hx, hy = 38 + lean * 120, -380
    for k in range(7):
        an = -math.pi / 2 + (k - 3) * .55 + math.sin(t * 1.5 + k) * .05
        L = skia.Path(); L.moveTo(hx, hy)
        ex, ey = hx + math.cos(an) * 190, hy + math.sin(an) * 70 + 90
        L.quadTo(hx + math.cos(an) * 110, hy + math.sin(an) * 110 - 30, ex, ey)
        L.quadTo(hx + math.cos(an) * 100, hy + math.sin(an) * 100 - 6, hx, hy + 8)
        c.drawPath(L, fill(color, a))
    c.restore()

def jungle(ctx, t, a=1.0, shore=.78, rain=0.0, dusk=False):
    """Swampy tropical shore: palms, undergrowth, still water. rain 0..1."""
    c = ctx.c; W, H = ctx.W, ctx.H; base = H * shore
    c.drawCircle(W * .78, H * .22, 260, fill("#c7d8a0" if not dusk else "#ffb45e", .06 * a, 90))
    rnd = random.Random(31)
    for k in range(22):
        x = rnd.uniform(-60, W + 60); r = rnd.uniform(90, 220)
        c.drawCircle(x, base - rnd.uniform(40, 160), r, fill("#0e1a14", a))
    for k in range(9):
        palm(c, -80 + k * 250 + rnd.uniform(-40, 40), base + 10, rnd.uniform(.8, 1.3), a, "#08110c", t, rnd.uniform(-.3, .3))
    c.drawRect(skia.Rect.MakeLTRB(0, base, W, H), fill("#0a0f0e", a))
    for j in range(4):
        c.drawLine(0, base + 30 + j * 50, W, base + 30 + j * 50, stroke("#1f3a33", 2, a * (.5 - j * .1), cap=False))
    if rain > 0:
        r2 = random.Random(7)
        for k in range(int(260 * rain)):
            x = r2.uniform(0, W + 300); sp = r2.uniform(900, 1400); y = (r2.uniform(0, H) + t * sp) % (H + 100) - 50
            c.drawLine(x - (y * .25), y, x - (y * .25) - 12, y + 40, stroke("#9fb4c8", 2, .35 * a * rain))

def city_mirage(c, cx, base, a=1.0, p=1.0, color=GOLD):
    """An imagined grand capital drawn in gold outline (St Joseph as advertised)."""
    if a <= 0: return
    st = stroke(color, 4, a * .9); gl = fill(color, .05 * a, 30)
    def r(x, y, w, h):
        c.drawRect(skia.Rect.MakeXYWH(cx + x, base - y - h, w, h), gl); c.drawRect(skia.Rect.MakeXYWH(cx + x, base - y - h, w, h), st)
    c.save(); c.clipRect(skia.Rect.MakeLTRB(cx - 1000, base - 700 * eo(p) - 20, cx + 1000, base + 4))
    r(-760, 0, 220, 160); r(-500, 0, 160, 230)
    r(-300, 0, 300, 220); c.drawArc(skia.Rect.MakeXYWH(cx - 250, base - 220 - 110, 200, 220), 180, 180, False, st)  # cathedral dome
    c.drawLine(cx - 150, base - 330, cx - 150, base - 390, st); c.drawLine(cx - 172, base - 368, cx - 128, base - 368, st)
    r(40, 0, 320, 200)                                                                                                     # opera house
    for k in range(6): c.drawLine(cx + 70 + k * 52, base - 20, cx + 70 + k * 52, base - 170, st)
    P = skia.Path(); P.moveTo(cx + 30, base - 200); P.lineTo(cx + 200, base - 270); P.lineTo(cx + 370, base - 200); c.drawPath(P, st)
    r(400, 0, 180, 260); r(620, 0, 160, 140)
    c.drawLine(cx - 900, base, cx + 900, base, st)
    c.restore()

def guidebook(c, x, y, w, rot=0, a=1.0, lines=("SKETCH OF THE", "MOSQUITO SHORE"), by="Capt. Thomas Strangeways", year="1822"):
    h = w * 1.42
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + 12, -h / 2 + 18, w, h), 8, 8, fill("#000000", .6 * a, 20))
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 8, 8, fill("#5a2a20", a))
    c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w * .06, h), fill("#3a1a14", a))
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + w * .12, -h / 2 + w * .1, w * .8, h - w * .2), 4, 4, stroke(GOLD, max(2, w * .008), a))
    for i, s in enumerate(lines): text(c, s, w * .03, -h * .22 + i * w * .11, w * .085, "serifb", GOLD, a)
    text(c, "including the territory of POYAIS", w * .03, -h * .22 + len(lines) * w * .11 + w * .02, w * .045, "serif", "#e9d29a", a)
    c.drawCircle(w * .03, h * .12, w * .12, stroke(GOLD, max(2, w * .01), a))
    text(c, "by " + by, w * .03, h * .33, w * .045, "serif", "#e9d29a", a)
    text(c, year, w * .03, h * .4, w * .045, "serifb", GOLD, a)
    c.restore()

def poyais_note(c, x, y, w, rot=0, a=1.0, amount="ONE", stamp_p=0.0):
    """Black-and-white engraved banknote (illustration of a Bank of Poyais dollar)."""
    h = w * .48
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + 6, -h / 2 + 9, w, h), 4, 4, fill("#000000", .5 * a, 10))
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 4, 4, fill("#efe8d6", a))
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + w * .03, -h / 2 + w * .03, w * .94, h - w * .06), 3, 3, stroke("#1d1a14", max(1, w * .008), a))
    for k in range(18): c.drawLine(-w / 2 + w * .05, -h / 2 + w * .05 + k * h * .045, -w / 2 + w * .2, -h / 2 + w * .05 + k * h * .045, stroke("#1d1a14", max(.6, w * .002), .35 * a))
    c.drawOval(skia.Rect.MakeXYWH(-w * .08, -h * .42, w * .16, h * .34), stroke("#1d1a14", max(1, w * .006), a))
    c.drawRect(skia.Rect.MakeXYWH(-w * .02, -h * .38, w * .04, h * .26), fill("#1d1a14", .8 * a))
    c.drawRect(skia.Rect.MakeXYWH(-w * .06, -h * .27, w * .12, h * .05), fill("#1d1a14", .8 * a))
    text(c, "BANK OF POYAIS", 0, h * .06, w * .075, "serifb", "#1d1a14", a)
    text(c, f"{amount} DOLLAR", 0, h * .2, w * .06, "serif", "#1d1a14", a)
    text(c, "St. Joseph", -w * .33, h * .36, w * .035, "serif", "#3b3324", a)
    text(c, "by order of his highness Gregor, Cazique", w * .14, h * .36, w * .03, "serif", "#3b3324", a)
    text(c, "1", -w * .4, -h * .22, w * .09, "serifb", "#1d1a14", a); text(c, "1", w * .4, -h * .22, w * .09, "serifb", "#1d1a14", a)
    if stamp_p > 0: stamp(c, "WORTHLESS", 0, 0, w * .11, stamp_p, rot=-10)
    c.restore()

def bond(c, x, y, w, rot=0, a=1.0, p=1.0, price=None):
    """Illustration of a Poyais government bond certificate."""
    h = w * .7; card(c, x, y, w, h, rot=rot, a=a, color="#efe3c4")
    c.drawRect(skia.Rect.MakeXYWH(w * .03, w * .03, w * .94, h - w * .06), stroke("#5a4320", w * .006, a, cap=False))
    c.drawRect(skia.Rect.MakeXYWH(w * .045, w * .045, w * .91, h - w * .09), stroke("#5a4320", w * .002, a, cap=False))
    text(c, "POYAISIAN GOVERNMENT", w / 2, h * .17, w * .055, "serifb", "#2a2216", a, spacing=w * .004)
    text(c, "LOAN OF £200,000 · 1822", w / 2, h * .26, w * .03, "serif", "#5a4d38", a, spacing=2)
    typed(c, "BOND FOR ONE HUNDRED POUNDS", w / 2, h * .42, w * .04, seg(p, 0, .35), "typeb", "#1d1a14", a, align="c")
    typed(c, "Interest: six per cent a year,", w / 2, h * .53, w * .034, seg(p, .3, .6), "type", "#1d1a14", a, align="c")
    typed(c, "on all the revenues of Poyais.", w / 2, h * .61, w * .034, seg(p, .5, .8), "type", "#1d1a14", a, align="c")
    if p > .8: text(c, "Gregor the First", w * .72, h * .82, w * .045, "serifb", "#1d1a14", a * seg(p, .8, 1))
    c.drawCircle(w * .2, h * .78, w * .07, fill(RED, .85 * a)); c.drawCircle(w * .2, h * .78, w * .05, stroke("#f0d9b0", 2, .7 * a))
    text(c, "ILLUSTRATION", w * .05, h - w * .05, w * .016, "sansb", "#8c7d60", a, align="l", spacing=2)
    if price is not None: chip(c, price, w * .78, h * .14, a=a, size=w * .04)
    c.restore()

def dots(c, x, y, n, cols, p_red, red_n, a=1.0, r=11, gap=30, home_n=0):
    """n people as dots in a grid; the first red_n go red (fading) as p_red runs 0..1."""
    for i in range(n):
        xx = x + (i % cols) * gap; yy = y + (i // cols) * gap
        q = seg(p_red, i / n * .8, i / n * .8 + .2) if i < red_n else 0
        c.drawCircle(xx, yy, r, fill(RED if q > 0 else WHITE, a * (1 - .65 * q)))
