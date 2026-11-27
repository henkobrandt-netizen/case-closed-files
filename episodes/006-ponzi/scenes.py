from lib import *

PONZI = GOLD          # Ponzi's rim colour
POST = "#8fa0c8"      # the Boston Post / officials
CROWD = "#2b3044"
MONEYG = "#9db58a"

def beat(ctx, i):
    t, a, d = ctx.ph(i)
    if a > 0: ctx.layer(a)
    return t, a, d
def xfade(c, k, draw_a, draw_b):
    if k < 1:
        c.saveLayerAlpha(None, int(255 * (1 - k))); draw_a(); c.restore()
    if k > 0:
        c.saveLayerAlpha(None, int(255 * k)); draw_b(); c.restore()
def panel(c, cx, cy, w, h, a=1.0):
    c.drawRoundRect(skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), 20, 20, fill("#0d1016", .92 * a))
    c.drawRoundRect(skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), 20, 20, stroke("#2e3446", 4, a))
def clock(c, x, y, r, hh, mm, a=1.0):
    c.drawCircle(x, y, r, fill("#e9dfc6", a)); c.drawCircle(x, y, r, stroke(GOLD, r * .08, a))
    for k in range(12):
        an = k * math.pi / 6; c.drawLine(x + math.sin(an) * r * .8, y - math.cos(an) * r * .8, x + math.sin(an) * r * .9, y - math.cos(an) * r * .9, stroke(INK, r * .04, a))
    am = mm / 60 * 2 * math.pi; ah = (hh % 12 + mm / 60) / 12 * 2 * math.pi
    c.drawLine(x, y, x + math.sin(ah) * r * .5, y - math.cos(ah) * r * .5, stroke(INK, r * .07, a))
    c.drawLine(x, y, x + math.sin(am) * r * .75, y - math.cos(am) * r * .75, stroke(INK, r * .045, a))
def sun_heat(ctx, a=1.0, t=0.0):
    c = ctx.c; W, H = ctx.W, ctx.H
    c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill("#3a2a1e", .35 * a))
    c.drawCircle(W * .82, H * .16, 70, fill("#ffe7b0", .9 * a)); c.drawCircle(W * .82, H * .16, 260, fill("#ffcf7a", .12 * a, 80))
    for k in range(5):
        y = H * .55 + k * 40 + math.sin(t * 2 + k) * 6
        P = skia.Path(); P.moveTo(0, y)
        for i in range(0, int(W) + 80, 80): P.lineTo(i, y + math.sin(i * .02 + t * 3 + k) * 6)
        c.drawPath(P, stroke("#ffcf7a", 2, .05 * a))
def street(ctx, a=1.0, t=0.0, lit=.5):
    """School Street: a row of brick fronts, pavement."""
    c = ctx.c; W, H = ctx.W, ctx.H; base = H * .8
    skyline(c, W, base - 330, 12, "#141722", a, 60, 200)
    storefront(c, W * .8, base, 620, 560, sign="SECURITIES EXCHANGE CO.", a=a, lit=lit, sub="SCHOOL STREET")
    storefront(c, W * .38, base, 560, 470, sign="", a=a * .8, lit=.15)
    storefront(c, W * .02, base, 520, 520, sign="", a=a * .8, lit=.1)
    c.drawRect(skia.Rect.MakeLTRB(0, base, W, H), fill("#16181e", a))
    c.drawLine(0, base + 8, W, base + 8, stroke("#2a2e3a", 6, a, cap=False))
def cup(c, x, y, s, a=1.0):
    c.drawRoundRect(skia.Rect.MakeXYWH(x - 30 * s, y - 60 * s, 60 * s, 60 * s), 8 * s, 8 * s, fill(PAPER, a))
    c.drawCircle(x + 34 * s, y - 32 * s, 14 * s, stroke(PAPER, 6 * s, a))
    for k in (-12, 6): c.drawLine(x + k * s, y - 72 * s, x + (k + 6) * s, y - 100 * s, stroke("#ffffff", 3 * s, a * .4))
def stamp_on(c, s, x, y, size, p, rot=-8, color=RED): stamp(c, s, x, y, size, p, rot=rot, color=color)
def counter(c, v, x, y, size, a=1.0, color=GOLD, prefix="$", suffix=""):
    v = round(v / 1000) * 1000 if v > 20000 else v
    text(c, f"{prefix}{int(v):,}{suffix}", x, y, size, "disp", color, a)
def bank(c, cx, base, w=820, a=1.0, name="HANOVER TRUST CO.", crack=0.0):
    """Classical bank front with columns."""
    h = w * .62
    c.drawRect(skia.Rect.MakeXYWH(cx - w / 2, base - h, w, h), fill("#262a36", a))
    P = skia.Path(); P.moveTo(cx - w / 2 - 30, base - h); P.lineTo(cx, base - h - w * .2); P.lineTo(cx + w / 2 + 30, base - h); P.close()
    c.drawPath(P, fill("#323848", a))
    c.drawRect(skia.Rect.MakeXYWH(cx - w / 2 - 30, base - h - 8, w + 60, 28), fill("#3a4152", a))
    sz = 40
    while tw(name, "serifb", sz) > w * .78: sz -= 2
    text(c, name, cx, base - h + 70, sz, "serifb", GOLD, a, spacing=3)
    for k in range(6):
        x = cx - w * .4 + k * w * .16
        c.drawRect(skia.Rect.MakeXYWH(x - 22, base - h + 100, 44, h - 130), fill("#3a4152", a))
    c.drawRect(skia.Rect.MakeXYWH(cx - w / 2 - 40, base - 30, w + 80, 30), fill("#323848", a))
    if crack > 0:
        u = w / 820; P = skia.Path(); P.moveTo(cx + 40 * u, base - h - w * .18)
        pts = [(cx + 10 * u, base - h), (cx + 60 * u, base - h * .7), (cx - 20 * u, base - h * .45), (cx + 30 * u, base - h * .2), (cx - 10 * u, base)]
        n = int(len(pts) * crack + .999)
        for px, py in pts[:n]: P.lineTo(px, py)
        c.drawPath(P, stroke(RED, 7 * u, a))
def ledger(c, x, y, w, h, a=1.0, rows=(), rot=-1.5, p=1.0):
    card(c, x, y, w, h, rot=rot, a=a)
    for k in range(int(h / 48)): c.drawLine(40, 90 + k * 48, w - 40, 90 + k * 48, stroke("#9db0c8", 1.5, a * .6, cap=False))
    c.drawLine(w * .68, 60, w * .68, h - 40, stroke(RED, 2, a * .6, cap=False))
    for i, (l, v, colr) in enumerate(rows):
        q = clamp(p * len(rows) - i)
        typed(c, l, 50, 130 + i * 72, 34, q, color="#1d1a14", a=a)
        if q >= 1: text(c, v, w - 50, 130 + i * 72, 38, "typeb", colr, a, align="r")
    c.restore()
def pyramid(c, cx, top, levels, p, a=1.0, r=13, gap=34, vgap=74, red_from=99):
    """Rows of dots doubling each level: 1, 2, 4, 8... revealed with p."""
    def pos(L, i):
        n = 2 ** L; g = min(gap, 1500 / n); return cx + (i - (n - 1) / 2) * g, top + L * vgap, min(r, g * .4)
    for L in range(levels):
        n = 2 ** L; q = seg(p, L / levels, (L + .8) / levels)
        if q <= 0: break
        for i in range(n):
            x, y, rr = pos(L, i)
            if L > 0:
                px, py, pr = pos(L - 1, i // 2); c.drawLine(x, y - rr, px, py + pr, stroke("#ffffff", 1.5, .2 * a * q))
            c.drawCircle(x, y, rr * eo(q), fill(RED if L >= red_from else (GOLD if L == 0 else WHITE), a))

# ------------------------------------------------------------------ cold open
def sc_cold(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        sun_heat(ctx, t=t)
        street(ctx, lit=.3)
        n = int(4 + 14 * eo(seg(t, .3, d * .8)))
        queue(c, W * .7, W * .7 - n * 95, H * .86, n, h=250, t=t, papers=1)
        label(c, "MONDAY 26 JULY 1920 · SCHOOL STREET, BOSTON", cx, 70, 28, seg(t, .2, 1.6))
        chip(c, "HUNDREDS IN LINE", cx - 300, 170, a=ap(t, d * .55), size=36)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        # map of the line: office -> round the corner -> City Hall
        for i in range(-6, 7): c.drawLine(cx + i * 150, 120, cx + i * 150, H - 120, stroke("#ffffff", 1, .04, cap=False))
        c.drawRect(skia.Rect.MakeXYWH(cx + 420, cy - 260, 300, 200), fill("#3a2620")); text(c, "THE OFFICE", cx + 570, cy - 150, 28, "sansb", GOLD)
        c.drawRect(skia.Rect.MakeXYWH(cx - 760, cy + 120, 320, 220), fill("#262a36")); text(c, "CITY HALL", cx - 600, cy + 240, 28, "sansb", WHITE)
        pts = [(cx + 420, cy - 120), (cx - 300, cy - 120), (cx - 300, cy + 60), (cx - 440, cy + 180)]
        hd = dashed(c, pts, eo(seg(t, .2, d * .6)), color=GOLD, w=10, dash=26)
        for k, s in enumerate(("CLERKS", "COOKS", "SHOPKEEPERS", "WIDOWS")):
            chip(c, s, cx + 120 + (k % 2) * 330, cy + 150 + (k // 2) * 110, a=ap(t, d * .3 + k * .35), size=32, color=WHITE)
        promissory(c, cx - 560, cy - 300, 360, rot=-6, a=ap(t, d * .7))
        text(c, "a small piece of paper", cx - 560, cy - 160, 30, "serif", GOLD, ap(t, d * .78))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        sun_heat(ctx, t=t)
        c.drawCircle(cx, cy, 460, fill("#ffcf7a", .08, 120))
        boater(c, cx, H + 30, 2.4, rim=PONZI, smile=ap(t, d * .2), cane=ap(t, .3))
        for k in range(3): cup(c, cx - 620 + k * 110, cy + 120, 1.3, a=ap(t, d * .3 + k * .15))
        sandwich(c, cx - 510, cy + 260, 200, a=ap(t, d * .45), bite=False)
        text(c, "coffee & sandwiches", cx - 510, cy - 60, 40, "serifb", WHITE, ap(t, d * .3))
        chip(c, "FAINTING WOMEN → FRONT OF THE LINE", cx - 480, H - 90, a=ap(t, d * .68), size=30)
        label(c, "THE MAN IN THE STRAW HAT", cx, 70, 28, seg(t, .2, 1.4))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        k = seg(t, d * .5, d * .6)
        def A():
            notes_pile(ctx, seg(t, 0, d * .45), cx, cy + 260, n=18, w=260)
            text(c, "PAID BACK IN CASH", cx, 150, 80, "disp", WHITE, ap(t, .2))
        def B():
            c.drawCircle(cx, cy, 420, fill("#ffe2a0", .08, 100))
            reply_coupon(c, cx, cy + 40, 560, rot=-4, a=1, glow=ap(t, d * .6))
            text(c, "WHERE DID THE MONEY COME FROM?", cx, 120, 60, "disp", WHITE, ap(t, d * .55))
            text(c, "5¢", cx + 360, cy + 300, 150, "disp", GOLD, ap(t, d * .75))
        xfade(c, k, A, B)
        c.restore()

def sc_title(ctx):
    c, cx, cy, t = ctx.c, ctx.cx, ctx.cy, ctx.t
    c.drawCircle(cx, cy - 20, 420, fill("#ffcf7a", .05, 120))
    reply_coupon(c, cx, cy - 300, 200, rot=-5, a=ap(t, .1, .6), lab=False)
    label(c, "CASE CLOSED FILES  ·  NO. 006", cx, cy - 150, 26, seg(t, .1, .7))
    text(c, "THE POSTAGE", cx, cy - 10 + (1 - ap(t, .2, .6)) * 30, 128, "disp", WHITE, ap(t, .2, .6), spacing=4)
    text(c, "STAMP KING", cx, cy + 140 + (1 - ap(t, .5, .6)) * 30, 140, "disp", GOLD, ap(t, .5, .6), spacing=4)
    text(c, "A true story · Boston, 1919–1920", cx, cy + 250, 34, "serif", WHITE, ap(t, 1.0) * .8)

# ------------------------------------------------------------------ arrival
def sc_arrival(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        liner(ctx, t, d, lab="15 NOVEMBER 1903 · BOSTON")
        chip(c, "THE SS VANCOUVER", cx, H - 70, a=ap(t, d * .4), size=36)
        text(c, "17 YEARS EARLIER", cx, 200, 64, "disp", WHITE, ap(t, .2))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        person(c, cx - 560, H * .93, 420, rim=PONZI, a=ap(t, .1))
        for k in range(6):
            yy = H * .93 - k * 80; c.drawLine(cx - 790, yy, cx - 750, yy, stroke(GOLD, 3, ap(t, .3)))
        text(c, "5 ft 2", cx - 800, H * .93 - 430, 40, "sansb", GOLD, ap(t, .5), align="r")
        for k in range(4):   # playing cards being swept away
            q = seg(t, d * .12 + k * .15, d * .3 + k * .15)
            card(c, cx - 200 + k * 60 + q * 400, cy - 300 - q * 160, 120, 170, rot=-15 + k * 10 + q * 40, a=1 - q, color="#f2ece0")
            text(c, "♠♥♦♣"[k], 60, 100, 60, "serifb", RED if k in (1, 2) else INK, 1 - q); c.restore()
        text(c, "a card cheat took the rest", cx - 20, cy - 60, 34, "serif", WHITE, ap(t, d * .2))
        text(c, "$2.50", cx + 430, cy + 40, 150, "disp", GOLD, ap(t, d * .5))
        text(c, "in cash", cx + 430, cy + 110, 40, "serifb", WHITE, ap(t, d * .55))
        text(c, "$1,000,000 in hopes", cx + 430, cy + 260, 60, "disp", WHITE, ap(t, d * .78))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        label(c, "THE HOPES DID NOT PAY", cx, 90, 30, seg(t, .1, 1.3), WHITE)
        jobs = (("NEW YORK", "washing dishes"), ("FLORIDA", "painting signs"), ("THE EAST COAST", "drifting"))
        for i, (pl, s) in enumerate(jobs):
            x = cx - 560 + i * 560; q = ap(t, .3 + i * d * .25)
            panel(c, x, cy + 40, 480, 560, q)
            person(c, x, cy + 280, 300, a=q, rim=PONZI if i == 2 else CROWD, step=t * .6 if i == 2 else 0)
            text(c, pl, x, cy - 160, 40, "sansb", GOLD, q, spacing=3)
            text(c, s, x, cy - 100, 36, "serif", WHITE, q)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        card(c, cx - 420, cy + 20, 720, 560, rot=-1.5, a=ap(t, .1))
        text(c, "RECORD", 360, 80, 40, "typeb", INK)
        typed(c, "MONTREAL", 60, 180, 42, seg(t, .3, d * .2), kind="typeb", color="#1d1a14")
        typed(c, "- worked at a small bank", 60, 240, 34, seg(t, d * .15, d * .3), color="#1d1a14")
        typed(c, "- a forged cheque", 60, 290, 34, seg(t, d * .25, d * .38), color="#1d1a14")
        typed(c, "ATLANTA", 60, 390, 42, seg(t, d * .5, d * .6), kind="typeb", color="#1d1a14")
        typed(c, "- 5 Italians brought in from Canada", 60, 450, 28, seg(t, d * .58, d * .75), color="#1d1a14")
        text(c, "RECONSTRUCTION", 60, 540, 14, "sansb", "#8c7d60", 1, align="l", spacing=3)
        c.restore()
        stamp(c, "PRISON", cx - 250, cy - 100, 50, seg(t, d * .38, d * .38 + .35), rot=-10)
        stamp(c, "PRISON", cx - 250, cy + 110, 50, seg(t, d * .78, d * .78 + .35), rot=-6)
        mugshot(c, cx + 520, cy + 20, 400, rot=2, a=ap(t, d * .3), plate="1910")
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        k = seg(t, d * .72, d * .8)
        def A():
            storefront(c, cx, H * .86, 900, 560, sign="GROCERY", lit=.35)
            c.drawRect(skia.Rect.MakeLTRB(0, H * .86, W, H), fill("#16181e"))
            person(c, cx - 620, H * .93, 380, rim=PONZI); person(c, cx - 470, H * .93, 340, rim="#c99aa0")
            label(c, "BOSTON · 1917–1919", cx, 70, 28, seg(t, .1, 1.3))
            text(c, "married Rose · took over her father's grocery", cx, 160, 40, "serifb", WHITE, ap(t, d * .25))
            stamp(c, "IT WENT BADLY", cx + 120, cy - 40, 70, seg(t, d * .5, d * .5 + .35), rot=-7)
        def B():
            envelope(c, cx, cy, 520, rot=-4)
            text(c, "A LETTER FROM SPAIN", cx, 170, 70, "disp", GOLD, ap(t, d * .8))
            chip(c, "ESPAÑA", cx + 160, cy - 80, size=30, color=WHITE)
        xfade(c, k, A, B)
        c.restore()

# ------------------------------------------------------------------ the letter and the coupon
def sc_letter(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        bank(c, cx - 380, H * .9, 760)
        label(c, "AUGUST 1919", cx, 70, 30, seg(t, .1, 1.2))
        ctx.layer(ap(t, d * .2)); card(c, cx + 560, cy - 20, 520, 420, rot=2)
        text(c, "LOAN REQUEST", 260, 80, 36, "typeb", INK)
        typed(c, "for: a trade journal", 40, 170, 32, seg(t, d * .25, d * .4), color="#1d1a14")
        text(c, "$2,000", 260, 290, 90, "disp", INK, ap(t, d * .4))
        text(c, "RECONSTRUCTION", 40, 400, 13, "sansb", "#8c7d60", 1, align="l", spacing=3)
        c.restore(); c.restore()
        stamp(c, "REFUSED", cx + 560, cy - 20, 80, seg(t, d * .55, d * .55 + .35), rot=-12)
        stamp(c, "REMEMBER THIS BANK", cx - 380, 200, 52, seg(t, d * .82, d * .82 + .35), rot=-5, color="#e8b23a")
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        out = eo(seg(t, d * .25, d * .7))
        c.drawCircle(cx, cy, 480, fill("#ffe2a0", .06 * out, 120))
        envelope(c, cx, cy + 220, 620, rot=-3)
        reply_coupon(c, cx, cy + 200 - out * 380, 520, rot=-3 + out * 5, a=seg(t, d * .2, d * .3), glow=out)
        text(c, "a small slip of paper", cx - 560, cy - 300, 40, "serif", WHITE, ap(t, d * .5))
        label(c, "AN INTERNATIONAL REPLY COUPON", cx, H - 70, 32, seg(t, d * .7, d), GOLD)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        label(c, "SINCE 1906 · UNIVERSAL POSTAL UNION", cx, 80, 28, seg(t, .1, 1.3))
        A = (cx - 560, cy + 60); B = (cx + 560, cy + 60)
        pin(c, A[0], A[1], 1.5, "YOU", 1); pin(c, B[0], B[1], 1.5, "ABROAD", seg(t, .3, .9))
        go = eio(seg(t, d * .15, d * .5)); back_ = eio(seg(t, d * .6, d * .9))
        pts = arc_pts(A, B, 220); hx, hy = dashed(c, pts, go, w=5)
        envelope(c, hx, hy - 40, 130, rot=-6)
        reply_coupon(c, hx + 40, hy - 100, 150, rot=8, a=1 - back_, lab=False)
        if back_ > 0:
            P = arc_pts(B, A, -200); bx, by = dashed(c, P, back_, w=5, color=WHITE)
            c.drawRect(skia.Rect.MakeXYWH(bx - 40, by - 50, 80, 96), fill("#c9b37a")); c.drawRect(skia.Rect.MakeXYWH(bx - 32, by - 42, 64, 80), stroke(INK, 2, cap=False))
            text(c, "STAMP", bx, by + 8, 16, "sansb", INK)
        text(c, "swap it for local postage, in any country", cx, H - 120, 42, "serifb", WHITE, ap(t, d * .7))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        reply_coupon(c, cx - 500, cy - 60, 420, rot=-4, a=ap(t, .1))
        text(c, "SPAIN", cx - 500, 170, 44, "sansb", GOLD, ap(t, .2), spacing=4)
        text(c, "30 centavos", cx - 500, cy + 230, 56, "disp", WHITE, ap(t, d * .15))
        c.drawLine(cx - 180, cy - 60, cx + 200, cy - 60, stroke(GOLD, 6, ap(t, d * .25)))
        P = skia.Path(); P.moveTo(cx + 200, cy - 85); P.lineTo(cx + 240, cy - 60); P.lineTo(cx + 200, cy - 35); P.close(); c.drawPath(P, fill(GOLD, ap(t, d * .25)))
        sx, sy = cx + 500, cy - 60; q = ap(t, d * .3)
        c.drawRect(skia.Rect.MakeXYWH(sx - 120, sy - 150, 240, 300), fill("#c9b37a", q)); c.drawRect(skia.Rect.MakeXYWH(sx - 100, sy - 130, 200, 260), stroke(INK, 3, q, cap=False))
        text(c, "5¢", sx, sy + 40, 120, "disp", INK, q)
        text(c, "AMERICA", cx + 500, 170, 44, "sansb", GOLD, ap(t, d * .3), spacing=4)
        text(c, "a 5-cent stamp", cx + 500, cy + 230, 50, "serifb", WHITE, ap(t, d * .35))
        chip(c, "SPAIN'S MONEY HAD FALLEN", cx, cy + 340, a=ap(t, d * .55), size=34, color=RED)
        text(c, "worth more here than it cost there", cx, H - 50, 40, "serifb", GOLD, ap(t, d * .8))
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        label(c, "WHAT $1 BUYS (BY ONE ACCOUNT)", cx, 80, 30, seg(t, .1, 1.3))
        text(c, "BOSTON", cx - 640, 250, 44, "sansb", WHITE, ap(t, .2), align="l")
        for k in range(5): reply_coupon(c, cx - 560 + k * 100, 360, 84, rot=0, a=ap(t, .3 + k * .1), lab=False)
        text(c, "5", cx + 800, 380, 90, "disp", WHITE, ap(t, .8), align="r")
        text(c, "ROME", cx - 640, 520, 44, "sansb", GOLD, ap(t, d * .3), align="l")
        n = int(66 * eo(seg(t, d * .32, d * .6)))
        for k in range(n): reply_coupon(c, cx - 580 + (k % 22) * 52, 600 + (k // 22) * 46, 44, a=1, lab=False)
        text(c, str(n), cx + 800, 680, 110, "disp", GOLD, ap(t, d * .35), align="r")
        text(c, "buy cheap in Europe · swap them here", cx, H - 130, 46, "serifb", WHITE, ap(t, d * .62))
        text(c, "at least, that was the idea", cx, H - 60, 36, "serif", GOLD, ap(t, d * .85))
        c.restore()

# ------------------------------------------------------------------ the company
def sc_company(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill("#1c1712"))
        dx, dy, dw, dh = cx - 330, 110, 660, 900
        c.drawRect(skia.Rect.MakeXYWH(dx, dy, dw, dh), fill("#3a2618")); c.drawRect(skia.Rect.MakeXYWH(dx, dy, dw, dh), stroke("#24170e", 16, cap=False))
        c.drawRect(skia.Rect.MakeXYWH(dx + 60, dy + 60, dw - 120, 420), fill("#d8c9a2", .35))
        c.drawRect(skia.Rect.MakeXYWH(dx + 60, dy + 60, dw - 120, 420), stroke("#24170e", 8, cap=False))
        text(c, "SECURITIES", cx, dy + 170, 58, "disp", GOLD, ap(t, .3))
        text(c, "EXCHANGE CO.", cx, dy + 240, 58, "disp", GOLD, ap(t, .5))
        c.drawLine(cx - 180, dy + 280, cx + 180, dy + 280, stroke(GOLD, 3, ap(t, .6)))
        q = ap(t, d * .6, .8)
        text(c, "CHARLES PONZI", cx, dy + 380, 64, "serifb", "#ffe7a6", q, glow=12)
        c.drawCircle(cx + 240, dy + 640, 20, fill(GOLD))
        label(c, "SCHOOL STREET, BOSTON · AROUND THE END OF 1919", cx, 60, 26, seg(t, .1, 1.4))
        stamp(c, "REMEMBER THIS NAME", cx + 640, cy + 300, 44, seg(t, d * .8, d * .8 + .35), rot=-6, color="#e8b23a")
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        label(c, "THE OFFER", cx, 80, 30, seg(t, .1, 1.1))
        banknote(c, cx - 520, cy - 20, 360, rot=-4, a=ap(t, .2), txt="100")
        P = skia.Path(); P.moveTo(cx - 260, cy - 20); P.lineTo(cx + 180, cy - 20)
        c.drawPath(P, stroke(GOLD, 6, ap(t, .4)))
        P = skia.Path(); P.moveTo(cx + 180, cy - 45); P.lineTo(cx + 220, cy - 20); P.lineTo(cx + 180, cy + 5); P.close(); c.drawPath(P, fill(GOLD, ap(t, .4)))
        for k in range(3): banknote(c, cx + 520 + (k - 1) * 30, cy - 20 - k * 20, 300, rot=4 - k * 3, a=ap(t, .5 + k * .1), txt="50" if k == 2 else "50")
        text(c, "+50%", cx + 520, cy - 200, 100, "disp", GREEN, ap(t, .7))
        k = seg(t, d * .45, d * .55)
        text(c, "90 DAYS", cx - 40, cy + 170, 80, "disp", WHITE, ap(t, .5) * (1 - .6 * k))
        if k > 0: c.drawLine(cx - 230, cy + 145, cx + 160 * k + (-70) * (1 - k), cy + 145, stroke(RED, 10))
        text(c, "45 DAYS", cx, cy + 330, 110, "disp", GOLD, ap(t, d * .58))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        sea(ctx, t, H * .72)
        A = (cx - 650, H * .62); B = (cx + 650, H * .62)
        pin(c, A[0], A[1], 1.4, "BOSTON", 1); pin(c, B[0], B[1], 1.4, "EUROPE", 1)
        go = eio(seg(t, .2, d * .45)); bk = eio(seg(t, d * .45, d * .8))
        if bk <= 0:
            x, y = arc_pts(A, B, 260, 60)[int(go * 60)]
            banknote(c, x, y - 60, 180, rot=-8)
        else:
            x, y = arc_pts(B, A, 200, 60)[int(bk * 60)]
            banknote(c, x, y - 60, 180, rot=6)
            banknote(c, x + 120, y - 10, 90, rot=10); banknote(c, x + 190, y + 10, 80, rot=-6)
        text(c, "“A little dollar ... could come home in six weeks,", cx, 150, 44, "serif", WHITE, ap(t, .3))
        text(c, "married and with a couple of kids.”", cx, 215, 44, "serif", WHITE, ap(t, d * .4))
        text(c, "— CHARLES PONZI", cx, 290, 28, "sansb", GOLD, ap(t, d * .6), spacing=4)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        k = seg(t, d * .48, d * .56)
        def A():
            boater(c, cx, cy + 120, 1.0, rim=PONZI)
            for i in range(6):
                an = i / 6 * 2 * math.pi + .3; x = cx + math.cos(an) * 560; y = cy + math.sin(an) * 300
                q = ap(t, .3 + i * .2)
                c.drawLine(cx, cy - 20, x, y - 60, stroke(GOLD, 2, .4 * q))
                figure(c, x, y + 60, .55, a=q, hat=i % 2 == 0, rim=CROWD)
                chip(c, "10%", x + 90, y - 120, a=q, size=26)
            label(c, "SALES AGENTS", cx, 70, 30, seg(t, .1, 1.2))
        def B():
            card(c, cx - 360, cy, 440, 480, rot=-2, color="#f2ece0")
            c.drawRect(skia.Rect.MakeXYWH(0, 0, 440, 110), fill(RED))
            text(c, "DAY", 220, 75, 50, "sansb", WHITE, spacing=6)
            text(c, "45", 220, 330, 200, "disp", INK)
            c.restore()
            promissory(c, cx + 400, cy - 80, 560, rot=3, amount="$150")
            stamp(c, "PAID IN FULL", cx + 400, cy + 220, 70, seg(t, d * .72, d * .72 + .35), rot=-7, color=GREEN)
        xfade(c, k, A, B)
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        rnd = random.Random(5); n = 120; told = eo(seg(t, .2, d * .7))
        for i in range(n):
            x = cx - 840 + (i % 20) * 88 + rnd.uniform(-10, 10); y = 250 + (i // 20) * 90
            on = rnd.random() < told
            c.drawCircle(x, y, 16, fill(GOLD if on else "#3a4055", 1))
        text(c, "THEY TOLD THEIR FAMILIES · THEIR NEIGHBOURS", cx, 140, 38, "sansb", WHITE, ap(t, .2), spacing=2)
        chip(c, "MANY PUT IT ALL BACK IN", cx - 380, H - 250, a=ap(t, d * .35), size=34)
        reply_coupon(c, cx + 520, H - 200, 300, rot=4, a=ap(t, d * .65), lab=False)
        text(c, "pay for all of that?", cx + 520, H - 40, 44, "serifb", GOLD, ap(t, d * .75))
        c.restore()

# ------------------------------------------------------------------ how it really worked
def investor(c, x, y, s, a=1.0, rim=CROWD, name=""):
    figure(c, x, y, s, a=a, hat=True, rim=rim)
    if name: chip(c, name, x, y + 50, a=a, size=26, color=WHITE)
def sc_trick(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        text(c, "IT COULDN'T.", cx, cy - 120, 140, "disp", WHITE, ap(t, .1))
        label(c, "HOW IT REALLY WORKED · STEP BY STEP", cx, cy + 40, 34, seg(t, d * .35, d), GOLD)
        reply_coupon(c, cx, cy + 260, 260, rot=-3, a=ap(t, d * .3) * .5, lab=False)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        label(c, "STEP 1", cx, 70, 30, seg(t, .1, 1))
        investor(c, cx - 560, H - 130, 1.1, rim="#7fb3c9", name="INVESTOR A")
        boater(c, cx + 560, H - 60, 1.1, rim=PONZI)
        go = eio(seg(t, d * .15, d * .45))
        banknote(c, lerp(cx - 400, cx + 320, go), cy - 40, 220, rot=-4, txt="100")
        promissory(c, cx, cy + 160, 480, rot=-2, a=ap(t, d * .55), amount="$150", days="45")
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        label(c, "STEP 2 · 45 DAYS LATER", cx, 70, 30, seg(t, .1, 1))
        boater(c, cx, H - 60, 1.0, rim=PONZI)
        investor(c, cx + 520, cy + 40, .7, rim=CROWD, name="B"); investor(c, cx + 760, cy + 40, .7, rim=CROWD, name="C")
        q = eio(seg(t, .3, d * .35))
        banknote(c, lerp(cx + 520, cx + 120, q), lerp(cy - 140, cy - 40, q), 160, txt="100")
        banknote(c, lerp(cx + 760, cx + 150, q), lerp(cy - 140, cy - 10, q), 160, txt="100")
        r = eio(seg(t, d * .4, d * .7))
        for k in range(3): banknote(c, lerp(cx + 100, cx - 380, r) + k * 24, lerp(cy - 20, cy + 40, r) - k * 14, 160, txt="50")
        happy = ap(t, d * .72)
        investor(c, cx - 620, cy + 40, .9, rim=GREEN if happy > .5 else "#7fb3c9", name="A")
        text(c, "+$50!", cx - 620, cy - 290, 70, "disp", GREEN, happy)
        text(c, "paid with B and C's money", cx, cy - 300, 44, "serifb", GOLD, ap(t, d * .5))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        label(c, "STEP 3 · THE HOLE GETS DEEPER", cx, 70, 30, seg(t, .1, 1), RED)
        pyramid(c, cx, 200, 7, seg(t, .2, d * .85), red_from=5)
        rows = ("1", "2", "4", "8", "16", "32", "64")
        for i, s in enumerate(rows): text(c, s, cx - 820, 212 + i * 74, 34, "sansb", GOLD if i < 5 else RED, ap(t, .2 + i * d * .11), align="l")
        text(c, "owed: $300", cx + 640, 300, 52, "disp", WHITE, ap(t, .4))
        text(c, "faster and faster,", cx + 640, H - 160, 44, "serifb", WHITE, ap(t, d * .7))
        text(c, "forever", cx + 640, H - 90, 64, "disp", RED, ap(t, d * .82))
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        k = seg(t, d * .55, d * .63)
        def A():
            label(c, "POSTAL INSPECTORS", cx, 80, 30, seg(t, .1, 1.1), POST)
            text(c, "coupons sold in the whole world", cx - 760, 330, 40, "serifb", WHITE, ap(t, .3), align="l")
            bar(c, cx - 760, 360, 1500, 60, .06 * ap(t, .5), "#8a93ad")
            text(c, "coupons needed for his profits", cx - 760, 560, 40, "serifb", GOLD, ap(t, d * .2), align="l")
            bar(c, cx - 760, 590, 1500, 60, eo(seg(t, d * .22, d * .5)), RED)
            text(c, "NOWHERE NEAR", cx, 860, 80, "disp", RED, ap(t, d * .45))
        def B():
            boater(c, cx, cy - 90, .8, rim=PONZI)
            text(c, "“It was the old game", cx, cy + 40, 66, "serif", WHITE, 1)
            text(c, "of robbing Peter", cx, cy + 130, 72, "serifb", GOLD, ap(t, d * .66))
            text(c, "to pay Paul.”", cx, cy + 220, 72, "serifb", GOLD, ap(t, d * .7))
            text(c, "— PONZI, YEARS LATER", cx, cy + 300, 28, "sansb", WHITE, ap(t, d * .8), spacing=4)
        xfade(c, k, A, B)
        c.restore()

# ------------------------------------------------------------------ the money
def sc_money(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        n = int(800 * eo(seg(t, .2, d * .8)) ** 2)
        for i in range(n):
            c.drawCircle(cx - 860 + (i % 50) * 35, 200 + (i // 50) * 38, 11, fill(WHITE if i % 7 else GOLD, .9))
        chip(c, "~40,000 PEOPLE · BY ONE COUNT", cx, H - 80, a=ap(t, d * .6), size=40)
        label(c, "SLOWLY, THEN IN A FLOOD", cx, 90, 30, seg(t, .1, 1.3))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        notes_pile(ctx, seg(t, 0, d * .9), cx, cy + 300, n=26, w=300)
        c.drawRect(skia.Rect.MakeXYWH(cx - 600, cy - 250, 1200, 200), fill("#0d1016", .8))
        counter(c, 15000000 * eo(seg(t, .3, d * .8)), cx, cy - 110, 130, color=GOLD)
        label(c, "IN ABOUT 8 MONTHS · BY MOST ESTIMATES", cx, 110, 30, seg(t, .2, 1.4))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        villa(c, cx - 380, H * .62, .9, a=ap(t, .1))
        label(c, "LEXINGTON · 12 ROOMS · SERVANTS", cx - 380, 90, 26, seg(t, .1, 1.3))
        car(c, cx - 380 + 700 * eo(seg(t, d * .15, d * .4)) - 700, H * .86, 1.3, a=ap(t, d * .15))
        chip(c, "LIMOUSINE + CHAUFFEUR", cx - 380, H - 50, a=ap(t, d * .3), size=30)
        c.drawLine(cx + 360, cy + 300, cx + 420, cy - 120, stroke("#2a1c12", 12, ap(t, d * .4)))
        c.drawCircle(cx + 424, cy - 134, 22, fill(GOLD, ap(t, d * .4)))
        text(c, "gold-handled canes", cx + 400, cy + 360, 32, "serif", WHITE, ap(t, d * .45))
        gem(c, cx + 680, cy + 40, 70, a=ap(t, d * .5), shine=ap(t, d * .55))
        text(c, "diamonds for Rose", cx + 680, cy + 180, 32, "serif", WHITE, ap(t, d * .5))
        text(c, "“The more I bought, the more I wanted to buy.", cx + 440, 230, 36, "serif", WHITE, ap(t, d * .62))
        text(c, "It was a mania.”", cx + 440, 290, 46, "serifb", GOLD, ap(t, d * .8))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        bank(c, cx, H * .9, 900)
        boater(c, cx + 640, H + 20, 1.5, rim=PONZI, smile=1)
        chip(c, "1919: REFUSED HIM $2,000", cx - 600, 330, a=ap(t, d * .3), size=32, color=WHITE)
        stamp(c, "NOW HE RUNS IT", cx, 190, 70, seg(t, d * .55, d * .55 + .35), rot=-5, color="#e8b23a")
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        c.drawRect(skia.Rect.MakeXYWH(cx - 760, 150, 1520, 760), fill("#1d2a24"))
        c.drawRect(skia.Rect.MakeXYWH(cx - 760, 150, 1520, 760), stroke("#5a4630", 22, cap=False))
        ln = ("$100  x  1.5  =  $150", "every 45 days ...", "who pays?")
        for i, s in enumerate(ln):
            typed(c, s, cx - 640, 320 + i * 170, 70, seg(t, .3 + i * d * .22, .3 + i * d * .22 + d * .2), kind="type", color="#e9efe6")
        text(c, "THE ARITHMETIC", cx, 110, 40, "sansb", GOLD, ap(t, .1), spacing=6)
        c.restore()

# ------------------------------------------------------------------ the doubt
def sc_doubt(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        card(c, cx - 520, cy, 560, 440, rot=-3, a=ap(t, .1))
        text(c, "LAWSUIT", 280, 90, 40, "typeb", INK)
        typed(c, "Daniels v. Ponzi", 50, 190, 34, seg(t, .3, d * .25), color="#1d1a14")
        text(c, "$1,000,000", 280, 320, 72, "disp", RED, ap(t, d * .2))
        text(c, "RECONSTRUCTION", 50, 420, 13, "sansb", "#8c7d60", 1, align="l", spacing=3)
        c.restore()
        newspaper(ctx, cx + 360, cy + 20, 760, 640, 2, ["DOUBLES THE", "MONEY WITHIN", "THREE MONTHS"], "Boston Post headline, 24 July 1920", "THE BOSTON POST",
                  a=ap(t, d * .45), hp=seg(t, d * .45, d * .8))
        label(c, "JULY 1920", cx, 60, 28, seg(t, .1, 1.1))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        figure(c, cx - 600, H + 40, 1.4, hat=False, rim=POST, a=ap(t, .1))
        label(c, "RICHARD GROZIER · THE POST", cx - 600, 160, 24, seg(t, .1, 1.3), POST)
        figure(c, cx + 600, H + 40, 1.5, hat=False, wide=1.35, rim="#c9b37a", a=ap(t, d * .25))
        label(c, "CLARENCE BARRON · THE WALL STREET JOURNAL", cx + 420, 160, 24, seg(t, d * .25, d * .5), "#c9b37a")
        panel(c, cx, cy - 20, 900, 340, ap(t, d * .45))
        text(c, "“No man of wide financial", cx, cy - 90, 44, "serif", WHITE, ap(t, d * .5))
        text(c, "or investment experience", cx, cy - 30, 44, "serif", WHITE, ap(t, d * .55))
        text(c, "would look twice ...”", cx, cy + 30, 44, "serif", WHITE, ap(t, d * .6))
        text(c, "50% IN 3 MONTHS?", cx, cy + 110, 50, "disp", RED, ap(t, d * .75))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        figure(c, cx - 560, H + 40, 1.5, hat=True, rim="#b7a6d9", a=ap(t, .1))
        label(c, "WILLIAM McMASTERS · PUBLICITY MAN", cx - 560, 160, 24, seg(t, .1, 1.3), "#b7a6d9")
        panel(c, cx + 300, cy, 960, 460, ap(t, .3))
        text(c, "To calm things down:", cx + 300, cy - 140, 44, "serifb", WHITE, ap(t, d * .2))
        item(c, "OPEN THE BOOKS TO AN AUDITOR", cx - 120, cy - 20, 40, t, d * .4, ok=True)
        item(c, "TAKE NO NEW MONEY", cx - 120, cy + 90, 40, t, d * .7, ok=True)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        sun_heat(ctx, t=t)
        street(ctx, lit=.3)
        n = int(3 + 15 * eo(seg(t, d * .3, d * .95)))
        queue(c, W * .7, W * .7 - n * 95, H * .86, n, h=250, t=t, papers=1)
        clock(c, 200, 200, 110, 12, 0)
        stamp(c, "NO NEW MONEY", W * .6, 330, 56, seg(t, d * .15, d * .15 + .35), rot=-6)
        label(c, "MONDAY 26 JULY · NOON", cx - 150, 70, 28, seg(t, .1, 1.2))
        chip(c, "THE SAME LINE", cx - 300, 330, a=ap(t, d * .55), size=36)
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        k = seg(t, d * .45, d * .53)
        def A():
            notes_pile(ctx, seg(t, 0, d * .45), cx, cy + 300, n=20, w=260)
            c.drawRect(skia.Rect.MakeXYWH(cx - 620, cy - 260, 1240, 230), fill("#0d1016", .8))
            counter(c, 1000000 * eo(seg(t, .3, d * .4)), cx, cy - 120, 120, suffix="+")
            label(c, "PAID OUT IN ONE DAY · THE POST REPORTED", cx, cy - 330, 28, seg(t, .2, 1.3))
        def B():
            boater(c, cx - 600, H + 40, 1.6, rim=PONZI, smile=1)
            text(c, "“My secret is how to cash", cx + 260, cy - 120, 54, "serif", WHITE)
            text(c, "the coupons.", cx + 260, cy - 50, 54, "serif", WHITE)
            text(c, "Let the United States", cx + 260, cy + 60, 60, "serifb", GOLD, ap(t, d * .7))
            text(c, "find it out, if it can.”", cx + 260, cy + 130, 60, "serifb", GOLD, ap(t, d * .75))
        xfade(c, k, A, B)
        c.restore()

# ------------------------------------------------------------------ the unravelling
def sc_unravel(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        newspaper(ctx, cx - 380, cy + 20, 820, 680, -2, ["HOPELESSLY", "INSOLVENT"], "says Ponzi's own publicity man", "THE BOSTON POST · 2 AUGUST 1920",
                  a=ap(t, .1), hp=seg(t, .3, d * .3))
        text(c, "DEBT", cx + 560, 250, 40, "sansb", WHITE, ap(t, d * .3), spacing=6)
        counter(c, 2000000 * eo(seg(t, d * .35, d * .55)), cx + 560, 380, 84, color=RED, suffix="+")
        text(c, "with interest", cx + 560, 560, 36, "serif", WHITE, ap(t, d * .7))
        counter(c, 4500000 * eo(seg(t, d * .72, d * .92)), cx + 560, 680, 96, color=RED)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        boater(c, cx, H + 40, 1.8, rim=PONZI)
        stamp(c, "I'LL SUE", cx - 520, 260, 70, seg(t, .2, .55), rot=-8)
        crowd(c, cx, H + 40, n=11, s=.6, spread=170, rim=GOLD, t=t)
        text(c, "many still believe him", cx + 480, 260, 44, "serifb", WHITE, ap(t, d * .35))
        text(c, "THEN ...", cx, 140, 80, "disp", RED, ap(t, d * .75))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        card(c, cx - 360, cy, 840, 540, rot=-1.5, a=ap(t, .1), color="#f0e3bf")
        text(c, "TELEGRAM · MONTREAL", 420, 80, 34, "typeb", INK)
        typed(c, "ABOUT TEN YEARS AGO", 60, 180, 38, seg(t, .3, d * .2), kind="typeb", color="#1d1a14")
        typed(c, "CHARLES PONSI JAILED HERE", 60, 250, 38, seg(t, d * .2, d * .4), kind="typeb", color="#1d1a14")
        typed(c, "FOR FORGERY", 60, 320, 38, seg(t, d * .4, d * .5), kind="typeb", color="#1d1a14")
        text(c, "RECONSTRUCTION", 60, 510, 13, "sansb", "#8c7d60", 1, align="l", spacing=3)
        c.drawCircle(60 + tw("CHARLES PONS", "typeb", 38) + 10, 238, 30, stroke(RED, 5, ap(t, d * .45)))
        c.restore()
        text(c, "with an S", cx - 120, cy + 330, 36, "serif", GOLD, ap(t, d * .45))
        boater(c, cx + 600, H + 40, 1.4, rim=PONZI, smile=1)
        text(c, "“I might have.”", cx + 560, 220, 64, "serifb", GOLD, ap(t, d * .75))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        k = seg(t, d * .62, d * .7)
        def A():
            mugshot(c, cx - 300, cy + 20, 440, rot=-3, moustache=eo(seg(t, d * .2, d * .35)))
            text(c, "add a moustache ...", cx + 380, cy - 140, 52, "serifb", WHITE, ap(t, d * .15))
            text(c, "“Bianchi, the snake!”", cx + 380, cy + 20, 64, "serifb", GOLD, ap(t, d * .4))
            text(c, "— A MONTREAL WITNESS", cx + 380, cy + 100, 28, "sansb", WHITE, ap(t, d * .45), spacing=4)
        def B():
            newspaper(ctx, cx, cy + 30, 900, 760, 1.5, ["CANADIAN 'PONSI'", "SERVED JAIL TERM"], "Boston Post headline, 11 August 1920", "THE BOSTON POST",
                      hp=seg(t, d * .68, d * .9))
            mugshot(c, cx + 520, cy + 260, 240, rot=6)
        xfade(c, k, A, B)
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        k = seg(t, d * .5, d * .58)
        def A():
            ledger(c, cx, cy + 20, 1000, 660, rows=(("GOVERNMENT AUDIT", "", INK), ("deficit", "$3,000,000", RED), ("revised", "$7,000,000", RED)), p=seg(t, .2, d * .45))
            label(c, "12 AUGUST 1920", cx, 70, 28, seg(t, .1, 1.1))
        def B():
            boater(c, cx, H + 40, 1.9, rim=PONZI, smile=1)
            for i in range(9): c.drawRect(skia.Rect.MakeXYWH(cx - 760 + i * 190, 0, 26, H), fill("#2a2e3a"))
            stamp(c, "ARRESTED", cx, 200, 90, seg(t, d * .55, d * .55 + .35), rot=-7)
            text(c, "“The man's nerve is iron.”", cx, H - 70, 56, "serifb", GOLD, ap(t, d * .8))
        xfade(c, k, A, B)
        c.restore()
    t, a, d = beat(ctx, 5)
    if a > 0:
        c.drawCircle(cx, cy, 440, fill("#ffe2a0", .06, 120))
        for k in range(5): reply_coupon(c, cx - 180 + k * 90, cy + 40 - k * 16, 300, rot=-12 + k * 6, a=ap(t, .2 + k * .1), lab=False)
        text(c, "$61", cx, 230, 170, "disp", GOLD, ap(t, d * .3))
        text(c, "worth of coupons, by one account", cx, H - 90, 46, "serifb", WHITE, ap(t, d * .45))
        c.restore()

# ------------------------------------------------------------------ after
def sc_after(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        bank(c, cx - 420, H * .62, 620, crack=seg(t, .2, d * .3))
        stamp(c, "FAILED", cx - 420, 500, 70, seg(t, d * .25, d * .25 + .35), rot=-8)
        for k in range(5): bank(c, cx + 180 + (k % 3) * 260, 380 + (k // 3) * 250, 160, a=ap(t, d * .3 + k * .15), name="BANK", crack=seg(t, d * .35 + k * .15, d * .5 + k * .15))
        text(c, "about half a dozen banks", cx + 430, 650, 34, "serif", WHITE, ap(t, d * .45))
        bar(c, cx - 760, H - 180, 1520, 46, .3 * eo(seg(t, d * .6, d * .85)), RED)
        text(c, "NOTE HOLDERS GOT BACK LESS THAN 30¢ ON THE DOLLAR", cx, H - 70, 40, "sansb", WHITE, ap(t, d * .6))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        card(c, cx, cy, 1080, 600, rot=-1, a=ap(t, .1))
        text(c, "UNITED STATES v. PONZI", 540, 100, 44, "typeb", INK)
        typed(c, "Charge: using the mails to defraud", 80, 220, 38, seg(t, .3, d * .3), color="#1d1a14")
        typed(c, "Plea: guilty", 80, 300, 38, seg(t, d * .3, d * .45), color="#1d1a14")
        text(c, "5 YEARS", 540, 450, 110, "disp", RED, ap(t, d * .5))
        typed(c, "served: about three and a half", 80, 540, 34, seg(t, d * .75, d * .9), color="#5a4d38")
        c.restore()
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        steps = (("STATE TRIAL", "convicted again"), ("FLORIDA", "swampland, new name"), ("ITALIAN SHIP", "signed on as a sailor"), ("NEW ORLEANS", "caught"))
        for i, (h, s) in enumerate(steps):
            x = cx - 690 + i * 460; q = ap(t, .2 + i * d * .2)
            c.drawCircle(x, cy - 60, 70, fill(RED if i == 3 else GOLD, q)); text(c, str(i + 1), x, cy - 35, 70, "disp", INK, q)
            text(c, h, x, cy + 80, 36, "sansb", GOLD if i < 3 else RED, q, spacing=2); text(c, s, x, cy + 130, 30, "serif", WHITE, q)
            if i < 3: c.drawLine(x + 90, cy - 60, x + 370, cy - 60, stroke(GOLD, 4, ap(t, .4 + i * d * .2)))
        palm(c, cx - 230, cy - 150, .5, a=ap(t, d * .22) * .6, t=t)
        label(c, "OUT ON BAIL", cx, 120, 30, seg(t, .1, 1.1))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        liner(ctx, t, d, lab="7 OCTOBER 1934 · DEPORTED TO ITALY")
        chip(c, "BALDING · 40 POUNDS HEAVIER · NEVER A CITIZEN", cx, 220, a=ap(t, d * .25), size=32, color=WHITE)
        text(c, "Rose stayed behind", cx, H - 60, 40, "serifb", GOLD, ap(t, d * .7))
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        c.drawCircle(cx - 380, cy, 260, fill(GOLD, .18, 60))
        c.drawCircle(cx - 380, cy, 220, fill(GOLD, ap(t, .2))); c.drawCircle(cx - 380, cy, 190, stroke("#8a6a2a", 6, ap(t, .2)))
        text(c, "1921", cx - 380, cy + 30, 90, "disp", "#3a2a10", ap(t, .3))
        newspaper(ctx, cx + 420, cy + 20, 640, 560, 2, ["PULITZER", "PRIZE"], "for the exposure of Charles Ponzi", "THE BOSTON POST", a=ap(t, d * .3), hp=seg(t, d * .3, d * .6))
        c.restore()

# ------------------------------------------------------------------ the end
def sc_end(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        route(ctx, seg(t, d * .2, d * .7), "ITALY", "RIO DE JANEIRO", sp=560)
        label(c, "ACCOUNTS DIFFER", cx, 90, 30, seg(t, .1, 1.1), RED)
        chip(c, "BY ONE ACCOUNT: AN ITALY–BRAZIL AIRLINE", cx, H - 160, a=ap(t, d * .3), size=32, color=WHITE)
        chip(c, "A STROKE · FAILING EYESIGHT", cx, H - 70, a=ap(t, d * .7), size=32)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        card(c, cx - 380, cy, 620, 480, rot=-1.5, a=ap(t, .1))
        text(c, "CHARLES PONZI", 310, 130, 46, "serifb", INK)
        text(c, "1882 – 1949", 310, 230, 62, "disp", INK)
        text(c, "died 18 January 1949", 310, 310, 32, "serif", "#3b3324")
        text(c, "charity hospital · Rio de Janeiro", 310, 360, 30, "serif", "#3b3324")
        c.restore()
        text(c, "$75", cx + 480, cy, 200, "disp", GOLD, ap(t, d * .55))
        text(c, "left to pay for his burial", cx + 480, cy + 90, 40, "serifb", WHITE, ap(t, d * .6))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        text(c, "$2.50", cx - 600, cy - 80, 140, "disp", GOLD, ap(t, .1))
        text(c, "+ $1,000,000 in hopes", cx - 600, cy, 34, "serif", WHITE, ap(t, .3))
        text(c, "$75", cx + 600, cy - 80, 140, "disp", GOLD, ap(t, d * .25))
        text(c, "1903", cx - 600, cy + 80, 34, "sansb", WHITE, ap(t, .3), spacing=4)
        text(c, "1949", cx + 600, cy + 80, 34, "sansb", WHITE, ap(t, d * .25), spacing=4)
        reply_coupon(c, cx, cy - 60, 320, rot=-4, a=ap(t, d * .5), glow=ap(t, d * .6), lab=False)
        queue(c, cx + 700, cx - 700, H * .97, 16, h=200, papers=1, a=ap(t, d * .55))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        k = seg(t, d * .55, d * .62)
        def A():
            pyramid(c, cx, 180, 6, seg(t, .1, d * .5))
            text(c, "older than he was", cx, H - 120, 56, "serifb", WHITE, ap(t, d * .2))
        def B():
            pyramid(c, cx, 180, 6, 1, a=.35)
            c.drawCircle(cx, cy, 520, fill("#ffcf7a", .06, 120))
            text(c, "BUT IT TOOK HIS NAME", cx, 150, 60, "disp", WHITE, 1)
            stamp(c, "PONZI SCHEME", cx, cy + 40, 130, seg(t, d * .7, d * .7 + .35), rot=-6)
        xfade(c, k, A, B)
        c.restore()

def sc_outro(ctx):
    c, cx, cy, t = ctx.c, ctx.cx, ctx.cy, ctx.t
    stamp(c, "CASE CLOSED", cx, cy - 110, 150, seg(t, .15, .45), rot=-5)
    label(c, "CASE CLOSED FILES", cx, cy + 110, 30, seg(t, .6, 1.4), GOLD)
    text(c, "New case every week. Subscribe so you don't miss it.", cx, cy + 210, 40, "serif", WHITE, ap(t, 1.1))

SCENES = {k[3:]: v for k, v in list(globals().items()) if k.startswith("sc_") and callable(v)}
HITS = [("cold", 3, 0, .55), ("arrival", 3, 0, .4), ("arrival", 3, 0, .8), ("arrival", 4, 0, .52), ("letter", 0, 0, .57), ("letter", 0, 0, .84),
        ("company", 0, 0, .82), ("company", 3, 0, .74), ("money", 3, 0, .57), ("doubt", 3, 0, .17), ("unravel", 1, 0, .22),
        ("unravel", 4, 0, .57), ("after", 0, 0, .27), ("end", 3, 0, .72), ("outro", -1, .15, 0)]
SHORT_HITS = []
WARM = {}

THUMB_WORDS = [(["50% IN", "45 DAYS"], 130), (["ALL", "FAKE."], 170), (["PAID WITH", "YOUR MONEY"], 120)]
def thumbnail(c, W, H, word):
    word, size = word
    sh = skia.GradientShader.MakeRadial(center=(W * .55, H * .5), radius=900, colors=[col("#3a3424"), col("#1a1a22"), col("#07080b")], positions=[0, .5, 1])
    c.drawPaint(skia.Paint(Shader=sh))
    c.drawCircle(W * .5, H * .58, 330, fill("#ffcf7a", .16, 90))
    reply_coupon(c, W * .48, H * .62, 520, rot=-8, lab=False)
    big_word(c, "5¢", W * .17, H * .86, 190, "#ffd36b")
    boater(c, W * .84, H * 1.08, 1.9, rim=GOLD, smile=1)
    for i, ln in enumerate(word):
        sz = size
        while tw(ln, "sansb", sz) > 520: sz -= 6
        big_word(c, ln, W * .22, H * .2 + i * size * 1.0, sz, "#ffd36b" if i == len(word) - 1 else "#ffffff")


# ---------------- the Short (60-100 s, 9:16) ----------------
from shorts import hook_card, cta_card
def _art(c, cx, cy, t, d):
    q = .9 * eo(seg(t, 0, .8)); reply_coupon(c, cx, cy + 210, 360, rot=-6, a=q, lab=False, glow=q)
SCENES["hook_a"] = hook_card(["50% PROFIT", "IN 45 DAYS.", "FROM A 5¢ COUPON."], stamp_text="BOSTON 1920", prop=_art)
SCENES["cta_a"] = cta_card("CASE 006 · PONZI", "FULL CASE")
SHORT_HITS += [("hook_a", -1, .15, .62)]
SHORT_VIEW = {}
