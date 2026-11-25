from lib import *

THIEF = GOLD        # Peruggia's rim colour
COP = "#8fa0c8"     # police / officials
PLUMB = "#7fb3c9"   # the plumber
GAP = (960, 410, 380, 540)   # where the portrait hangs on the gallery wall

def beat(ctx, i):
    t, a, d = ctx.ph(i)
    if a > 0: ctx.layer(a)
    return t, a, d
def xfade(c, k, draw_a, draw_b):
    if k < 1:
        c.saveLayerAlpha(None, int(255 * (1 - k))); draw_a(); c.restore()
    if k > 0:
        c.saveLayerAlpha(None, int(255 * k)); draw_b(); c.restore()
def hung(c, a=1.0):
    portrait(c, GAP[0], GAP[1], GAP[2] * .9, a=a, frame=True)
def panel(c, cx, cy, w, h, a=1.0):
    c.drawRoundRect(skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), 20, 20, fill("#0d1016", .92 * a))
    c.drawRoundRect(skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), 20, 20, stroke("#2e3446", 4, a))
def book(c, x, y, w, rot=0, a=1.0, year="1878", note="1 PARAGRAPH", hi=0.0):
    h = w * 1.4
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + 12, -h / 2 + 18, w, h), 8, 8, fill("#000000", .6 * a, 20))
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 8, 8, fill("#7a2a1e", a))
    c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w * .07, h), fill("#4a1a12", a))
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + w * .12, -h / 2 + w * .1, w * .78, h - w * .2), 4, 4, stroke(GOLD, max(2, w * .01), a))
    text(c, "PARIS", w * .03, -h * .2, w * .13, "serifb", GOLD, a)
    text(c, "and its environs", w * .03, -h * .2 + w * .1, w * .06, "serif", "#e9d29a", a)
    text(c, "TRAVEL GUIDE", w * .03, h * .05, w * .07, "sansb", "#e9d29a", a, spacing=3)
    text(c, year, w * .03, h * .3, w * .12, "serifb", GOLD, a)
    c.restore()
    if note: chip(c, note, x, y + h / 2 + 70, a=a * hi, size=34)
def stairs(ctx, a=1.0):
    c = ctx.c; W, H = ctx.W, ctx.H
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill("#14110f", a))
    for k in range(12):
        x0 = 80 + k * 110; y0 = 260 + k * 62
        c.drawRect(skia.Rect.MakeXYWH(x0, y0, 130, H), fill("#2a2420" if k % 2 else "#241f1b", a))
        c.drawLine(x0, y0, x0 + 130, y0, stroke("#4a4038", 4, a, cap=False))
    c.drawLine(60, 200, 1400, 960, stroke("#5a4a3a", 8, a))
    c.drawRect(skia.Rect.MakeLTRB(1360, 0, W, H), fill("#1c1814", a))
def bundle(c, x, y, w, rot=0, a=1.0, colr="#e8e2d2"):
    h = w * 1.45
    c.save(); c.translate(x, y); c.rotate(rot)
    c.drawRect(skia.Rect.MakeXYWH(-w / 2 + 8, -h / 2 + 12, w, h), fill("#000000", .5 * a, 14))
    c.drawRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), fill(colr, a))
    for k in range(4): c.drawLine(-w / 2, -h / 2 + h * (k + 1) / 5, w / 2, -h / 2 + h * (k + .6) / 5, stroke("#9c9482", 3, a * .6))
    c.restore()
def poster(c, x, y, w, rot=0, a=1.0, head="MISSING"):
    h = w * 1.4
    card(c, x, y, w, h, rot=rot, a=a, r=2)
    text(c, head, w / 2, h * .12, w * .13, "sansb", RED, a, spacing=3)
    portrait(c, w / 2, h * .5, w * .5, a=a)
    text(c, "REWARD", w / 2, h * .88, w * .1, "serifb", INK, a, spacing=4)
    text(c, "ILLUSTRATION", w / 2, h * .96, w * .04, "sansb", "#8c7d60", a, spacing=2)
    c.restore()
def letter_card(c, x, y, t, d, a=1.0, lines=(), sign="", w=760, h=620, rot=-1.5):
    card(c, x, y, w, h, rot=rot, a=a)
    tot = sum(len(b) for b in lines) + 1; done = 0; pp = seg(t, .3, d * .7) * tot
    for i, b in enumerate(lines):
        if b: typed(c, b, 70, 110 + i * 54, 34, clamp((pp - done) / len(b)), color="#1d1a14", a=a, cursor=True)
        done += len(b)
    if sign: text(c, sign, w - 90, h - 110, 52, "serif", "#2a2216", a * seg(t, d * .7, d * .8), align="r")
    text(c, "RECONSTRUCTION", 70, h - 36, 14, "sansb", "#8c7d60", a, align="l", spacing=3)
    c.restore()
def clock(c, x, y, r, hh, mm, a=1.0):
    c.drawCircle(x, y, r, fill("#e9dfc6", a)); c.drawCircle(x, y, r, stroke(GOLD, r * .08, a))
    for k in range(12):
        an = k * math.pi / 6; c.drawLine(x + math.sin(an) * r * .8, y - math.cos(an) * r * .8, x + math.sin(an) * r * .9, y - math.cos(an) * r * .9, stroke(INK, r * .04, a))
    am = mm / 60 * 2 * math.pi; ah = (hh % 12 + mm / 60) / 12 * 2 * math.pi
    c.drawLine(x, y, x + math.sin(ah) * r * .5, y - math.cos(ah) * r * .5, stroke(INK, r * .07, a))
    c.drawLine(x, y, x + math.sin(am) * r * .75, y - math.cos(am) * r * .75, stroke(INK, r * .045, a))
def room(ctx, a=1.0, night=0.0):
    """Peruggia's small rented room: window over roofs, bed, table."""
    c = ctx.c; W, H = ctx.W, ctx.H
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill("#1e1a16", a))
    c.drawRect(skia.Rect.MakeLTRB(0, H * .8, W, H), fill("#120f0c", a))
    wx, wy, ww, wh = 1300, 170, 380, 420
    c.drawRect(skia.Rect.MakeXYWH(wx, wy, ww, wh), fill("#2a3550" if night else "#5d6f8a", a))
    c.save(); c.clipRect(skia.Rect.MakeXYWH(wx, wy, ww, wh)); skyline(c, W, wy + wh - 20, 9, "#121620", a, 40, 160, -300, lit=.3 * night); c.restore()
    c.drawRect(skia.Rect.MakeXYWH(wx, wy, ww, wh), stroke("#3a2a1a", 16, a, cap=False))
    c.drawLine(wx + ww / 2, wy, wx + ww / 2, wy + wh, stroke("#3a2a1a", 10, a)); c.drawLine(wx, wy + wh / 2, wx + ww, wy + wh / 2, stroke("#3a2a1a", 10, a))
    c.drawRect(skia.Rect.MakeXYWH(140, H * .62, 520, 90), fill("#2c2620", a)); c.drawRect(skia.Rect.MakeXYWH(140, H * .55, 90, 70), fill("#d8cdb4", a * .6))
    c.drawRect(skia.Rect.MakeXYWH(140, H * .7, 20, H * .1), fill("#2c2620", a)); c.drawRect(skia.Rect.MakeXYWH(640, H * .7, 20, H * .1), fill("#2c2620", a))
def stamp_on(c, s, x, y, size, p, rot=-8, color=RED): stamp(c, s, x, y, size, p, rot=rot, color=color)

# ------------------------------------------------------------------ cold open
def sc_cold(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        q = seg(t, d * .55, d * .75)
        gallery_wall(ctx, gap=GAP, hang=(lambda c: hung(c, 1 - q)) if q < 1 else None)
        easel(c, 360, H * .9, .55)
        person(c, 230 + 120 * eo(seg(t, 0, d * .4)), H * .95, 340, rim=WHITE, step=t * .8 if t < d * .4 else 0)
        label(c, "TUESDAY 22 AUGUST 1911 · THE LOUVRE, PARIS", cx, 70, 28, seg(t, .2, 1.6))
        chip(c, "AROUND NOON · THE SALON CARRÉ", cx, H - 60, a=ap(t, d * .3), size=34)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill("#3a2420"))
        hooks(c, cx, cy - 20, 560, 760, a=ap(t, .1))
        text(c, "a bare patch of wall", cx - 620, cy - 40, 50, "serifb", WHITE, ap(t, d * .2))
        text(c, "4 iron hooks", cx + 620, cy - 40, 58, "disp", GOLD, ap(t, d * .55))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        figure(c, cx - 520, H + 40, 1.5, hat=True, rim=COP, a=ap(t, .1))
        label(c, "THE GUARD", cx - 520, 180, 28, seg(t, .1, 1.2), COP)
        panel(c, cx + 300, cy, 860, 520, ap(t, .2))
        text(c, "Taken to be photographed?", cx + 300, cy - 170, 44, "serifb", WHITE, ap(t, d * .25))
        item(c, "PHOTO STUDIO", cx + 60, cy - 30, 48, t, d * .5, ok=False)
        item(c, "CLEANING ROOM", cx + 60, cy + 70, 48, t, d * .65, ok=False)
        item(c, "ANYWHERE", cx + 60, cy + 170, 48, t, d * .8, ok=False)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill("#3a2420", .6))
        hooks(c, cx, cy - 60, 380, 540, a=.8)
        P = skia.Path(); P.addRect(skia.Rect.MakeXYWH(cx - 190, cy - 330, 380, 540))
        c.drawPath(P, skia.Paint(Color=col(GOLD, .7), Style=skia.Paint.kStroke_Style, StrokeWidth=4, PathEffect=skia.DashPathEffect.Make([18, 12], t * 20), AntiAlias=True))
        text(c, "GONE FOR MORE THAN A DAY", cx, 120, 56, "disp", WHITE, ap(t, .2))
        text(c, "and nobody noticed", cx, 190, 40, "serif", WHITE, ap(t, d * .15) * .85)
        text(c, "WHO? HOW?", cx, H - 70, 76, "disp", GOLD, ap(t, d * .5))
        stamp(c, "MISSING", cx, cy - 60, 90, seg(t, d * .3, d * .3 + .35), rot=-8)
        c.restore()

def sc_title(ctx):
    c, cx, cy, t = ctx.c, ctx.cx, ctx.cy, ctx.t
    c.drawCircle(cx, cy - 20, 420, fill("#ffcf7a", .05, 120))
    hooks(c, cx, cy - 300, 120, 90, a=ap(t, .1, .6), patch=False)
    label(c, "CASE CLOSED FILES  ·  NO. 005", cx, cy - 170, 26, seg(t, .1, .7))
    text(c, "THE SMILE", cx, cy - 20 + (1 - ap(t, .2, .6)) * 30, 128, "disp", WHITE, ap(t, .2, .6), spacing=4)
    text(c, "THAT VANISHED", cx, cy + 130 + (1 - ap(t, .5, .6)) * 30, 140, "disp", GOLD, ap(t, .5, .6), spacing=4)
    text(c, "A true story · Paris, 1911–1914", cx, cy + 240, 34, "serif", WHITE, ap(t, 1.0) * .8)

# ------------------------------------------------------------------ the Louvre, 1910
def sc_louvre(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        portrait(c, cx - 460, cy + 30, 360, frame=True, a=ap(t, .1), label="ILLUSTRATION")
        label(c, "1911", cx + 300, 220, 40, seg(t, .1, 1))
        text(c, "The most famous", cx + 300, 380, 60, "serifb", WHITE, ap(t, d * .3))
        text(c, "painting in the world?", cx + 300, 460, 60, "serifb", WHITE, ap(t, d * .35))
        stamp(c, "NOT YET", cx + 300, 650, 100, seg(t, d * .7, d * .7 + .35), rot=-7)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        book(c, cx - 380, cy - 40, 300, rot=-4, a=ap(t, .1), year="1878", note="ONE PARAGRAPH", hi=ap(t, d * .25))
        book(c, cx + 380, cy - 40, 300, rot=4, a=ap(t, d * .4), year="1907", note="TWO SENTENCES", hi=ap(t, d * .55))
        text(c, "Admired by experts. Not a household name.", cx, H - 50, 44, "serifb", GOLD, ap(t, d * .8))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        louvre(ctx, lit=.25)
        label(c, "THE LOUVRE · PARIS", cx, 90, 30, seg(t, .1, 1.3))
        stats = (("1,000+", "ROOMS", WHITE), ("45", "ACRES", WHITE), ("~250,000", "OBJECTS", WHITE), ("< 150", "GUARDS", RED))
        for i, (n, l, colr) in enumerate(stats):
            x = cx - 690 + i * 460; q = ap(t, .3 + i * d * .2)
            text(c, n, x, 260, 80, "disp", GOLD if colr == WHITE else RED, q)
            text(c, l, x, 320, 32, "sansb", colr, q, spacing=4)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        label(c, "1910 · AFTER A THREAT", cx, 100, 30, seg(t, .1, 1.3))
        for i in range(3):
            x = cx - 560 + i * 560; q = ap(t, .2 + i * .3)
            painting(c, x, cy - 20, 300, 380, a=q, seed=i + 2)
            glass_case(c, x, cy - 20, 320, 400, a=q, t=t, open_=1 - eo(seg(t, d * .25 + i * .4, d * .5 + i * .4)))
        text(c, "The best pictures go behind glass.", cx, H - 120, 50, "serifb", WHITE, ap(t, d * .5))
        chip(c, "A FIRM OF GLAZIERS IS HIRED", cx, H - 50, a=ap(t, d * .75), size=32)
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        door(c, cx + 260, H * .9, 300, 560, open_=.85, lit=1)
        person(c, cx + 520, H * .9, 360, rim=PLUMB, a=ap(t, d * .45))
        smock_man(c, cx - 300 + 300 * eo(seg(t, .2, d * .5)), H * .9, 360, carry=1, step=t * .9)
        text(c, "a stranger holds the door", cx, 140, 56, "serifb", WHITE, ap(t, d * .35))
        stamp(c, "REMEMBER THIS", cx - 520, 330, 66, seg(t, d * .72, d * .72 + .35), rot=-6, color="#e8b23a")
        c.restore()

# ------------------------------------------------------------------ the workman
def sc_worker(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        route(ctx, seg(t, d * .35, d * .85), "ITALY", "PARIS", sp=520)
        label(c, "A VILLAGE NEAR THE SWISS BORDER", cx - 520, cy + 200, 24, seg(t, .2, 1.4), WHITE, rule=False)
        text(c, "1908", cx + 520, cy - 160, 70, "disp", GOLD, ap(t, d * .75))
        chip(c, "PAINTER & DECORATOR · ABOUT 30", cx, H - 70, a=ap(t, d * .5), size=34)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        smock_man(c, cx - 450, H * .92, 520, a=ap(t, .1))
        for k in range(6):
            yy = H * .92 - k * 104
            c.drawLine(cx - 700, yy, cx - 660, yy, stroke(GOLD, 3, ap(t, .3)))
        text(c, "5 ft 3", cx - 720, H * .92 - 540, 40, "sansb", GOLD, ap(t, .5), align="r")
        ctx.layer(ap(t, d * .25)); card(c, cx + 340, cy, 720, 520, rot=1.5)
        text(c, "POLICE RECORD", 360, 80, 40, "typeb", INK, ap(t, d * .25))
        typed(c, "- a night in jail", 60, 200, 38, seg(t, d * .4, d * .55), color="#1d1a14")
        typed(c, "- a fine for carrying a gun", 60, 270, 38, seg(t, d * .58, d * .75), color="#1d1a14")
        typed(c, "small things", 60, 380, 38, seg(t, d * .8, d * .9), kind="typeb", color=RED)
        text(c, "RECONSTRUCTION", 60, 490, 14, "sansb", "#8c7d60", 1, align="l", spacing=3)
        c.restore(); c.restore()
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        portrait(c, cx + 250, cy - 20, 330, a=ap(t, .1))
        glass_case(c, cx + 250, cy - 20, 360, 520, a=ap(t, .1), t=t, open_=1 - eo(seg(t, d * .3, d * .7)))
        smock_man(c, cx - 380, H * .95, 420, a=ap(t, .2))
        wrench(c, cx - 300, H * .95 - 260, 1.2, rot=30, a=ap(t, .4), color="#b9a27a")
        text(c, "He helped build the glass cases", cx, 110, 50, "serifb", WHITE, ap(t, d * .2))
        text(c, "including hers, by most accounts", cx, 175, 34, "serif", GOLD, ap(t, d * .55))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        panel(c, cx, cy, 1340, 620)
        label(c, "WHAT HE KNEW", cx, cy - 230, 30, seg(t, .1, 1))
        for i, s in enumerate(("THE ROOMS", "THE GUARDS", "WHICH DAYS IT WAS EMPTY", "HOW THE GLASS BOX CAME APART")):
            item(c, s, cx - 500, cy - 110 + i * 100, 48, t, .3 + i * d * .2, ok=True, color=GOLD if i == 3 else WHITE)
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        louvre(ctx, lit=.15)
        portrait(c, cx, cy - 120, 180, a=ap(t, .1), frame=True)
        text(c, "Off the wall: easy.", cx, 120, 52, "serifb", WHITE, ap(t, d * .2))
        text(c, "Out of the Louvre?", cx, 190, 60, "disp", GOLD, ap(t, d * .55))
        c.restore()

# ------------------------------------------------------------------ Monday morning
def sc_monday(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        louvre(ctx, lit=.05)
        label(c, "MONDAY 21 AUGUST 1911", cx, 90, 32, seg(t, .1, 1.2))
        stamp(c, "CLOSED TO THE PUBLIC", cx, 250, 64, seg(t, d * .25, d * .25 + .35), rot=-4)
        for i in range(4): smock_man(c, cx - 600 + i * 360 + t * 25, H * .98, 260, a=ap(t, d * .45 + i * .2) * .9, step=t * .7 + i * .3)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        label(c, "ACCOUNTS DIFFER", cx, 80, 32, seg(t, .1, 1.1), RED)
        panel(c, cx - 470, cy + 40, 820, 760, ap(t, .2))
        panel(c, cx + 470, cy + 40, 820, 760, ap(t, d * .45))
        text(c, "Hid overnight in a storeroom", cx - 470, 260, 40, "serifb", WHITE, ap(t, .4))
        text(c, "two brothers helped (some say)", cx - 470, 310, 30, "serif", GOLD, ap(t, d * .25))
        for i in range(3): smock_man(c, cx - 640 + i * 170, H * .86, 300, a=ap(t, .6 + i * .2) * (1 if i == 1 else .75), rim=GOLD if i == 1 else "#3a4055")
        text(c, "His own account", cx + 470, 260, 40, "serifb", WHITE, ap(t, d * .5))
        text(c, "walked in at 7 a.m., the workmen's door", cx + 470, 310, 30, "serif", GOLD, ap(t, d * .58))
        clock(c, cx + 300, cy + 150, 130, 7, 0, ap(t, d * .62))
        smock_man(c, cx + 640, H * .86, 300, a=ap(t, d * .68))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        lift = eo(seg(t, d * .3, d * .6)); away = eo(seg(t, d * .6, d * .95))
        gallery_wall(ctx, gap=GAP)
        px = GAP[0] + lift * 120 + away * 900; py = GAP[1] + lift * 160
        portrait(c, px, py, GAP[2] * .9, frame=True)
        smock_man(c, GAP[0] + 330 + away * 900, H * .97, 440, step=t * .8 * (away > 0))
        clock(c, 170, 170, 90, 7, 10 + 10 * seg(t, 0, d), .95)
        label(c, "THE SALON CARRÉ · EMPTY", cx, 1030, 26, seg(t, .1, 1.2), WHITE)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        pw = 300; ph = pw * 1.45
        portrait(c, cx - 150, cy + 10, pw, a=ap(t, .1))
        c.drawLine(cx - 150 - pw / 2 - 50, cy + 10 - ph / 2, cx - 150 - pw / 2 - 50, cy + 10 + ph / 2, stroke(GOLD, 4, ap(t, .5)))
        text(c, "77 cm", cx - 150 - pw / 2 - 70, cy + 20, 40, "sansb", GOLD, ap(t, .6), align="r")
        c.drawLine(cx - 150 - pw / 2, cy + 10 + ph / 2 + 40, cx - 150 + pw / 2, cy + 10 + ph / 2 + 40, stroke(GOLD, 4, ap(t, .9)))
        text(c, "53 cm", cx - 150, cy + 10 + ph / 2 + 90, 40, "sansb", GOLD, ap(t, 1.0))
        smock_man(c, cx + 300, H * .95, 640, a=ap(t, d * .4))
        text(c, "painted on a panel of wood", cx - 150, 110, 44, "serifb", WHITE, ap(t, d * .3))
        text(c, "small enough to carry", cx + 520, 300, 40, "serif", WHITE, ap(t, d * .6))
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        stairs(ctx)
        glass_case(c, 560, 470, 260, 360, t=t, open_=eo(seg(t, d * .1, d * .35)))
        c.save(); c.translate(560, 470); c.rotate(-8 * seg(t, d * .35, d * .55))
        c.drawRect(skia.Rect.MakeXYWH(-140, -190, 280, 380), stroke("#c9a24a", 22, 1 - .0, cap=False)); c.restore()
        q = seg(t, d * .45, d * .7)
        xfade(c, q, lambda: portrait(c, 900, 620, 220), lambda: bundle(c, 900, 620, 220, rot=6))
        label(c, "SERVICE STAIRWELL", 1640, 140, 26, seg(t, .1, 1.2), WHITE, rule=False)
        text(c, "case + frame", 560, 760, 38, "sansb", GOLD, ap(t, d * .4))
        text(c, "left on the steps", 560, 810, 34, "serif", WHITE, ap(t, d * .45))
        text(c, "wrapped in a white sheet", 1640, 900, 36, "serif", WHITE, ap(t, d * .75))
        door(c, 1640, 760, 220, 420, a=ap(t, d * .8))
        c.restore()

# ------------------------------------------------------------------ the plumber
def sc_plumber(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        door(c, cx, H * .95, 420, 760)
        c.drawCircle(cx + 160, H * .95 - 365, 40, fill(GOLD, .25 * ap(t, .2), 16))
        text(c, "LOCKED.", cx, 140, 110, "disp", RED, ap(t, .2))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        kp = 1 - seg(t, d * .25, d * .75)
        door(c, cx + 250, H * .95, 400, 720, knob=max(.3, kp))
        person(c, cx + 220, H * .95, 330, rim=THIEF, crouch=.6, arms=.8)
        bundle(c, cx - 520, H * .95 - 220, 260, rot=-6)
        text(c, "No key.", cx - 520, 140, 60, "disp", WHITE, ap(t, .2))
        text(c, "He starts taking the doorknob apart.", cx - 520, 220, 34, "serif", GOLD, ap(t, d * .2))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        stairs(ctx)
        k = eo(seg(t, d * .2, d * .9))
        person(c, lerp(260, 820, k), lerp(330, 680, k) + 120, 300, rim=PLUMB, step=t * 1.2)
        wrench(c, lerp(260, 820, k) + 50, lerp(330, 680, k) - 10, 1.0, rot=-20)
        label(c, "FOOTSTEPS", 1640, 160, 30, seg(t, .1, 1), WHITE, rule=False)
        chip(c, "A LOUVRE PLUMBER", 1640, 300, a=ap(t, d * .5), size=36, color=PLUMB)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        op = eo(seg(t, d * .6, d * .9))
        door(c, cx + 280, H * .95, 400, 720, open_=op)
        smock_man(c, cx - 120, H * .95, 380)
        person(c, cx - 420, H * .95, 380, rim=PLUMB, arms=.6 * op)
        wrench(c, cx - 380, H * .95 - 170, 1.0, rot=40)
        chip(c, "ONE OF THE STAFF, SURELY", cx - 270, 170, a=ap(t, d * .2), size=36, color=PLUMB)
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        louvre(ctx, lit=.1)
        k = eo(seg(t, .2, d))
        smock_man(c, lerp(cx - 400, cx + 700, k), H * .95, 380, carry=1, step=t * .9)
        text(c, "“Thank you.”", cx - 500, 160, 60, "serifb", WHITE, ap(t, .2))
        text(c, "Out into Paris.", cx + 380, 160, 60, "disp", GOLD, ap(t, d * .55))
        c.restore()

# ------------------------------------------------------------------ gone
def sc_gone(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        gallery_wall(ctx, gap=GAP)
        chip(c, "OUT FOR CLEANING?", cx - 520, H - 80, a=ap(t, d * .3), size=34)
        chip(c, "BEING PHOTOGRAPHED?", cx + 500, H - 80, a=ap(t, d * .5), size=34)
        clock(c, 170, 170, 90, 9 + t * 1.5, (t * 90) % 60, .95)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        label(c, "TUESDAY · MORE THAN 24 HOURS LATER", cx, 120, 30, seg(t, .1, 1.3))
        text(c, "“The Mona Lisa", cx, cy - 20, 110, "disp", WHITE, ap(t, d * .5))
        text(c, "is gone.”", cx, cy + 110, 110, "disp", GOLD, ap(t, d * .58))
        text(c, "a museum official, that evening", cx, cy + 200, 34, "serif", WHITE, ap(t, d * .65) * .8)
        figure(c, cx + 700, H + 40, 1.2, hat=True, rim=COP, a=ap(t, d * .5))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        louvre(ctx, lit=0)
        stamp(c, "CLOSED · ONE WEEK", cx, 170, 70, seg(t, .2, .55), rot=-5)
        crowd(c, cx - 360, H + 60, n=6, s=.75, spread=150, rim=COP, t=t, a=ap(t, d * .2))
        label(c, "DOZENS OF POLICE", cx - 360, 890, 26, seg(t, d * .2, d * .2 + 1), COP)
        glass_case(c, cx + 560, cy + 40, 200, 280, a=ap(t, d * .4), t=t, open_=.0)
        text(c, "found on the stairs", cx + 560, cy + 240, 34, "serif", WHITE, ap(t, d * .5))
        text(c, "“two or three days”", cx, H - 60, 52, "serifb", GOLD, ap(t, d * .75))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        for i in range(5): poster(c, 220 + i * 370, 330 + (i % 2) * 40, 250, rot=(-4, 3, -2, 5, -3)[i], a=ap(t, .1 + i * .15))
        newspaper(ctx, cx, 860, 900, 520, -2, ["MONA LISA", "STOLEN"], "The Louvre's famous portrait vanishes", "THE MORNING EDITION", a=ap(t, d * .45), hp=seg(t, d * .45, d * .7))
        c.restore()

# ------------------------------------------------------------------ the empty wall
def sc_empty(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        gallery_wall(ctx, gap=GAP)
        crowd(c, cx, H + 60, n=9, s=.9, spread=200, t=t, a=ap(t, d * .3))
        label(c, "THE LOUVRE REOPENS", cx, 70, 30, seg(t, .1, 1.2))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill("#3a2420"))
        hooks(c, cx, cy - 120, 380, 540)
        crowd(c, cx, H + 80, n=8, s=1.1, spread=240, t=t)
        text(c, "Thousands came to see", cx - 620, 300, 44, "serifb", WHITE, ap(t, .3))
        text(c, "nothing.", cx - 620, 370, 60, "disp", GOLD, ap(t, d * .3))
        chip(c, "FRANZ KAFKA CAME TOO", cx + 600, 330, a=ap(t, d * .65), size=34)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        for i, (hd, sub) in enumerate((("WHERE IS", "SHE?"), ("THE EMPTY", "WALL"), ("COME BACK,", "MONA LISA"))):
            card(c, (420, 600, 400)[i], (240, 530, 820)[i], 420, 260, rot=(-6, 3, -2)[i], a=ap(t, .1 + i * .3))
            text(c, hd, 210, 110, 44, "serifb", INK, 1); text(c, sub, 210, 170, 50, "disp", RED, 1)
            text(c, "POSTCARD · ILLUSTRATION", 210, 250, 14, "sansb", "#8c7d60", 1, spacing=3); c.restore()
        for i, s in enumerate(("AN AMERICAN MILLIONAIRE?", "THE GERMANS?", "BRAZIL? RUSSIA? JAPAN?")):
            chip(c, s, cx + 520, 330 + i * 160, a=ap(t, d * .4 + i * d * .15), size=36, color=(GOLD, GOLD, "#c9a56a")[i])
        label(c, "RUMOURS", cx + 520, 200, 30, seg(t, d * .35, d * .35 + 1))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        figure(c, cx - 430, H + 40, 1.4, hat=False, rim="#b8c4e0", a=ap(t, .1))
        figure(c, cx + 430, H + 40, 1.4, hat=False, rim="#e0b8b8", a=ap(t, d * .3))
        label(c, "GUILLAUME APOLLINAIRE · POET", cx - 430, 140, 26, seg(t, .1, 1.3), WHITE)
        label(c, "PABLO PICASSO · PAINTER", cx + 430, 140, 26, seg(t, d * .3, d * .3 + 1.3), WHITE)
        stamp(c, "ARRESTED", cx - 430, 300, 60, seg(t, d * .15, d * .15 + .35), rot=-6)
        stamp(c, "QUESTIONED", cx + 430, 300, 60, seg(t, d * .4, d * .4 + .35), rot=5, color="#e8b23a")
        chip(c, "BOTH LET GO · NOTHING TO DO WITH IT", cx, H - 70, a=ap(t, d * .75), size=36, color="#9db58a")
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        portrait(c, cx, cy - 10, 340, a=ap(t, .1) * .5, frame=True, glow=1)
        P = skia.Path(); P.addRect(skia.Rect.MakeXYWH(cx - 200, cy - 280, 400, 540))
        text(c, "everybody knew her now", cx - 560, cy, 44, "serifb", WHITE, ap(t, d * .2))
        text(c, "But where was she?", cx + 560, cy, 52, "disp", GOLD, ap(t, d * .65))
        c.restore()

# ------------------------------------------------------------------ the room
def peruggia(c, x, y, s, a=1.0, bow=0.0): figure(c, x, y, s, a=a, hat=False, rim=THIEF, bow=bow)
def _bundle_in(c, x, y, w, h):
    c.drawRect(skia.Rect.MakeXYWH(x - w * .3, y + 4, w * .6, h - 10), fill("#e8e2d2"))
    for k in range(5): c.drawLine(x - w * .3 + k * w * .13, y + 4, x - w * .3 + k * w * .13 + 30, y + h - 6, stroke("#9c9482", 3, .6))
def sc_room(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        room(ctx)
        trunk(c, cx + 60, H * .9, 760, cut=seg(t, d * .45, d * .75), inside=_bundle_in)
        label(c, "STILL IN PARIS · A SMALL RENTED ROOM", cx, 80, 28, seg(t, .1, 1.3), WHITE)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        peruggia(c, cx - 450, H + 40, 1.6, a=ap(t, .1))
        id_card(c, cx + 360, cy - 40, 720, rot=2, a=ap(t, .3), title="LOUVRE WORKMAN", name="V. PERUGGIA", sub="decorator · glazier")
        stamp(c, "ALREADY QUESTIONED", cx + 360, cy + 300, 58, seg(t, d * .55, d * .55 + .35), rot=-6)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        two(ctx, lrim=COP, rrim=THIEF)
        text(c, "“I overslept.”", cx + 420, 160, 60, "serifb", WHITE, ap(t, d * .4))
        text(c, "after a night of drinking", cx + 420, 225, 34, "serif", GOLD, ap(t, d * .5))
        chip(c, "THEY BELIEVED HIM", cx, H - 70, a=ap(t, d * .8), size=38, color="#9db58a")
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        glass_case(c, cx - 420, cy - 20, 420, 560, t=t)
        thumbprint(c, cx - 380, cy + 60, 80, p=seg(t, .3, 1.8))
        label(c, "BY ONE ACCOUNT", cx - 420, 120, 26, seg(t, .1, 1.1), WHITE)
        ctx.layer(ap(t, d * .3)); card(c, cx + 420, cy - 30, 620, 420, rot=1.5)
        text(c, "POLICE FILE", 310, 80, 38, "typeb", INK)
        typed(c, "prints on record:", 50, 180, 34, seg(t, d * .35, d * .5), color="#1d1a14")
        typed(c, "PERUGGIA, V.", 50, 240, 38, seg(t, d * .5, d * .6), kind="typeb", color="#1d1a14")
        thumbprint(c, 500, 260, 60, p=seg(t, d * .4, d * .7), color="#3b3324")
        text(c, "RECONSTRUCTION", 50, 395, 14, "sansb", "#8c7d60", 1, align="l", spacing=3)
        c.restore(); c.restore()
        stamp(c, "NEVER MATCHED", cx + 420, cy + 260, 60, seg(t, d * .75, d * .75 + .35), rot=-7)
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        room(ctx, night=1)
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill("#000000", .35))
        portrait(c, cx + 140, cy + 20, 260, glow=.6 + .2 * math.sin(t * 2))
        peruggia(c, cx - 360, H + 40, 1.4)
        text(c, "“I fell a victim to her smile”", cx, 110, 50, "serifb", WHITE, ap(t, d * .2))
        text(c, "“and feasted my eyes on my treasure every evening.”", cx, 175, 36, "serif", GOLD, ap(t, d * .5))
        c.restore()
    t, a, d = beat(ctx, 5)
    if a > 0:
        n = int(28 * eo(seg(t, .2, d * .8)))
        text(c, f"{n}", cx, cy + 60, 300, "disp", GOLD, ap(t, .1))
        text(c, "MONTHS IN HIDING", cx, cy + 160, 50, "sansb", WHITE, ap(t, .3), spacing=6)
        for i in range(28):
            x = cx - 810 + (i % 14) * 125; y = 160 + (i // 14) * 90
            c.drawRoundRect(skia.Rect.MakeXYWH(x - 45, y - 30, 90, 60), 8, 8, fill(PAPER if i < n else "#2a2e3a", .9))
        c.restore()

# ------------------------------------------------------------------ Florence
def sc_florence(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        letter_card(c, cx - 300, cy + 40, t, d, lines=("Signore,", "", "I have the Mona Lisa.", "I want to bring her", "home to Italy."), sign="Leonardo")
        figure(c, cx + 650, H + 40, 1.3, hat=True, rim="#c9a56a", a=ap(t, .2))
        label(c, "ALFREDO GERI · ART DEALER, FLORENCE", cx + 520, 110, 26, seg(t, .2, 1.4), WHITE)
        label(c, "LATE 1913", cx - 300, 110, 30, seg(t, .1, 1))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        text(c, "500,000 LIRE", cx, 230, 120, "disp", GOLD, ap(t, .2))
        figure(c, cx - 360, H + 40, 1.3, hat=True, rim="#c9a56a", a=ap(t, d * .3))
        figure(c, cx + 360, H + 40, 1.3, hat=False, rim=COP, a=ap(t, d * .45))
        label(c, "GERI", cx - 360, 420, 28, seg(t, d * .3, d * .3 + 1), WHITE)
        label(c, "GIOVANNI POGGI · DIRECTOR, UFFIZI GALLERY", cx + 360, 420, 24, seg(t, d * .45, d * .45 + 1.3), WHITE)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        route(ctx, seg(t, .3, d * .7), "PARIS", "FLORENCE", sp=520)
        train(c, lerp(-200, W + 600, seg(t, 0, d)), H * .95, .55, t=t)
        label(c, "DECEMBER 1913 · WITH HIS TRUNK", cx, 90, 30, seg(t, .1, 1.3))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        q = seg(t, d * .25, d * .55)
        trunk(c, cx - 420, H * .92, 520, lid=seg(t, .1, d * .25))
        xfade(c, q, lambda: bundle(c, cx + 250, cy, 300, rot=-4, colr="#a8262a"), lambda: portrait(c, cx + 250, cy, 300, glow=.6))
        text(c, "red silk", cx + 250, 120, 40, "serif", WHITE, ap(t, .4) * (1 - q))
        text(c, "“intact and marvellously preserved”", cx + 250, 120, 42, "serifb", GOLD, ap(t, d * .6))
        chip(c, "LOUVRE STAMP ON THE BACK: REAL", cx + 250, H - 60, a=ap(t, d * .8), size=34)
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        peruggia(c, cx - 420, H + 40, 1.5, bow=eo(seg(t, d * .3, d * .5)))
        for i in range(2): person(c, cx - 720 + i * 600, H * .98, 380, rim=COP, a=ap(t, d * .2 + i * .2))
        stamp(c, "ARRESTED", cx - 420, 300, 84, seg(t, d * .35, d * .35 + .35), rot=-7)
        c.drawRoundRect(skia.Rect.MakeXYWH(cx + 160, 240, 640, 170), 14, 14, fill("#0d1016"))
        c.drawRoundRect(skia.Rect.MakeXYWH(cx + 160, 240, 640, 170), 14, 14, stroke(GOLD, 4, ap(t, d * .6)))
        k = seg(t, d * .7, d * .8)
        text(c, "HOTEL", cx + 480, 345, 60, "serifb", GOLD, ap(t, d * .6) * (1 - k))
        text(c, "HOTEL LA GIOCONDA", cx + 480, 345, 50, "serifb", GOLD, k)
        text(c, "(later, the story goes)", cx + 480, 460, 30, "serif", WHITE, ap(t, d * .8) * .8)
        c.restore()

# ------------------------------------------------------------------ the trial
def sc_trial(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        peruggia(c, cx - 450, H + 40, 1.6, a=ap(t, .1))
        text(c, "“A patriot.”", cx + 360, 300, 80, "disp", GOLD, ap(t, .3))
        text(c, "“Napoleon stole her from Italy.", cx + 360, 450, 44, "serifb", WHITE, ap(t, d * .4))
        text(c, "I only brought her home.”", cx + 360, 510, 44, "serifb", WHITE, ap(t, d * .5))
        label(c, "HIS STORY", cx + 360, 180, 28, seg(t, .1, 1.1), WHITE)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        stamp(c, "NOT TRUE", cx, 140, 70, seg(t, .1, .45), rot=-5)
        steps = (("1500s", "Leonardo takes the painting to France himself"), ("", "King Francis I acquires it"), ("1911", "his letters home: making his fortune"))
        for i, (yr, s) in enumerate(steps):
            y = 330 + i * 190; q = ap(t, d * .15 + i * d * .22)
            c.drawCircle(cx - 640, y - 14, 16, fill(GOLD if i < 2 else RED, q))
            if i < 2: c.drawLine(cx - 640, y + 6, cx - 640, y + 170, stroke(GOLD, 4, q * .6))
            text(c, yr, cx - 680, y, 34, "sansb", GOLD, q, align="r")
            text(c, s, cx - 590, y, 48, "serifb", WHITE if i < 2 else "#f0b0a8", q, align="l")
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        crowd(c, cx, H + 70, n=9, s=.95, spread=210, t=t, rim="#c9a56a")
        text(c, "1 YEAR, 15 DAYS", cx, 230, 100, "disp", WHITE, ap(t, d * .3))
        text(c, "free after about 7 months", cx, 320, 48, "serifb", GOLD, ap(t, d * .6))
        text(c, "(by most accounts; some say 8)", cx, 380, 30, "serif", WHITE, ap(t, d * .7) * .75)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        cities = (("FLORENCE", cx - 520, cy + 40), ("ROME", cx, cy + 180), ("MILAN", cx + 520, cy - 80))
        for i, (n, x, y) in enumerate(cities):
            q = ap(t, .2 + i * d * .2)
            pin(c, x, y, 1.6, n, seg(t, .2 + i * d * .2, .9 + i * d * .2))
            for k in range(5): figure(c, x - 160 + k * 80, y + 300, .4, a=q * .9, hat=k % 2 == 0, rim="#2b3044")
        portrait(c, cx, 220, 150, frame=True, a=ap(t, .1))
        label(c, "A TOUR OF ITALY", cx, 400, 26, seg(t, .1, 1.2), WHITE)
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        gallery_wall(ctx, gap=GAP, hang=lambda c: hung(c, ap(t, .1, .8)))
        crowd(c, cx, H + 60, n=9, s=.9, spread=200, t=t)
        label(c, "JANUARY 1914 · BACK IN THE LOUVRE", cx, 60, 28, seg(t, .1, 1.3))
        n = int(100000 * eo(seg(t, d * .3, d * .75)))
        chip(c, f"{n:,}+ VISITORS IN 2 DAYS", cx, 840, a=ap(t, d * .3), size=44)
        c.restore()

# ------------------------------------------------------------------ the end
def sc_end(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        peruggia(c, cx - 560, H + 40, 1.5, a=ap(t, .1))
        rows = (("1914-18", "Italian army · First World War"), ("", "prisoner of war"), ("after", "back to France, painter and decorator"))
        for i, (yr, s) in enumerate(rows):
            y = 340 + i * 170; q = ap(t, .3 + i * d * .25)
            text(c, yr, cx - 80, y, 34, "sansb", GOLD, q, align="r")
            text(c, s, cx - 40, y, 48, "serifb", WHITE, q, align="l")
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        card(c, cx - 400, cy, 560, 440, rot=-1.5, a=ap(t, .1))
        text(c, "VINCENZO PERUGGIA", 280, 140, 40, "serifb", INK)
        text(c, "1881 – 1925", 280, 220, 54, "disp", INK)
        text(c, "died on his 44th birthday", 280, 300, 32, "serif", "#3b3324")
        c.restore()
        newspaper(ctx, cx + 420, cy + 20, 640, 520, 2, ["OBITUARY"], "the wrong man · years later", "BY MISTAKE", a=ap(t, d * .5), hp=seg(t, d * .5, d * .7))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        portrait(c, cx, cy - 120, 300, frame=True, a=ap(t, .1))
        glass_case(c, cx, cy - 120, 360, 500, a=ap(t, .3), t=t)
        crowd(c, cx, H + 70, n=11, s=.85, spread=170, t=t)
        n = int(8000000 * eo(seg(t, d * .2, d * .7)))
        text(c, f"~{n:,} a year", cx - 560, cy - 140, 64, "disp", GOLD, ap(t, d * .2))
        text(c, "behind bulletproof glass", cx + 560, cy - 140, 40, "serifb", WHITE, ap(t, d * .6))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        k = seg(t, d * .35, d * .42)
        def A():
            book(c, cx - 300, cy, 280, rot=-4, year="1907", note="TWO SENTENCES", hi=1)
            hooks(c, cx + 400, cy - 40, 300, 420)
            text(c, "a small man · a helpful plumber · four empty hooks", cx, 110, 42, "serifb", WHITE, ap(t, d * .1))
        def B():
            c.drawCircle(cx, cy, 520, fill("#ffcf7a", .08, 120))
            portrait(c, cx, cy - 30, 330, frame=True, glow=1)
            text(c, "THE MOST FAMOUS", cx, 120, 70, "disp", WHITE, ap(t, d * .5))
            text(c, "PAINTING IN THE WORLD", cx, H - 60, 70, "disp", GOLD, ap(t, d * .6))
            smock_man(c, cx - 640, H * .98, 280, a=.9)
            person(c, cx + 640, H * .98, 280, rim=PLUMB, a=.9)
        xfade(c, k, A, B)
        c.restore()

def sc_outro(ctx):
    c, cx, cy, t = ctx.c, ctx.cx, ctx.cy, ctx.t
    stamp(c, "CASE CLOSED", cx, cy - 110, 150, seg(t, .15, .45), rot=-5)
    label(c, "CASE CLOSED FILES", cx, cy + 110, 30, seg(t, .6, 1.4), GOLD)
    text(c, "New case every week. Subscribe so you don't miss it.", cx, cy + 210, 40, "serif", WHITE, ap(t, 1.1))

SCENES = {k[3:]: v for k, v in list(globals().items()) if k.startswith("sc_") and callable(v)}
HITS = [("cold", 3, 0, .3), ("louvre", 0, 0, .7), ("louvre", 4, 0, .72), ("monday", 0, 0, .25), ("plumber", 0, 0, .1), ("gone", 2, 0, .05),
        ("empty", 3, 0, .15), ("empty", 3, 0, .4), ("room", 1, 0, .55), ("room", 3, 0, .75), ("florence", 4, 0, .35), ("trial", 1, 0, .05), ("outro", -1, .15, 0)]
SHORT_HITS = []
WARM = {}

THUMB_WORDS = [(["NOBODY", "NOTICED."], 140), (["SHE'S", "GONE."], 160), (["26 HOURS", "LATE."], 130)]
def thumbnail(c, W, H, word):
    word, size = word
    sh = skia.GradientShader.MakeRadial(center=(W * .3, H * .5), radius=900, colors=[col("#4a2c26"), col("#24161a"), col("#07080b")], positions=[0, .5, 1])
    c.drawPaint(skia.Paint(Shader=sh))
    c.drawRect(skia.Rect.MakeXYWH(W * .05, H * .12, W * .26, H * .72), fill("#6a5446", .45))
    hooks(c, W * .18, H * .48, W * .26, H * .72, patch=False)
    c.drawCircle(W * .5, H * .55, 330, fill("#ffcf7a", .14, 90))
    c.save(); c.translate(W * .5, H * .56); c.rotate(-8); portrait(c, 0, 0, 330, frame=True); c.restore()
    smock_man(c, W * .78, H * 1.25, 900, rim=GOLD)
    for i, ln in enumerate(word):
        sz = size
        while tw(ln, "sansb", sz) > 520: sz -= 6
        big_word(c, ln, W * .2 if i == 0 else W * .2, H * .2 + i * size * 1.0, sz, "#ffd36b")


# ---------------- the Short (60-100 s, 9:16) ----------------
from shorts import hook_card, cta_card
def _art(c, cx, cy, t, d):
    q = .9 * eo(seg(t, 0, .8)); portrait(c, cx, cy + 200, 240, a=q, frame=True)
SCENES["hook_a"] = hook_card(["THE MONA LISA.", "A PLUMBER", "HELD THE DOOR."], stamp_text="PARIS 1911", prop=_art)
SCENES["cta_a"] = cta_card("CASE 005 · MONA LISA", "FULL CASE")
SHORT_HITS += [("hook_a", -1, .15, .62)]
SHORT_VIEW = {}
