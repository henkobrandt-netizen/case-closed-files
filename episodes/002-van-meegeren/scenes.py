from lib import *

HAN = GOLD          # van Meegeren's rim colour
COLD = "#8fa0c8"    # officials / experts
def beat(ctx, i):
    t, a, d = ctx.ph(i)
    if a > 0: ctx.layer(a)
    return t, a, d
def han(c, x, y, s, a=1.0, rim=HAN, bow=0.0): figure(c, x, y, s, a=a, hat=False, rim=rim, bow=bow)
def caption_line(c, s, x, y, a, size=46, color=WHITE, kind="serif"): text(c, s, x, y, size, kind, color, a)

# ------------------------------------------------------------------ cold open
def sc_cold(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        bx = lerp(cx - 500, cx + 420, eio(seg(t, .5, d)))
        mine(ctx, t, beam=(bx, cy + 60))
        label(c, "MAY 1945 · A SALT MINE, AUSTRIA", 120, 140, 30, seg(t, .2, 1.6), align="l")
        text(c, "THOUSANDS", W - 140, 200, 96, "disp", GOLD, ap(t, d * .45), align="r")
        text(c, "of looted works, hidden here", W - 140, 250, 30, "serif", WHITE, ap(t, d * .55) * .85, align="r")
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        mine(ctx, t, crates=True, beam=(cx, cy - 20))
        painting(c, cx, cy - 30, 560 * (1 + .04 * t / d), 460 * (1 + .04 * t / d), seed=3, glow=ap(t, .3, 1.5), reveal=1,
                 label="CHRIST AND THE ADULTERESS · “VERMEER”", lab_a=ap(t, d * .45))
        label(c, "THE PRIDE OF HERMANN GÖRING'S COLLECTION", cx, 120, 28, seg(t, d * .2, d * .2 + 1.5), WHITE)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        route(ctx, seg(t, .2, d * .55), "SALT MINE", "AMSTERDAM", sp=520)
        q = ap(t, d * .5, .8)
        han(c, cx + 640, H + 40 + (1 - q) * 120, 1.6, a=q)
        label(c, "HAN VAN MEEGEREN · PAINTER", cx + 520, 200, 26, seg(t, d * .6, d * .6 + 1), GOLD)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        han(c, cx, H + 50, 2.2, rim=RED)
        stamp(c, "TREASON?", cx - 460, cy - 230, 100, seg(t, .5, .85), rot=-8)
        stamp(c, "PENALTY: DEATH", cx + 430, cy - 150, 80, seg(t, d * .28, d * .28 + .35), rot=6)
        text(c, "“I painted it myself.”", cx, 140, 64, "serifb", GOLD, ap(t, d * .78, .6))
        c.restore()

def sc_title(ctx):
    c, cx, cy, t = ctx.c, ctx.cx, ctx.cy, ctx.t
    painting(c, cx, cy, 900, 700, a=.18, seed=3, frame=True)
    label(c, "CASE CLOSED FILES  ·  NO. 002", cx, cy - 190, 26, seg(t, .1, .7))
    text(c, "THE FORGER WHO", cx, cy - 40 + (1 - ap(t, .2, .6)) * 30, 128, "disp", WHITE, ap(t, .2, .6), spacing=4)
    text(c, "FOOLED THE NAZIS", cx, cy + 110 + (1 - ap(t, .5, .6)) * 30, 140, "disp", GOLD, ap(t, .5, .6), spacing=4)
    text(c, "A true story · Netherlands, 1932–1947", cx, cy + 220, 34, "serif", WHITE, ap(t, 1.0) * .8)

# ------------------------------------------------------------------ who
def sc_who(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        w, h = 1300, 620; card(c, cx, cy + (1 - ap(t, 0, .7)) * 80, w, h, rot=-1.0)
        text(c, "DOSSIER", 60, 80, 40, "sansb", INK, align="l", spacing=10); text(c, "FILE 002", w - 60, 80, 22, "type", "#5a4d38", align="r")
        c.drawLine(60, 104, w - 60, 104, stroke(INK, 2, cap=False))
        c.drawRect(skia.Rect.MakeXYWH(60, 140, 340, 420), fill("#1b1e29"))
        c.save(); c.clipRect(skia.Rect.MakeXYWH(60, 140, 340, 420)); han(c, 230, 590, 1.25, rim=GOLD); c.restore()
        rows = [("NAME", "Han van Meegeren", .8), ("BORN", "1889, Deventer, Netherlands", d * .3), ("TRADE", "Painter", d * .5), ("AMBITION", "To be called a great artist", d * .7)]
        for i, (k, v, ts) in enumerate(rows):
            y = 190 + i * 100
            text(c, k, 460, y, 18, "sansb", "#7a6a4c", ap(t, ts - .3), align="l", spacing=4)
            typed(c, v, 460, y + 44, 38, seg(t, ts, ts + .9), color="#1d1a14", cursor=True)
        c.restore(); c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        newspaper(ctx, cx - 280, cy + 30, 900, 760, -2, ["CRITICS: HE CAN", "ONLY COPY"], "A review of the painter's latest exhibition", "THE HAGUE · 1928", hp=seg(t, .2, d * .5))
        han(c, cx + 620, H + 40, 1.7, rim=COLD, bow=eo(seg(t, d * .5, d * .8)) * 1.2)
        stamp(c, "REJECTED", cx - 280, cy + 260, 96, seg(t, d * .62, d * .62 + .35), rot=-7)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        han(c, cx - 520, H + 40, 2.0, rim=GOLD)
        text(c, "“I'll make the experts", cx + 260, cy - 120, 64, "serifb", WHITE, ap(t, .3))
        text(c, "look like fools.”", cx + 260, cy - 30, 64, "serifb", WHITE, ap(t, .8))
        label(c, "HIS STORY, LATER", cx + 260, cy - 250, 24, seg(t, .1, 1.0), GOLD)
        stamp(c, "REMEMBER THIS", cx + 260, cy + 170, 74, seg(t, d * .62, d * .62 + .35), rot=-5, color="#e8b23a")
        c.restore()

# ------------------------------------------------------------------ method
def step_tag(c, n, s, x, y, p, a=1.0):
    if p <= 0: return
    c.drawCircle(x, y, 34, fill(GOLD, a * eo(p))); text(c, str(n), x, y + 13, 38, "sansb", INK, a * eo(p))
    text(c, s, x + 60, y + 14, 42, "sansb", WHITE, a * eo(p), align="l")

def sc_method(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        c.drawCircle(W * .78, H * .3, 220, fill("#ffcf7a", .12, 80)); c.drawCircle(W * .78, H * .3, 70, fill("#ffd48a", .9))
        villa(c, cx - 300, H * .8, 1.1)
        c.drawRect(skia.Rect.MakeLTRB(0, H * .8, W, H), fill("#0b1530"))
        label(c, "1932 · SOUTH OF FRANCE", 120, 140, 30, seg(t, .2, 1.4), align="l")
        text(c, "NEW", cx + 520, cy - 60, 90, "disp", WHITE, ap(t, d * .55))
        text(c, "→ 300 YEARS OLD?", cx + 520, cy + 40, 70, "disp", GOLD, ap(t, d * .7))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        painting(c, cx - 420, cy + 30, 620, 760, seed=7, reveal=1 - eo(seg(t, d * .12, d * .32)) if t < d * .34 else 0.0)
        x = cx + 80
        step_tag(c, 1, "Real 17th-century canvas", x, cy - 240, seg(t, .3, .9))
        step_tag(c, 2, "Scrape it back", x, cy - 150, seg(t, d * .2, d * .2 + .6))
        step_tag(c, 3, "Grind lapis lazuli + lead white", x, cy - 60, seg(t, d * .45, d * .45 + .6))
        step_tag(c, 4, "Badger-hair brushes, lilac oil", x, cy + 30, seg(t, d * .75, d * .75 + .6))
        for k, colr in enumerate(("#2e4f8f", "#efe9da", "#c8a23c")):
            q = seg(t, d * .5 + k * .3, d * .5 + k * .3 + .6)
            if q > 0: c.drawCircle(x + 120 + k * 150, cy + 200, 50 * back(q), fill(colr))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        x = cx - 420
        step_tag(c, 5, "Problem: new paint is soft", cx - 720, 160, seg(t, .2, .8))
        vial(c, x - 150, cy + 300, 1.6, level=.7, fillc="#e0a43a")
        label(c, "BAKELITE", x - 150, cy + 360, 30, seg(t, d * .6, d * .6 + .8), GOLD, rule=False)
        text(c, "An early plastic.", cx + 320, cy - 40, 64, "serifb", WHITE, ap(t, d * .62))
        text(c, "Mixed into the paint.", cx + 320, cy + 50, 52, "serif", GOLD, ap(t, d * .74))
        stamp(c, "MODERN", cx + 320, cy + 220, 80, seg(t, d * .85, d * .85 + .3), rot=-6)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        k1 = seg(t, d * .36, d * .42)
        oa = 1 - k1
        if oa > 0:
            c.saveLayerAlpha(None, int(255 * oa))
            oven(c, cx - 300, cy + 40, 1.4, heat=eo(seg(t, .3, 2)), temp=lerp(20, 110, eo(seg(t, .3, d * .3))))
            step_tag(c, 6, "Bake at about 110°C", cx + 200, cy - 100, seg(t, .2, .8))
            text(c, "The paint sets like stone.", cx + 200, cy, 44, "serif", GOLD, ap(t, d * .22), align="l")
            c.restore()
        if k1 > 0:
            c.saveLayerAlpha(None, int(255 * k1))
            painting(c, cx - 380, cy + 20, 620, 760, seed=7, crack=eo(seg(t, d * .45, d * .7)), ink=eo(seg(t, d * .75, d * .95)))
            step_tag(c, 7, "Roll it to crack it", cx + 80, cy - 100, seg(t, d * .44, d * .5))
            step_tag(c, 8, "Ink in the cracks = old dirt", cx + 80, cy, seg(t, d * .74, d * .8))
            text(c, "Three centuries, in a week.", cx + 80, cy + 150, 46, "serifb", GOLD, ap(t, d * .9), align="l")
            c.restore()
        c.restore()

# ------------------------------------------------------------------ target
def sc_target(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        label(c, "THE NAME: JOHANNES VERMEER", cx, 150, 32, seg(t, .2, 1.4))
        n = 0
        for r in range(3):
            for k in range(12):
                n += 1
                if n > 36: break
                q = seg(t, d * .25 + n * .05, d * .25 + n * .05 + .4)
                if q > 0: painting(c, cx - 770 + k * 140, cy - 120 + r * 170, 110, 140, a=q, seed=n)
        text(c, "fewer than forty known paintings", cx, cy + 390, 46, "serifb", GOLD, ap(t, d * .6))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        # timeline with a gap
        y = cy + 60
        c.drawLine(cx - 800, y, cx + 800, y, stroke("#8a93ad", 6))
        for k in range(10):
            x = cx - 300 + k * 110
            painting(c, x, y - 110, 90, 120, seed=k + 40, a=ap(t, .2 + k * .06))
        gx = cx - 600
        c.drawRoundRect(skia.Rect.MakeXYWH(gx - 160, y - 200, 320, 180), 12, 12, stroke(GOLD, 5, ap(t, d * .3)))
        text(c, "?", gx, y - 70, 130, "disp", GOLD, ap(t, d * .35))
        label(c, "AN EARLY RELIGIOUS PERIOD?", gx, y + 70, 26, seg(t, d * .45, d * .45 + 1), GOLD)
        figure(c, cx + 700, H + 40, 1.3, hat=False, rim=COLD, a=ap(t, .3))
        label(c, "ABRAHAM BREDIUS · EXPERT", cx + 600, y + 260, 22, seg(t, d * .2, d * .2 + 1), WHITE, rule=False)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        route(ctx, seg(t, .2, d * .5), "ITALY", "DELFT", sp=520)
        text(c, "Borrowed from Caravaggio", cx, 150, 54, "serifb", WHITE, ap(t, d * .3))
        text(c, "Every detail: a gift for the judges.", cx, H - 120, 46, "serif", GOLD, ap(t, d * .65))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        y = cy + 60
        c.drawLine(cx - 800, y, cx + 800, y, stroke("#8a93ad", 6))
        for k in range(10): painting(c, cx - 300 + k * 110, y - 110, 90, 120, seed=k + 40)
        gx = cx - 600; q = eo(seg(t, d * .3, d * .55))
        painting(c, gx, lerp(y - 600, y - 110, q), 300, 170, seed=11, a=q, glow=q)
        text(c, "He painted the missing one.", cx, 170, 64, "serifb", GOLD, ap(t, d * .5))
        c.restore()

# ------------------------------------------------------------------ emmaus
def sc_emmaus(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        painting(c, cx - 380, cy + 10, 760, 640, seed=11, reveal=eo(seg(t, .3, d * .5)), label="THE SUPPER AT EMMAUS", lab_a=ap(t, d * .3))
        x = cx + 220
        item(c, "PAINTED OVER A REAL 1600s CANVAS", x, cy - 160, 32, t, d * .3, color=WHITE)
        item(c, "“FROM AN OLD FAMILY ESTATE”", x, cy - 80, 32, t, d * .55, color=GOLD)
        item(c, "SHOWN TO THE TOP EXPERT · 1937", x, cy, 32, t, d * .78, color=WHITE)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        figure(c, cx - 420, H + 40, 2.0, hat=False, rim=COLD, bow=.6)
        n = int(82 * eo(seg(t, .3, 1.6)))
        text(c, str(n), cx + 360, cy, 260, "disp", GOLD, ap(t, .3))
        text(c, "years old. A lifetime of Dutch painting.", cx + 360, cy + 90, 40, "serif", WHITE, ap(t, d * .3))
        label(c, "ABRAHAM BREDIUS", cx + 360, cy - 230, 28, seg(t, .1, 1.0), WHITE)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        w, h = 1000, 640; card(c, cx, cy + 20, w, h, rot=1.0)
        text(c, "THE BURLINGTON MAGAZINE", w / 2, 90, 40, "serifb", INK, spacing=4); c.drawLine(80, 120, w - 80, 120, stroke(INK, 2, cap=False))
        text(c, "LONDON · 1937", w / 2, 160, 22, "serif", "#5a4d38", spacing=4)
        typed(c, "“the masterpiece of", w / 2, 300, 62, seg(t, d * .3, d * .55), "serifb", "#1d1a14", align="c")
        typed(c, "Johannes Vermeer of Delft”", w / 2, 390, 62, seg(t, d * .55, d * .8), "serifb", "#1d1a14", align="c")
        text(c, "— Abraham Bredius", w / 2, 480, 32, "serif", "#5a4d38", ap(t, d * .82))
        text(c, "ILLUSTRATION", 60, h - 30, 13, "sansb", "#8c7d60", align="l", spacing=3)
        c.restore(); c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        painting(c, cx - 420, cy + 10, 700, 600, seed=11)
        x = cx + 120
        text(c, "Heavy faces.", x, cy - 160, 54, "serifb", WHITE, ap(t, d * .15), align="l")
        text(c, "Closer to Caravaggio.", x, cy - 80, 54, "serifb", WHITE, ap(t, d * .3), align="l")
        text(c, "They weren't looking at the painting.", x, cy + 60, 40, "serif", GOLD, ap(t, d * .62), align="l")
        text(c, "They were looking at their theory.", x, cy + 120, 40, "serifb", GOLD, ap(t, d * .8), align="l")
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        v = int(520000 * eo(seg(t, .2, d * .3)))
        text(c, f"ƒ {v:,}", cx, 210, 120, "disp", GOLD, ap(t, .2))
        label(c, "GUILDERS · MUSEUM BOIJMANS, ROTTERDAM", cx, 290, 26, seg(t, d * .2, d * .2 + 1.2), WHITE)
        painting(c, cx, cy + 120, 420, 360, seed=11, glow=1)
        for k in range(9):
            q = seg(t, d * .4 + k * .15, d * .4 + k * .15 + .6)
            figure(c, cx - 820 + k * 205 + (k > 4) * 0, H + 160, .9, hat=k % 3 == 0, rim="#2b3044", a=q * .95)
        stamp(c, "FOOLED", cx + 520, cy + 40, 100, seg(t, d * .82, d * .82 + .35), rot=-8)
        c.restore()

# ------------------------------------------------------------------ money
def sc_money(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        for k in range(6): painting(c, cx - 750 + k * 300, cy - 200, 230, 280, seed=20 + k, a=ap(t, .2 + k * .35))
        label(c, "MORE FAKES · VERMEER · DE HOOGH", cx, 140, 28, seg(t, .1, 1.2))
        lo = 5.5 * eo(seg(t, d * .5, d * .8)); hi = 7.5 * eo(seg(t, d * .5, d * .8))
        text(c, f"ƒ {lo:.1f}M – {hi:.1f}M", cx, cy + 260, 110, "disp", GOLD, ap(t, d * .5))
        text(c, "estimated earnings", cx, cy + 330, 36, "serif", WHITE, ap(t, d * .6))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        k = seg(t, d * .52, d * .6)
        if k < 1:
            c.saveLayerAlpha(None, int(255 * (1 - k)))
            c.drawRect(skia.Rect.MakeLTRB(0, H * .78, W, H), fill("#0b1530")); villa(c, cx - 360, H * .8, 1.2)
            chip(c, "12 BEDROOMS · NICE", cx + 480, cy - 160, size=40)
            chip(c, "57 PROPERTIES", cx + 480, cy - 20, size=40, color="#9db58a") if t > d * .3 else None
            c.restore()
        if k > 0:
            c.saveLayerAlpha(None, int(255 * k))
            c.drawPaint(skia.Paint(Color=col(RED, .08 + .08 * math.sin(t * 6))))
            text(c, "1940", cx, cy - 40, 220, "disp", WHITE, ap(t, d * .6))
            label(c, "THE NETHERLANDS IS OCCUPIED", cx, cy + 80, 34, seg(t, d * .66, d * .66 + 1.2), "#f08a7c")
            c.restore()
        c.restore()

# ------------------------------------------------------------------ war
def sc_war(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        figure(c, cx + 480, H + 40, 2.0, hat=False, wide=1.35, rim=COLD)
        label(c, "HERMANN GÖRING", cx + 480, 200, 30, seg(t, .3, 1.3), WHITE)
        painting(c, cx - 420, cy, 420, 500, seed=3, a=.35 + .65 * ap(t, d * .5), glow=ap(t, d * .5))
        text(c, "WANTED: A VERMEER", cx - 420, cy - 320, 50, "sansb", GOLD, ap(t, d * .45))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        xl, xm, xr = cx - 640, cx, cx + 640
        han(c, xl, H + 40, 1.3, rim=GOLD); figure(c, xm, H + 40, 1.3, hat=True, rim="#9aa3b8"); figure(c, xr, H + 40, 1.5, hat=False, wide=1.35, rim=COLD)
        for x, s in ((xl, "VAN MEEGEREN"), (xm, "ALOIS MIEDL · DEALER"), (xr, "GÖRING")): label(c, s, x, cy - 30, 22, seg(t, .2, 1.2), WHITE, rule=False)
        q = seg(t, d * .15, d * .45)
        if q > 0: painting(c, lerp(xl, xr, eio(q)), cy - 250, 200, 240, seed=3, label=None)
        text(c, "ƒ 1,650,000", cx, 130, 80, "disp", GOLD, ap(t, d * .45))
        text(c, "his highest price ever", cx, 190, 32, "serif", WHITE, ap(t, d * .52))
        # 137 paintings flood back
        n = int(137 * eo(seg(t, d * .7, d * .97)))
        rnd = random.Random(8)
        for k in range(min(n, 60)):
            sx = lerp(xr, xl, (k / 60 + t * .1) % 1); sy = cy - 250 + rnd.uniform(-45, 45)
            painting(c, sx, sy, 70, 85, seed=k + 60, a=.9)
        if n: text(c, f"{n} looted paintings", cx, cy + 70, 56, "sansb", "#f08a7c", 1)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        k = seg(t, d * .4, d * .5)
        if k < 1:
            c.saveLayerAlpha(None, int(255 * (1 - k)))
            painting(c, cx, cy - 20, 520, 620, seed=3, glow=1)
            label(c, "GÖRING'S COUNTRY ESTATE", cx, 120, 28, seg(t, .2, 1.2))
            c.restore()
        if k > 0:
            c.saveLayerAlpha(None, int(255 * k)); mine(ctx, t, beam=(cx + 200, cy)); painting(c, cx + 200, cy, 300, 360, seed=3, a=.85)
            label(c, "BACK INTO THE SALT MINE", cx, 120, 28, seg(t, d * .5, d * .5 + 1.2)); c.restore()
        c.restore()

# ------------------------------------------------------------------ arrest
def sc_arrest(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        cal_w = 360
        for i, (day, txt, colr) in enumerate((("17", "PAINTING FOUND", GOLD), ("29", "ARREST · AMSTERDAM", RED))):
            q = ap(t, .3 + i * d * .45, .6); x = cx - 300 + i * 600
            c.drawRoundRect(skia.Rect.MakeXYWH(x - cal_w / 2, cy - 260, cal_w, 400), 20, 20, fill(PAPER, q))
            c.drawRoundRect(skia.Rect.MakeXYWH(x - cal_w / 2, cy - 260, cal_w, 90), 20, 20, fill(colr, q))
            text(c, "MAY 1945", x, cy - 200, 34, "sansb", WHITE, q, spacing=4)
            text(c, day, x, cy + 40, 200, "disp", INK, q)
            label(c, txt, x, cy + 230, 26, seg(t, .5 + i * d * .45, 1.5 + i * d * .45), colr, rule=False)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        han(c, cx, H + 50, 2.2, rim=RED)
        text(c, "Selling a national treasure to the enemy.", cx, 150, 52, "serifb", WHITE, ap(t, .2))
        stamp(c, "PENALTY: DEATH", cx, cy - 120, 110, seg(t, d * .6, d * .6 + .35), rot=-6)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        two(ctx, lrim=COLD, rrim=GOLD, bow=1 - eo(seg(t, d * .35, d * .55)))
        text(c, "Weeks of silence.", cx, 140, 46, "serif", WHITE, ap(t, .2) * (1 - seg(t, d * .35, d * .42)))
        text(c, "“Not a Vermeer.", cx, 140, 66, "serifb", GOLD, ap(t, d * .6))
        text(c, "I painted the picture.”", cx, 230, 66, "serifb", GOLD, ap(t, d * .78))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        two(ctx, lrim=COLD, rrim=GOLD)
        label(c, "ARRESTING OFFICER: JOOP PILLER · EX-RESISTANCE", cx, 130, 26, seg(t, .2, 1.4), WHITE, rule=False)
        bel = .1 + .1 * eo(seg(t, d * .2, d * .4))
        label(c, "HOW MANY BELIEVE HIM", cx, 230, 26, 1, RED, rule=False); bar(c, cx - 380, 262, 760, 26, bel, RED)
        text(c, "Europe's top experts said: genuine.", cx, H - 70, 44, "serif", WHITE, ap(t, d * .55))
        c.restore()

# ------------------------------------------------------------------ proof
def sc_proof(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        han(c, cx - 480, H + 40, 2.0, rim=GOLD)
        text(c, "“Give me a canvas.”", cx + 300, cy - 100, 70, "serifb", WHITE, ap(t, d * .3))
        text(c, "“I'll paint you a Vermeer.”", cx + 300, cy, 70, "serifb", GOLD, ap(t, d * .6))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        easel(c, cx - 200, H - 40, 1.05)
        painting(c, cx - 200, cy - 110, 520, 440, seed=31, reveal=eo(seg(t, d * .15, d * .95)))
        han(c, cx + 300, H + 60, 1.4, rim=GOLD)
        for k, x in enumerate((cx - 820, cx + 780)): figure(c, x, H + 40, 1.3, hat=True, rim="#2b3044")
        label(c, "UNDER GUARD · BEFORE WITNESSES", cx, 80, 26, seg(t, .2, 1.2))
        day = 1 + int(seg(t, d * .2, d * .95) * 50)
        text(c, f"DAY {day}", cx + 700, 200, 70, "disp", GOLD, ap(t, d * .2))
        label_plate(c, "JESUS AMONG THE DOCTORS", cx - 200, cy + 190, ap(t, d * .5))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        for k, (colr, lv) in enumerate((("#7fd1c7", .6), ("#e0a43a", .8), ("#c86d6d", .4))): vial(c, cx - 640 + k * 130, cy + 260, 1.3, level=lv, fillc=colr)
        label(c, "THE COREMANS COMMISSION", cx - 510, cy - 200, 26, seg(t, .2, 1.2), WHITE, rule=False)
        x = cx + 120
        text(c, "FOUND:", x, cy - 160, 40, "sansb", WHITE, ap(t, d * .25), align="l")
        solid_stamp(c, "BAKELITE", x + 330, cy - 40, 74, rot=-4) if t > d * .35 else None
        text(c, "a 20th-century plastic", x, cy + 80, 40, "serif", GOLD, ap(t, d * .45), align="l")
        item(c, "INK IN THE CRACKS", x + 40, cy + 170, 34, t, d * .68, ok=True)
        item(c, "PAINT NO SOLVENT CAN TOUCH", x + 40, cy + 240, 34, t, d * .8, ok=True)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        w, h = 1100, 560; card(c, cx, cy + 10, w, h, rot=-1.2)
        text(c, "CASE FILE · VAN MEEGEREN", w / 2, 90, 40, "serifb", INK, spacing=4); c.drawLine(80, 120, w - 80, 120, stroke(INK, 2, cap=False))
        text(c, "COLLABORATOR", w / 2, 260, 80, "sansb", "#1d1a14")
        if t > d * .35:
            q = eo(seg(t, d * .35, d * .55)); c.drawLine(w / 2 - 330, 235, w / 2 - 330 + 660 * q, 235, stroke(RED, 12))
        c.restore(); c.restore()
        stamp(c, "FORGER", cx + 40, cy + 120, 140, seg(t, d * .7, d * .7 + .35), rot=-8)
        c.restore()

# ------------------------------------------------------------------ hero
def sc_hero(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        newspaper(ctx, cx, cy + 30, 1200, 760, 1.5, ["THE MAN WHO", "FOOLED GÖRING"], "Painter traded fake paint for real masterpieces", "AMSTERDAM · 1945", hp=seg(t, .2, d * .5))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        label(c, "NATIONAL POLL · OCTOBER 1947", cx, 150, 30, seg(t, .1, 1.2))
        for i, (rk, who, colr) in enumerate((("1", "THE PRIME MINISTER", WHITE), ("2", "HAN VAN MEEGEREN", GOLD))):
            q = ap(t, d * (.25 + i * .3), .6); y = cy - 80 + i * 200
            c.drawRoundRect(skia.Rect.MakeXYWH(cx - 640, y - 90, 1280, 150), 20, 20, fill("#ffffff", .06 * q))
            text(c, rk, cx - 540, y + 30, 140, "disp", colr, q)
            text(c, who, cx - 420, y + 10, 64, "sansb", colr, q, align="l")
        text(c, "Most popular people in the Netherlands", cx, H - 110, 40, "serif", WHITE, ap(t, d * .8))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        k = seg(t, d * .5, d * .58)
        if k < 1:
            c.saveLayerAlpha(None, int(255 * (1 - k)))
            label(c, "29 OCTOBER 1947 · THE TRIAL", cx, 140, 30, seg(t, .1, 1.2))
            for i in range(7): figure(c, cx - 780 + i * 260, H + 140, .9, hat=True, rim="#2b3044")
            han(c, cx, cy + 260, 1.3, rim=GOLD)
            stamp(c, "GUILTY · FORGERY", cx - 420, cy - 230, 80, seg(t, d * .2, d * .2 + .35), rot=-6)
            stamp(c, "1 YEAR", cx + 450, cy - 180, 110, seg(t, d * .32, d * .32 + .35), rot=7, color="#e8b23a")
            c.restore()
        if k > 0:
            c.saveLayerAlpha(None, int(255 * k))
            c.drawCircle(cx, cy - 40, 420, fill("#ffcf7a", .08, 120))
            han(c, cx, H + 50, 2.0, rim=GOLD, bow=1.4)
            text(c, "30 DECEMBER 1947", cx, 150, 56, "disp", WHITE, ap(t, d * .62))
            label(c, "DIED BEFORE SERVING A DAY · A NATIONAL HERO", cx, 220, 26, seg(t, d * .75, d * .75 + 1.5), GOLD)
            c.restore()
        c.restore()

# ------------------------------------------------------------------ twist
def sc_twist(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        k = seg(t, d * .55, d * .63)
        if k < 1:
            c.saveLayerAlpha(None, int(255 * (1 - k)))
            han(c, cx - 520, H + 40, 2.0, rim=GOLD)
            item(c, "REVENGE ON THE CRITICS", cx - 40, cy - 100, 46, t, .6, ok=True)
            item(c, "FOOLED THE NAZIS ON PURPOSE", cx - 40, cy + 10, 46, t, d * .25, ok=True)
            label(c, "THE LEGEND", cx + 260, cy - 240, 26, seg(t, .1, 1.0))
            c.restore()
        if k > 0:
            c.saveLayerAlpha(None, int(255 * k))
            for i in range(4):
                card(c, cx - 300 + i * 200, cy + 40 - i * 30, 520, 360, rot=-6 + i * 4, a=1); text(c, "ARCHIVE", 260, 70, 26, "sansb", "#5a4d38", spacing=6); c.restore()
            label(c, "HISTORIAN JONATHAN LOPEZ", cx, 140, 30, seg(t, d * .6, d * .6 + 1.2), WHITE)
            text(c, "4 countries of archives", cx, H - 100, 50, "serifb", GOLD, ap(t, d * .78))
            c.restore()
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        w, h = 1300, 720; card(c, cx, cy + 20, w, h, rot=.8)
        text(c, "THE OTHER FILE", w / 2, 90, 46, "sansb", INK, spacing=8); c.drawLine(80, 120, w - 80, 120, stroke(INK, 2, cap=False))
        rows = [("Forged and sold fakes years before Emmaus", .05), ("1928: magazine attacking modern art", .18), ("Admired Hitler", .3),
                ("Art for the occupation regime", .45), ("Money to Nazi causes", .58), ("Sent Hitler a book of drawings", .7)]
        for i, (s, f) in enumerate(rows):
            y = 200 + i * 78; q = seg(t, d * f, d * f + .5)
            if q > 0:
                c.drawCircle(110, y - 12, 10, fill(RED, eo(q))); typed(c, s, 140, y, 38, q * 1.4, color="#1d1a14")
        if t > d * .74: text(c, "“To the beloved Führer”", w / 2 + 260, 680, 40, "serifb", RED, ap(t, d * .76))
        c.restore(); c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        k = seg(t, d * .42, d * .5)
        if k < 1:
            c.saveLayerAlpha(None, int(255 * (1 - k)))
            villa(c, cx - 420, H * .82, 1.0)
            for i in range(4): figure(c, cx + 300 + i * 170, H + 120, .8, hat=False, rim="#2b3044", bow=1.2)
            text(c, "Rich, while his neighbours went hungry.", cx, 150, 50, "serifb", WHITE, ap(t, .2))
            c.restore()
        if k > 0:
            c.saveLayerAlpha(None, int(255 * k))
            figure(c, cx, H + 40, 2.0, hat=False, wide=1.35, rim=COLD)
            text(c, "“Horrified to learn it was fake”?", cx, 150, 56, "serifb", WHITE, ap(t, d * .5))
            stamp(c, "DISPUTED", cx, cy - 60, 120, seg(t, d * .72, d * .72 + .35), rot=-7)
            c.restore()
        c.restore()

# ------------------------------------------------------------------ end
def sc_end(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        han(c, cx, H + 40, 2.1, rim=GOLD)
        text(c, "His greatest forgery", cx, 140, 70, "disp", WHITE, ap(t, .2))
        text(c, "wasn't a painting.", cx, 230, 70, "disp", GOLD, ap(t, d * .3))
        solid_stamp(c, "HIS LEGEND", cx, cy + 40, 90, rot=-6) if t > d * .6 else None
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        for i in range(7): figure(c, cx - 780 + i * 260, H + 120, 1.0, hat=i % 2 == 0, rim="#2b3044")
        painting(c, cx, cy - 100, 520, 440, seed=11, glow=1)
        text(c, "They saw what they wanted to see.", cx, H - 120, 54, "serifb", GOLD, ap(t, d * .5))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill("#2a2733", .7))
        c.drawRect(skia.Rect.MakeLTRB(0, H * .86, W, H), fill("#3a2a1f"))
        painting(c, cx, cy - 60, 640, 540, seed=11, glow=ap(t, .3, 1.5))
        if t > d * .5: label_plate(c, "HAN VAN MEEGEREN · THE SUPPER AT EMMAUS · 1936–37", cx, cy + 290, ap(t, d * .5), size=24)
        label(c, "MUSEUM BOIJMANS VAN BEUNINGEN · ROTTERDAM · TODAY", cx, 90, 24, seg(t, .2, 1.4), WHITE, rule=False)
        c.restore()

def sc_outro(ctx):
    c, cx, cy, t = ctx.c, ctx.cx, ctx.cy, ctx.t
    stamp(c, "CASE CLOSED", cx, cy - 110, 150, seg(t, .15, .45), rot=-5)
    label(c, "CASE CLOSED FILES", cx, cy + 110, 30, seg(t, .6, 1.4), GOLD)
    text(c, "New case every week. Subscribe so you don't miss it.", cx, cy + 210, 40, "serif", WHITE, ap(t, 1.1))

# ------------------------------------------------------------------ short (vertical)
def s_hook(ctx):
    c, cx, cy, t, d = ctx.c, ctx.cx, ctx.cy, ctx.t, ctx.dur
    painting(c, cx, cy - 400, 700, 560, seed=3, glow=1, reveal=eio(seg(t, 0, .8)))
    label(c, "1945", cx, 230, 60, seg(t, .1, .6))
    han(c, cx, cy + 560, 1.4, rim=RED)
    stamp(c, "DEATH PENALTY?", cx, cy - 10, 90, seg(t, d * .35, d * .35 + .3), rot=-5)

def s_proof(ctx):
    c, cx, cy, t, d = ctx.c, ctx.cx, ctx.cy, ctx.t, ctx.dur
    easel(c, cx, cy + 420, 1.2)
    painting(c, cx, cy - 400, 640, 560, seed=31, reveal=eo(seg(t, .3, d * .95)))
    figure(c, cx - 380, cy + 560, 1.0, hat=True, rim="#2b3044"); figure(c, cx + 380, cy + 560, 1.0, hat=True, rim="#2b3044")
    label(c, "UNDER GUARD", cx, 200, 40, seg(t, .1, .8))

def s_lab(ctx):
    c, cx, cy, t, d = ctx.c, ctx.cx, ctx.cy, ctx.t, ctx.dur
    for k, (colr, lv) in enumerate((("#7fd1c7", .6), ("#e0a43a", .8), ("#c86d6d", .4))): vial(c, cx - 200 + k * 200, cy - 80, 1.6, level=lv, fillc=colr)
    if t > d * .45: solid_stamp(c, "BAKELITE", cx, cy - 560, 110, rot=-5)
    label(c, "PLASTIC IN A “VERMEER”", cx, 200, 40, seg(t, .1, .8))

def s_hero(ctx):
    c, cx, cy, t, d = ctx.c, ctx.cx, ctx.cy, ctx.t, ctx.dur
    han(c, cx, cy + 560, 1.7, rim=GOLD)
    stamp(c, "TRAITOR", cx, cy - 560, 110, seg(t, .1, .4), rot=-6)
    if t > d * .35:
        c.drawLine(cx - 300, cy - 560, cx - 300 + 600 * eo(seg(t, d * .35, d * .5)), cy - 560, stroke(WHITE, 14))
    solid_stamp(c, "HERO", cx, cy - 320, 130, rot=4, color="#c79a2e", ink="#1d1a14") if t > d * .5 else None

def s_twist(ctx):
    c, cx, cy, t, d = ctx.c, ctx.cx, ctx.cy, ctx.t, ctx.dur
    painting(c, cx, cy - 380, 640, 560, seed=11, a=.35)
    han(c, cx, cy + 560, 1.7, rim=GOLD)
    text(c, "?", cx, cy - 300, 300, "disp", GOLD, ap(t, .3))
    label(c, "FULL CASE ON CASE CLOSED FILES", cx, 200, 30, seg(t, d * .5, d), WHITE)

SCENES = {k[3:] if k.startswith("sc_") else k: v for k, v in list(globals().items()) if k.startswith(("sc_", "s_")) and callable(v)}
HITS = [("cold", 3, .5, 0), ("cold", 3, 0, .28), ("who", 1, 0, .62), ("who", 2, 0, .62), ("method", 2, 0, .85),
        ("emmaus", 4, 0, .82), ("arrest", 1, 0, .6), ("proof", 3, 0, .7), ("hero", 2, 0, .2), ("hero", 2, 0, .32),
        ("twist", 2, 0, .72), ("outro", -1, .15, 0)]
SHORT_HITS = [("s_hook", -1, .2, 0), ("s_hook", -1, 0, .35), ("s_lab", -1, 0, .45), ("s_hero", -1, .1, 0), ("s_hero", -1, 0, .5)]
WARM = {}

THUMB_WORDS = [(["I PAINTED", "IT."], 112), (["PROVE", "IT."], 140), (["FOOLED", "GÖRING"], 112)]
def thumbnail(c, W, H, word):
    word, size = word
    sh = skia.GradientShader.MakeRadial(center=(W * .36, H * .5), radius=900, colors=[col("#3a3550"), col("#151827"), col("#07080b")], positions=[0, .5, 1])
    c.drawPaint(skia.Paint(Shader=sh))
    painting(c, W * .3, H * .52, 470, 560, seed=3, glow=1)
    solid_stamp(c, "FAKE", W * .3, H * .62, 110, rot=-12)
    figure(c, W * .8, H + 30, 1.55, hat=False, rim=GOLD)
    for i, ln in enumerate(word): big_word(c, ln, W * .76, H * .2 + i * size * 1.02, size, "#ffd36b")


# ---------------- shorts (60-90 s, 9:16) ----------------
from shorts import hook_card, cta_card
def _art(seed):
    def prop(c, cx, cy, t, d):
        painting(c, cx, cy + 190, 440, 340, a=.85 * eo(seg(t, 0, .8)), seed=seed, glow=.6)
    return prop
SCENES["hook_a"] = hook_card(["SOLD A FAKE", "TO THE NAZIS."], stamp_text="DEATH PENALTY?", prop=_art(3))
SCENES["hook_b"] = hook_card(["HOW TO FAKE", "A VERMEER"], stamp_text="STEP BY STEP", prop=_art(11), rim=GOLD)
SCENES["hook_c"] = hook_card(["NOBODY", "BELIEVED HIM."], stamp_text="PROVE IT", prop=_art(31))
SCENES["cta_a"] = cta_card("CASE 002 · THE FORGER", "PART 2 NEXT")
SCENES["cta_b"] = cta_card("CASE 002 · THE FORGER", "PART 3 NEXT")
SCENES["cta_c"] = cta_card("CASE 002 · THE FORGER", "FULL CASE")
SHORT_HITS += [("hook_a", -1, .15, .62), ("hook_b", -1, .15, .62), ("hook_c", -1, .15, .62)]
SHORT_VIEW = {}
