from lib import *

MAC = GOLD          # MacGregor's rim colour
COLD = "#8fa0c8"    # officials / others
GREEN_F = "#2f7a45"
def beat(ctx, i):
    t, a, d = ctx.ph(i)
    if a > 0: ctx.layer(a)
    return t, a, d
def mac(c, x, y, s, a=1.0, rim=MAC, bow=0.0, hat=False): figure(c, x, y, s, a=a, hat=hat, rim=rim, bow=bow)
def xfade(c, k, draw_a, draw_b):
    """crossfade inside a beat: k 0..1"""
    if k < 1:
        c.saveLayerAlpha(None, int(255 * (1 - k))); draw_a(); c.restore()
    if k > 0:
        c.saveLayerAlpha(None, int(255 * k)); draw_b(); c.restore()
def settlers(c, cx, y, n=7, s=.9, a=1.0, spread=240, bow=0.0, rim="#2b3044"):
    for i in range(n): figure(c, cx - (n - 1) * spread / 2 + i * spread, y, s, hat=i % 3 == 0, rim=rim, a=a, bow=bow)
def torch(c, x, y, t, a=1.0):
    c.drawLine(x, y, x + 10, y - 90, stroke("#3a2a1a", 8, a))
    f = 1 + .15 * math.sin(t * 13 + x)
    c.drawCircle(x + 10, y - 100, 60 * f, fill("#ffb45e", .25 * a, 30)); c.drawCircle(x + 10, y - 100, 14 * f, fill("#ffd28a", a))

# ------------------------------------------------------------------ cold open
def sc_cold(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        c.drawCircle(W * .6, H * .17, 54, fill("#f1e6c8", .9)); c.drawCircle(W * .6, H * .17, 190, fill("#f1e6c8", .08, 60))
        sailship(c, lerp(cx - 560, cx - 400, t / d), H * .7, 1.15, t=t, flag="poyais")
        sea(ctx, t, H * .7 + 18)
        label(c, "MARCH 1823 · THE MOSQUITO COAST", 120, 140, 30, seg(t, .2, 1.6), align="l")
        text(c, "NEARLY 200", W - 140, 230, 96, "disp", GOLD, ap(t, d * .4), align="r")
        text(c, "settlers, and one guidebook", W - 140, 285, 32, "serif", WHITE, ap(t, d * .5) * .85, align="r")
        guidebook(c, W - 330, cy + 120, 170, rot=6, a=ap(t, d * .7))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        city_mirage(c, cx, H * .8, p=seg(t, .2, d * .5))
        label(c, "AS ADVERTISED · ST. JOSEPH", cx, 120, 30, seg(t, .1, 1.3))
        for i, (s, x) in enumerate((("CATHEDRAL", cx - 150), ("BANK", cx + 490), ("OPERA HOUSE", cx + 200))):
            label(c, s, x, H * .8 + 50, 24, seg(t, d * (.3 + i * .12), d * (.3 + i * .12) + .8), WHITE, rule=False)
        q = seg(t, d * .7, d * .95)
        if q > 0: poyais_note(c, lerp(cx - 1100, cx - 560, eo(q)), cy - 160, 380, rot=lerp(-20, -6, q))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        jungle(ctx, t)
        city_mirage(c, cx, H * .78, a=.6 * (1 - seg(t, .2, d * .35)))
        for i, x in enumerate((cx - 420, cx - 80, cx + 300)):
            figure(c, x, H + 60, .95, hat=i == 1, rim="#4a5a50"); torch(c, x + 120, H * .9, t)
        text(c, "Only jungle.", cx, 150, 64, "serifb", WHITE, ap(t, d * .3))
        text(c, "WHERE IS POYAIS?", cx, 260, 92, "disp", GOLD, ap(t, d * .72))
        c.restore()

def sc_title(ctx):
    c, cx, cy, t = ctx.c, ctx.cx, ctx.cy, ctx.t
    poyais_flag(c, cx - 450, cy - 280, 900, a=.06, t=t)
    label(c, "CASE CLOSED FILES  ·  NO. 003", cx, cy - 190, 26, seg(t, .1, .7))
    text(c, "THE CON MAN WHO", cx, cy - 40 + (1 - ap(t, .2, .6)) * 30, 128, "disp", WHITE, ap(t, .2, .6), spacing=4)
    text(c, "INVENTED A COUNTRY", cx, cy + 110 + (1 - ap(t, .5, .6)) * 30, 134, "disp", GOLD, ap(t, .5, .6), spacing=4)
    text(c, "A true story · London and the Mosquito Coast, 1820–1823", cx, cy + 220, 34, "serif", WHITE, ap(t, 1.0) * .8)

# ------------------------------------------------------------------ who
def sc_who(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        w, h = 1300, 620; card(c, cx, cy + (1 - ap(t, 0, .7)) * 80, w, h, rot=-1.0)
        text(c, "DOSSIER", 60, 80, 40, "sansb", INK, align="l", spacing=10); text(c, "FILE 003", w - 60, 80, 22, "type", "#5a4d38", align="r")
        c.drawLine(60, 104, w - 60, 104, stroke(INK, 2, cap=False))
        c.drawRect(skia.Rect.MakeXYWH(60, 140, 340, 420), fill("#1b1e29"))
        c.save(); c.clipRect(skia.Rect.MakeXYWH(60, 140, 340, 420)); mac(c, 230, 590, 1.25); c.restore()
        rows = [("NAME", "Gregor MacGregor", .8), ("BORN", "1786, Scotland", d * .3), ("TRADE", "Soldier", d * .5), ("CLAIMED", "Descent from Rob Roy", d * .7)]
        for i, (k, v, ts) in enumerate(rows):
            y = 190 + i * 100
            text(c, k, 460, y, 18, "sansb", "#7a6a4c", ap(t, ts - .3), align="l", spacing=4)
            typed(c, v, 460, y + 44, 38, seg(t, ts, ts + .9), color="#1d1a14", cursor=True)
        c.restore(); c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        mac(c, cx - 560, H + 40, 2.0)
        x = cx - 120
        item(c, "BRITISH ARMY · AGE 16", x, cy - 210, 44, t, .3, ok=True)
        item(c, "THE WAR AGAINST NAPOLEON", x, cy - 100, 44, t, d * .2, ok=True)
        item(c, "SOUTH AMERICA · WITH BOLÍVAR", x, cy + 10, 44, t, d * .45, ok=True, color=GOLD)
        item(c, "MARRIED BOLÍVAR'S COUSIN", x, cy + 120, 44, t, d * .78, ok=True)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        k = seg(t, d * .4, d * .48)
        def A():
            chip(c, "1816 · A 34-DAY RETREAT", cx, cy - 200, size=48)
            text(c, "“superior to the conquest", cx, cy - 20, 64, "serifb", WHITE, ap(t, d * .12))
            text(c, "of an empire”", cx, cy + 70, 64, "serifb", WHITE, ap(t, d * .2))
            text(c, "— Simón Bolívar", cx, cy + 150, 34, "serif", GOLD, ap(t, d * .26))
        def B():
            sailship(c, lerp(cx + 100, cx + 700, eo(seg(t, d * .55, d))), H * .66, .8, t=t)
            sea(ctx, t, H * .66 + 14)
            label(c, "1819 · PORTO BELLO, PANAMA", 120, 140, 30, seg(t, d * .45, d * .45 + 1.2), align="l")
            for i in range(6): figure(c, 160 + i * 120, H * .66 + 30, .55, hat=False, rim="#4a5a70", a=.9)
            stamp(c, "ABOUT 200 MEN LEFT BEHIND", cx - 140, 300, 60, seg(t, d * .8, d * .8 + .35), rot=-5)
        xfade(c, k, A, B)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        c.drawCircle(cx + 200, cy, 300, fill("#2c5a8a", .18, 80))
        P = skia.Path(); P.moveTo(cx + 120, cy + 260); P.cubicTo(cx + 60, cy + 80, cx + 100, cy - 120, cx + 190, cy - 280); P.cubicTo(cx + 230, cy - 120, cx + 250, cy + 80, cx + 200, cy + 260); P.close()
        c.drawPath(P, fill("#1c2a22", ap(t, .2))); c.drawPath(P, stroke(GOLD, 3, ap(t, .2)))
        pin(c, cx + 170, cy - 40, 1.5, "", seg(t, .4, 1.4))
        label(c, "AMELIA ISLAND · FLORIDA · 1817", cx + 200, cy - 380, 28, seg(t, .4, 1.6))
        q = seg(t, d * .45, d * .7)
        c.drawLine(cx + 260, cy - 60, cx + 260, cy - 60 - 260 * eo(q), stroke("#c9c2b0", 6))
        if q > 0: poyais_flag(c, cx + 263, cy - 60 - 260 * eo(q), 150, t=t)
        text(c, "A new republic.", cx - 460, cy - 60, 64, "serifb", WHITE, ap(t, d * .15))
        text(c, "Gone in months.", cx - 460, cy + 30, 52, "serif", WHITE, ap(t, d * .35))
        text(c, "Remember that flag.", cx - 460, cy + 150, 52, "serifb", GOLD, ap(t, d * .75))
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        mac(c, cx - 420, H + 40, 2.1, rim=MAC)
        text(c, "When things go wrong,", cx + 300, cy - 110, 62, "serifb", WHITE, ap(t, .2))
        text(c, "MacGregor leaves.", cx + 300, cy - 20, 76, "serifb", GOLD, ap(t, d * .35))
        stamp(c, "REMEMBER THIS", cx + 300, cy + 170, 74, seg(t, d * .6, d * .6 + .35), rot=-5, color="#e8b23a")
        c.restore()

# ------------------------------------------------------------------ grant
def coast(ctx, a=1.0, hi=0.0):
    """Stylised Central American coast with the Mosquito Coast highlighted."""
    c = ctx.c; cx, cy = ctx.cx, ctx.cy
    for i in range(-6, 7): c.drawLine(cx + i * 150, cy - 420, cx + i * 150 + 40, cy + 420, stroke("#ffffff", 1, .05 * a, cap=False))
    P = skia.Path(); P.moveTo(cx - 900, cy - 300); P.cubicTo(cx - 600, cy - 260, cx - 300, cy - 200, cx - 60, cy - 170)
    P.cubicTo(cx + 150, cy - 150, cx + 260, cy - 120, cx + 330, cy - 40); P.cubicTo(cx + 380, cy + 80, cx + 350, cy + 230, cx + 420, cy + 420)
    P.lineTo(cx - 900, cy + 420); P.close()
    c.drawPath(P, fill("#1c2a22", a)); c.drawPath(P, stroke("#3b5a48", 3, a))
    if hi > 0:
        Q = skia.Path(); Q.moveTo(cx - 160, cy - 178); Q.cubicTo(cx + 150, cy - 150, cx + 260, cy - 120, cx + 330, cy - 40)
        Q.cubicTo(cx + 370, cy + 60, cx + 360, cy + 160, cx + 370, cy + 220); Q.lineTo(cx + 120, cy + 200); Q.lineTo(cx - 100, cy - 60); Q.close()
        c.drawPath(Q, fill(GOLD, .35 * a * hi)); c.drawPath(Q, stroke(GOLD, 4, a * hi))
    text(c, "CARIBBEAN SEA", cx + 640, cy - 200, 26, "sansb", "#6f86a8", a * .8, spacing=6)

def sc_grant(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        coast(ctx, hi=seg(t, d * .45, d * .65))
        pin(c, cx + 330, cy - 40, 1.4, "", seg(t, .3, 1.3))
        label(c, "MOSQUITO COAST", cx + 420, cy + 10, 30, seg(t, .3, 1.5), align="l", rule=False)
        label(c, "APRIL 1820", 120, 140, 30, seg(t, .2, 1.2), align="l")
        n = int(8000000 * eo(seg(t, d * .5, d * .75)))
        text(c, f"{n:,} ACRES", cx - 380, cy + 260, 84, "disp", GOLD, ap(t, d * .5))
        text(c, "about. Larger than Wales.", cx - 380, cy + 330, 38, "serif", WHITE, ap(t, d * .8))
        label(c, "KING GEORGE FREDERIC AUGUSTUS OF THE MISKITO", cx, 110, 24, seg(t, d * .2, d * .2 + 1.4), WHITE, rule=False)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        # rum bottle + jewels
        bx = cx - 520; by = cy + 160
        c.drawRoundRect(skia.Rect.MakeXYWH(bx - 70, by - 260, 140, 260), 30, 30, fill("#5a3218", ap(t, .2)))
        c.drawRect(skia.Rect.MakeXYWH(bx - 22, by - 360, 44, 110), fill("#5a3218", ap(t, .2)))
        c.drawRect(skia.Rect.MakeXYWH(bx - 60, by - 190, 120, 80), fill(PAPER, ap(t, .2))); text(c, "RUM", bx, by - 138, 34, "sansb", INK, ap(t, .2))
        for k, colr in enumerate(("#c0392b", "#2e86c1", "#d4a94e", "#27ae60")):
            q = ap(t, .5 + k * .2)
            P = skia.Path(); x0 = bx + 160 + k * 70; y0 = by - 30
            P.moveTo(x0, y0 - 30); P.lineTo(x0 + 26, y0); P.lineTo(x0, y0 + 30); P.lineTo(x0 - 26, y0); P.close(); c.drawPath(P, fill(colr, q))
        text(c, "REPORTEDLY", bx + 60, by + 90, 34, "sansb", GOLD, ap(t, d * .15))
        text(c, "Did the king know", cx + 360, cy - 140, 56, "serifb", WHITE, ap(t, d * .3))
        text(c, "exactly what he was doing?", cx + 360, cy - 60, 56, "serifb", WHITE, ap(t, d * .36))
        text(c, "Some historians say yes.", cx + 360, cy + 30, 40, "serif", GOLD, ap(t, d * .48))
        solid_stamp(c, "THE LAND WAS REAL", cx + 360, cy + 200, 60, rot=-4, color="#2f7a45") if t > d * .72 else None
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        k = seg(t, d * .35, d * .45)
        def A():
            mac(c, cx - 380, H + 40, 1.8, rim="#6f7c8f")
            label(c, "A SOLDIER WITH A PATCH OF JUNGLE?", cx + 300, cy - 40, 30, seg(t, .2, 1.4), WHITE, rule=False)
        def B():
            c.drawCircle(cx - 380, cy - 40, 420, fill(GOLD, .1, 100))
            mac(c, cx - 380, H + 40, 2.1, rim=GOLD)
            poyais_flag(c, cx - 820, 140, 220, t=t)
            text(c, "THE CAZIQUE", cx + 380, cy - 80, 100, "disp", GOLD, ap(t, d * .45))
            text(c, "OF POYAIS", cx + 380, cy + 30, 100, "disp", GOLD, ap(t, d * .52))
            label(c, "RULER OF AN “INDEPENDENT COUNTRY”", cx + 380, cy + 150, 28, seg(t, d * .7, d * .7 + 1.4), WHITE, rule=False)
        xfade(c, k, A, B)
        c.restore()

# ------------------------------------------------------------------ sell
def arms(c, x, y, s=1.0, a=1.0):
    """Invented coat of arms: shield with green cross, two unicorn-ish supporters (simple silhouettes)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    P = skia.Path(); P.moveTo(-90, -110); P.lineTo(90, -110); P.lineTo(90, 10); P.cubicTo(90, 80, 20, 110, 0, 130); P.cubicTo(-20, 110, -90, 80, -90, 10); P.close()
    c.drawPath(P, fill("#f2efe6", a)); c.save(); c.clipPath(P, True)
    c.drawRect(skia.Rect.MakeXYWH(-16, -120, 32, 260), fill(GREEN_F, a)); c.drawRect(skia.Rect.MakeXYWH(-100, -30, 200, 32), fill(GREEN_F, a)); c.restore()
    c.drawPath(P, stroke(GOLD, 6, a))
    c.drawCircle(0, -150, 26, stroke(GOLD, 5, a)); c.drawLine(-60, -150, -30, -150, stroke(GOLD, 4, a)); c.drawLine(30, -150, 60, -150, stroke(GOLD, 4, a))
    c.restore()

def sc_sell(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        poyais_flag(c, cx - 820, 150, 300, t=t, a=ap(t, .2))
        arms(c, cx - 670, cy + 160, 1.3, a=ap(t, d * .15))
        label(c, "COAT OF ARMS", cx - 670, cy + 380, 24, seg(t, d * .15, d * .15 + 1), WHITE, rule=False)
        for i, s in enumerate(("AN ARMY", "A GOVERNMENT", "A BANK")):
            chip(c, s, cx - 40 + i * 330, 200, a=ap(t, d * (.3 + i * .08)), size=36)
        city_mirage(c, cx + 220, H * .86, p=seg(t, d * .55, d * .9), a=1)
        text(c, "ST. JOSEPH · UP TO 20,000 PEOPLE", cx + 220, H - 60, 40, "sansb", GOLD, ap(t, d * .7))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        guidebook(c, cx - 420, cy + 20, 470, rot=-3, a=ap(t, .1))
        x = cx + 140
        label(c, "EDINBURGH & LONDON · 1822", x, cy - 260, 26, seg(t, .3, 1.4), align="l")
        text(c, "355 pages", x, cy - 150, 64, "serifb", WHITE, ap(t, d * .2), align="l")
        text(c, "“Capt. Thomas Strangeways”", x, cy - 60, 46, "serif", WHITE, ap(t, d * .4), align="l")
        text(c, "Probably MacGregor himself,", x, cy + 60, 44, "serifb", GOLD, ap(t, d * .62), align="l")
        text(c, "or someone close to him.", x, cy + 120, 44, "serifb", GOLD, ap(t, d * .7), align="l")
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        w, h = 1240, 760; card(c, cx + 120, cy + 20, w, h, rot=.8)
        text(c, "WHAT THE GUIDEBOOK PROMISED", w / 2, 80, 40, "sansb", INK, spacing=4); c.drawLine(80, 110, w - 80, 110, stroke(INK, 2, cap=False))
        rows = [("“remarkably healthy” climate", .1), ("three harvests of maize a year", .25), ("one day's hunting feeds a family for a week", .4),
                ("rivers with “globules of pure gold”", .57), ("moonlight bright enough to read by", .74)]
        for i, (s, f) in enumerate(rows):
            y = 200 + i * 100; q = seg(t, d * f, d * f + .5)
            if q > 0: c.drawCircle(100, y - 12, 12, fill(GOLD, eo(q))); typed(c, s, 136, y, 40, q * 1.4, color="#1d1a14")
        text(c, "QUOTED FROM THE 1822 GUIDEBOOK", w - 60, h - 30, 14, "sansb", "#8c7d60", align="r", spacing=3)
        c.restore()
        guidebook(c, cx - 760, cy + 200, 200, rot=-8)
        stamp(c, "SALES PITCH", cx + 520, cy + 330, 70, seg(t, d * .9, d * .9 + .3), rot=-6)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        for i, s in enumerate(("LONDON", "EDINBURGH", "GLASGOW")):
            x = cx - 560 + i * 560; q = ap(t, .3 + i * .5)
            c.drawRoundRect(skia.Rect.MakeXYWH(x - 210, 120, 420, 120), 14, 14, fill("#1f2433", q)); c.drawRoundRect(skia.Rect.MakeXYWH(x - 210, 120, 420, 120), 14, 14, stroke(GOLD, 3, q))
            text(c, "POYAIS LAND OFFICE", x, 165, 22, "sansb", GOLD, q, spacing=3); text(c, s, x, 215, 40, "disp", WHITE, q)
        p = seg(t, d * .75, d * .95)
        price = "2s 3d" if p < .5 else "4s"
        text(c, price, cx - 260, cy + 140, 190, "disp", GOLD if p < .5 else "#f08a7c", ap(t, d * .2))
        text(c, "per acre", cx - 260, cy + 220, 40, "serif", WHITE, ap(t, d * .25))
        label(c, "AND RISING", cx - 260, cy + 290, 28, p, "#f08a7c", rule=False)
        chip(c, "100 ACRES ≈ £11", cx + 460, cy + 90, a=ap(t, d * .45), size=48)
        settlers(c, cx, H + 60, n=8, s=.7, a=ap(t, d * .6), spread=230)
        c.restore()

# ------------------------------------------------------------------ loan
def sc_loan(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        hotel(ctx, t=t)
        label(c, "OCTOBER 1822 · THE CITY OF LONDON", cx, 110, 30, seg(t, .2, 1.4))
        text(c, "Sir John Perring, Shaw, Barber & Co.", cx, 180, 40, "serif", WHITE, ap(t, d * .2))
        v = int(200000 * eo(seg(t, d * .5, d * .75)))
        if t > d * .45: c.drawRoundRect(skia.Rect.MakeXYWH(cx - 520, cy - 170, 1040, 270), 24, 24, fill("#0b0c10", .82 * ap(t, d * .45)))
        text(c, f"£{v:,}", cx, cy - 20, 150, "disp", GOLD, ap(t, d * .5))
        label(c, "A LOAN TO THE GOVERNMENT OF POYAIS", cx, cy + 60, 28, seg(t, d * .6, d * .6 + 1.4), WHITE, rule=False)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        label(c, "WHAT YOUR MONEY EARNS IN A YEAR", cx, 150, 30, seg(t, .1, 1.3))
        bar_chart(c, cx - 200, cy - 160, [("POYAIS BONDS · 6%", 1.0), ("BRITISH GOV. BONDS", .5)], seg(t, .3, d * .45), w=760, row_h=130, hi=0)
        text(c, "about half", cx + 440, cy + 40, 30, "serif", "#8a93ad", ap(t, d * .3))
        text(c, "London is in a boom: loans to the new nations of Latin America.", cx, cy + 260, 40, "serif", WHITE, ap(t, d * .5))
        text(c, "One more country doesn't look strange.", cx, cy + 340, 46, "serifb", GOLD, ap(t, d * .75))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        p = seg(t, .2, d * .6); pr = 80 + int(6 * eo(seg(t, d * .65, d * .95)))
        bond(c, cx - 260, cy + 20, 1000, rot=-1.2, p=p)
        if t > d * .6: chip(c, f"PRICE {pr}", cx + 620, cy + 200, size=48)
        text(c, "A country on paper,", cx + 620, cy - 60, 50, "serifb", WHITE, ap(t, d * .62))
        text(c, "with a price.", cx + 620, cy + 10, 50, "serifb", GOLD, ap(t, d * .7))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        label(c, "THE CRUELLEST TOUCH", cx, 120, 30, seg(t, .1, 1.2), RED)
        for i in range(6):
            q = seg(t, d * .15 + i * .25, d * .15 + i * .25 + .8)
            if q > 0: poyais_note(c, cx + 380 + (i % 3) * 30, lerp(-200, cy + 60 - i * 14, eo(q)), 460, rot=(i - 3) * 4)
        for i in range(10):
            q = seg(t, d * .45 + i * .08, d * .45 + i * .08 + .7)
            if q > 0: c.drawCircle(lerp(cx - 640, cx + 240, eo(q)), cy + 80 + math.sin(i) * 60, 34, fill(GOLD, 1 - seg(q, .8, 1)));
        text(c, "REAL GOLD", cx - 640, cy + 220, 40, "sansb", GOLD, ap(t, d * .45))
        text(c, "→ POYAIS DOLLARS", cx + 360, cy + 300, 44, "sansb", WHITE, ap(t, d * .6))
        label(c, "PRINTED IN SCOTLAND", cx + 360, cy - 260, 24, seg(t, d * .2, d * .2 + 1.2), WHITE, rule=False)
        c.restore()

# ------------------------------------------------------------------ ships
def sc_ships(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        c.drawCircle(W * .86, H * .48, 50, fill("#f1e6c8", .9)); c.drawCircle(W * .86, H * .48, 170, fill("#f1e6c8", .07, 60))
        sailship(c, lerp(cx - 300, cx + 200, t / d), H * .68, 1.1, t=t)
        sea(ctx, t, H * .68 + 18)
        label(c, "SEPTEMBER 1822 · LONDON", 120, 120, 30, seg(t, .2, 1.4), align="l")
        text(c, "THE HONDURAS PACKET", 120, 200, 56, "disp", WHITE, ap(t, d * .15), align="l")
        text(c, "about 70 settlers", 120, 250, 34, "serif", GOLD, ap(t, d * .25), align="l")
        chip(c, "OFFICER · POYAIS ARMY", W - 380, 170, a=ap(t, d * .6), size=34)
        chip(c, "CLERK · BANK OF POYAIS", W - 380, 270, a=ap(t, d * .72), size=34, color="#9db58a")
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        c.drawRect(skia.Rect.MakeLTRB(0, H * .64, W, H), fill("#141820"))
        sailship(c, cx + 300, H * .66, 1.2, t=t, flag="poyais")
        sea(ctx, t, H * .66 + 18, color="#0b0e17")
        c.drawRect(skia.Rect.MakeLTRB(0, H * .7, cx - 260, H), fill("#1d1814"))     # quay
        for i in range(6):
            q = seg(t, d * .55 + i * .18, d * .55 + i * .18 + 1.4)
            if q > 0:
                c.drawCircle(cx + 40 + i * 70, H * .62 - q * 40, 30 + q * 60, fill("#d9d4c8", .5 * (1 - q), 14)); c.drawCircle(cx + 40 + i * 70, H * .62, 18, fill("#ffcf7a", (1 - seg(q, 0, .2))))
        settlers(c, cx - 620, H + 40, n=5, s=.8, spread=150)
        label(c, "JANUARY 1823 · LEITH, NEAR EDINBURGH", 120, 120, 30, seg(t, .2, 1.4), align="l")
        text(c, "THE KENNERSLEY CASTLE", 120, 200, 56, "disp", WHITE, ap(t, d * .15), align="l")
        text(c, "almost 200 people", 120, 250, 34, "serif", GOLD, ap(t, d * .25), align="l")
        text(c, "A six-gun salute, by one account.", 120, 320, 32, "serif", WHITE, ap(t, d * .62), align="l")
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        k = seg(t, d * .5, d * .58)
        def A():
            w, h = 860, 560; card(c, cx, cy + 10, w, h, rot=-1.5)
            c.drawRect(skia.Rect.MakeXYWH(50, 50, w - 100, h - 150), fill("#d8ccae"))
            st = stroke("#3b3324", 3)
            P = skia.Path(); P.moveTo(50, 300); P.lineTo(300, 200); P.quadTo(380, 120, 450, 200); P.lineTo(810, 290); c.drawPath(P, st)
            for k2 in range(8): c.drawLine(60 + k2 * 100, 360 + (k2 % 2) * 8, 140 + k2 * 100, 360 + (k2 % 2) * 8, stroke("#3b3324", 2))
            for k2 in range(3): palm(c, 120 + k2 * 260, 340, .35, 1, "#3b3324")
            text(c, "BLACK RIVER, AS IMAGINED", w / 2, h - 50, 26, "sansb", "#3b3324", spacing=4)
            text(c, "ILLUSTRATION", 50, h - 18, 13, "sansb", "#8c7d60", align="l", spacing=3)
            c.restore()
            label(c, "THE ONLY PICTURE THEY HAD", cx, 110, 28, seg(t, .2, 1.4), WHITE)
        def B():
            mac(c, cx - 420, H + 40, 2.0)
            text(c, "Not one of them", cx + 320, cy - 120, 62, "serifb", WHITE, ap(t, d * .52))
            text(c, "had seen Poyais.", cx + 320, cy - 30, 62, "serifb", WHITE, ap(t, d * .58))
            text(c, "And the man who sold it", cx + 320, cy + 110, 46, "serif", GOLD, ap(t, d * .78))
            text(c, "was staying behind.", cx + 320, cy + 170, 46, "serifb", GOLD, ap(t, d * .84))
        xfade(c, k, A, B)
        c.restore()

# ------------------------------------------------------------------ arrival
def sc_arrival(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        jungle(ctx, t)
        for i, x in enumerate((cx - 640, cx - 360)):
            figure(c, x, H + 60, .9, hat=i == 0, rim="#4a5a50"); torch(c, x + 110, H * .9, t)
        label(c, "NOVEMBER 1822 · THE BLACK RIVER", 120, 120, 30, seg(t, .2, 1.4), align="l")
        x = cx + 260
        item(c, "STREETS", x, cy - 140, 56, t, d * .45, ok=False)
        item(c, "BANK", x, cy - 50, 56, t, d * .58, ok=False)
        item(c, "OPERA HOUSE", x, cy + 40, 56, t, d * .7, ok=False)
        text(c, "only old foundations and rubble", cx + 260, cy + 140, 36, "serif", GOLD, ap(t, d * .3), align="l")
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        jungle(ctx, t, shore=.66)
        sea(ctx, t, H * .82, color="#0a0f14", n=3)
        for k in range(4):
            x = cx - 680 + k * 230; y = H * .76
            P = skia.Path(); P.moveTo(x - 90, y); P.lineTo(x, y - 110); P.lineTo(x + 90, y); P.close(); c.drawPath(P, fill("#2a2219")); c.drawPath(P, stroke("#5a4a30", 3))
        sailship(c, lerp(cx + 400, W + 400, eo(seg(t, d * .35, d))), H * .84, .55, t=t)
        text(c, "Rough shelters. Then the ship sails away.", cx, 120, 50, "serifb", WHITE, ap(t, .3))
        q = seg(t, d * .65, d)
        if q > 0:
            P = skia.Path(); x = lerp(cx - 200, cx + 300, q); y = H * .9
            P.moveTo(x - 60, y); P.quadTo(x, y + 20, x + 60, y); P.close(); c.drawPath(P, fill("#3a2a1a"))
            label(c, "A CANOE FOR HELP · IT FOUNDERS", cx, 200, 26, seg(t, d * .7, d * .7 + 1.2), "#f08a7c", rule=False)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        jungle(ctx, t, rain=eo(seg(t, d * .3, d * .5)), dusk=False)
        label(c, "MARCH 1823 · NEARLY 200 MORE ARRIVE", cx, 120, 30, seg(t, .1, 1.3), WHITE)
        stamp(c, "MALARIA", cx - 360, cy - 40, 110, seg(t, d * .55, d * .55 + .35), rot=-8)
        stamp(c, "YELLOW FEVER", cx + 360, cy + 80, 96, seg(t, d * .75, d * .75 + .35), rot=6)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        k = seg(t, d * .6, d * .68)
        def A():
            w, h = 1200, 520; card(c, cx, cy, w, h, rot=-.8)
            text(c, "SETTLER JAMES HASTIE, LATER:", w / 2, 80, 28, "sansb", "#5a4d38", spacing=5)
            for i, s in enumerate(("“Sickness and despondency was so general,", "that few were able or willing", "to make any exertion.”")):
                typed(c, s, w / 2, 210 + i * 80, 50, seg(t, .3 + i * d * .15, .3 + (i + 1) * d * .15), "serifb", "#1d1a14", align="c")
            c.restore()
        def B():
            poyais_note(c, cx, cy - 20, 900, rot=-4, stamp_p=seg(t, d * .72, d * .72 + .35))
            text(c, "Nothing to buy. No one to sell it.", cx, H - 110, 52, "serifb", GOLD, ap(t, d * .8))
        xfade(c, k, A, B)
        c.restore()

# ------------------------------------------------------------------ rescue
def sc_rescue(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        c.drawCircle(W * .7, H * .3, 300, fill("#ffd28a", .08, 90))
        sailship(c, lerp(W + 300, cx + 280, eo(seg(t, .1, d * .5))), H * .68, 1.0, t=t)
        sea(ctx, t, H * .68 + 18)
        label(c, "SPRING 1823 · DATES DIFFER", 120, 120, 30, seg(t, .2, 1.4), align="l")
        text(c, "THE MEXICAN EAGLE", 120, 200, 56, "disp", WHITE, ap(t, d * .2), align="l")
        text(c, "from Belize · Marshal Bennett, chief magistrate", 120, 250, 32, "serif", GOLD, ap(t, d * .3), align="l")
        chip(c, "INQUIRY · SUPT. EDWARD CODD", cx - 380, H * .55, a=ap(t, d * .75), size=34)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        label(c, "ROUGHLY 250 ON THE FIRST TWO SHIPS", cx, 110, 30, seg(t, .1, 1.3))
        dots(c, cx - 24 * 44 / 2, 220, 250, 25, seg(t, d * .35, d * .8), 180, r=15, gap=44)
        text(c, "at least 180 died", cx - 380, H - 90, 50, "sansb", "#f08a7c", ap(t, d * .6))
        text(c, "fewer than 50 came home", cx + 380, H - 90, 50, "sansb", WHITE, ap(t, d * .82))
        label(c, "BY MOST ESTIMATES", cx, H - 40, 20, seg(t, d * .6, d * .6 + 1), "#8a93ad", rule=False)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        sea(ctx, t, H * .7 + 18)
        for i in range(5): sailship(c, cx - 760 + i * 300, H * .7, .42, t=t + i, a=.9)
        q = eo(seg(t, .3, d * .6))
        sailship(c, lerp(W + 300, cx + 600, q), H * .72, .75, t=t, color="#1a1e2a", sail="#b9c2d6")
        label(c, "ROYAL NAVY", lerp(W + 300, cx + 600, q), H * .72 + 70, 22, q, WHITE, rule=False)
        stamp(c, "STOPPED", cx - 160, cy - 180, 110, seg(t, d * .7, d * .7 + .35), rot=-6)
        label(c, "FIVE MORE SHIPS OF SETTLERS", cx, 110, 30, seg(t, .1, 1.3))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        newspaper(ctx, cx - 340, cy + 20, 900, 760, -1.5, ["KING CANCELS", "THE GRANT"], "A notice from the Miskito king", "THE TIMES · SEPT 1823", hp=seg(t, .2, d * .4))
        x0, y0 = cx + 260, cy - 150; w = 520; h = 330
        c.drawLine(x0, y0 + h, x0 + w, y0 + h, stroke("#8a93ad", 3)); c.drawLine(x0, y0, x0, y0 + h, stroke("#8a93ad", 3))
        pts = [(x0, y0 + 60), (x0 + w * .3, y0 + 40), (x0 + w * .55, y0 + 70)]
        q = seg(t, d * .5, d * .85)
        pts += [(x0 + w * .55 + w * .45 * eo(q), y0 + 70 + (h - 90) * eo(q))]
        P = skia.Path(); P.moveTo(*pts[0]); [P.lineTo(*p_) for p_ in pts[1:]]; c.drawPath(P, stroke("#f08a7c" if q > 0 else GOLD, 8))
        label(c, "POYAIS BONDS", x0 + w / 2, y0 - 30, 26, seg(t, d * .45, d * .45 + 1), WHITE, rule=False)
        stamp(c, "CRASH", x0 + w * .65, y0 + h * .55, 80, seg(t, d * .85, d * .85 + .3), rot=-8)
        c.restore()

# ------------------------------------------------------------------ unravel
def sc_unravel(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        w, h = 1100, 640; card(c, cx - 160, cy + 20, w, h, rot=-1)
        text(c, "STATEMENT OF SIX SURVIVORS", w / 2, 90, 44, "serifb", INK, spacing=3); c.drawLine(80, 120, w - 80, 120, stroke(INK, 2, cap=False))
        text(c, "LONDON · 22 OCTOBER 1823", w / 2, 165, 22, "serif", "#5a4d38", spacing=4)
        item(c, "TO BLAME: THE EXPEDITION'S LEADERS", 120, 280, 40, t, d * .45, ok=True, color="#1d1a14")
        item(c, "TO BLAME: THE AGENTS", 120, 360, 40, t, d * .55, ok=True, color="#1d1a14")
        item(c, "TO BLAME: MACGREGOR", 120, 440, 40, t, d * .72, ok=False, color="#1d1a14")
        text(c, "RECONSTRUCTION · SUMMARY", 60, h - 30, 14, "sansb", "#8c7d60", align="l", spacing=3)
        c.restore()
        mac(c, W - 230, H + 40, 1.4, rim=GOLD)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        route(ctx, seg(t, .2, d * .6), "LONDON", "FRANCE", sp=500)
        text(c, "“Taking his wife south, for her health.”", cx, H - 110, 50, "serifb", GOLD, ap(t, d * .45))
        label(c, "SHORTLY BEFORE THE SURVIVORS LANDED", cx, 120, 28, seg(t, .1, 1.3), WHITE)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        for i, s in enumerate(("NEW COMPANY", "NEW CONSTITUTION", "NEW POYAIS")):
            chip(c, s, cx - 560 + i * 560, 250, a=ap(t, .2 + i * .5), size=40)
        mac(c, cx, H + 60, 1.2, rim=GOLD)
        stamp(c, "ARRESTED · DEC 1825", cx - 380, cy + 80, 70, seg(t, d * .4, d * .4 + .35), rot=-6)
        text(c, "Associate: 13 months", cx + 400, cy + 40, 46, "sansb", WHITE, ap(t, d * .62))
        solid_stamp(c, "ACQUITTED", cx + 400, cy + 220, 90, rot=5, color="#c79a2e", ink="#1d1a14") if t > d * .82 else None
        label(c, "PARIS · 1825", cx, 120, 30, seg(t, .1, 1), GOLD)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        bond(c, cx - 420, cy - 40, 720, rot=-5, p=1)
        card(c, cx + 300, cy + 60, 640, 420, rot=4, color="#efe3c4")
        text(c, "LAND IN POYAIS", 320, 110, 50, "serifb", "#2a2216", spacing=2); text(c, "CERTIFICATE · 1830s", 320, 170, 26, "serif", "#5a4d38", spacing=4)
        text(c, "ILLUSTRATION", 40, 400, 13, "sansb", "#8c7d60", align="l", spacing=3)
        c.restore()
        chip(c, "1827 LOAN · MOSTLY UNSOLD", cx - 420, 120, a=ap(t, d * .15), size=36)
        text(c, "The country that never was", cx, H - 140, 54, "serifb", WHITE, ap(t, d * .6))
        text(c, "refuses to die.", cx, H - 70, 54, "serifb", GOLD, ap(t, d * .72))
        c.restore()

# ------------------------------------------------------------------ end
def sc_end(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        route(ctx, seg(t, .2, d * .5), "EDINBURGH", "CARACAS", sp=520)
        label(c, "1838 · VENEZUELA TAKES HIM BACK", cx, 110, 30, seg(t, .1, 1.3))
        chip(c, "CITIZENSHIP", cx - 260, H - 140, a=ap(t, d * .55), size=40)
        chip(c, "A GENERAL'S PENSION", cx + 260, H - 140, a=ap(t, d * .7), size=40, color="#9db58a")
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        c.drawCircle(cx, cy - 100, 420, fill("#ffcf7a", .07, 120))
        P = skia.Path(); P.moveTo(cx - 330, cy + 120); P.lineTo(cx - 250, cy + 60); P.lineTo(cx + 330, cy + 70); P.lineTo(cx + 360, cy + 120); P.lineTo(cx + 330, cy + 170); P.lineTo(cx - 250, cy + 180); P.close()
        c.drawPath(P, fill("#2a1b14")); c.drawPath(P, stroke(GOLD, 4))
        c.drawLine(cx - 120, cy + 120, cx + 200, cy + 120, stroke(GOLD, 6)); c.drawLine(cx - 40, cy + 85, cx - 40, cy + 155, stroke(GOLD, 6))
        for x in (cx - 470, cx + 500):
            c.drawRect(skia.Rect.MakeXYWH(x - 12, cy + 20, 24, 160), fill("#e9dcc0")); c.drawCircle(x, cy + 6, 40 * (1 + .1 * math.sin(t * 9 + x)), fill("#ffb45e", .3, 16)); c.drawCircle(x, cy + 6, 9, fill("#ffd28a"))
        for i in range(8): figure(c, cx - 860 + i * 245, H + 120, .9, hat=False, rim="#2b3044", bow=.8)
        text(c, "CARACAS · DECEMBER 1845", cx, 140, 56, "disp", WHITE, ap(t, .2))
        label(c, "FULL MILITARY HONOURS", cx, 220, 28, seg(t, d * .2, d * .2 + 1.3), GOLD)
        solid_stamp(c, "NEVER CONVICTED", cx, cy - 120, 80, rot=-5) if t > d * .78 else None
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        for i, (who, l1, l2, colr) in enumerate((("THE ECONOMIST", "“perhaps the greatest", "con of all time”", RED), ("A RECENT STUDY", "a real, reckless scheme;", "the broker took about a third", "#5a7fb0"))):
            x = cx - 430 + i * 860; q = ap(t, .3 + i * d * .3)
            c.drawRoundRect(skia.Rect.MakeXYWH(x - 380, cy - 240, 760, 420), 20, 20, fill("#ffffff", .05 * q)); c.drawRoundRect(skia.Rect.MakeXYWH(x - 380, cy - 240, 760, 420), 20, 20, stroke(colr, 4, q))
            label(c, who, x, cy - 160, 28, seg(t, .3 + i * d * .3, 1.5 + i * d * .3), colr, rule=False)
            text(c, l1, x, cy - 30, 44, "serifb", WHITE, q); text(c, l2, x, cy + 40, 44, "serifb", WHITE, q)
        label(c, "HISTORIANS STILL ARGUE", cx, 140, 30, seg(t, .1, 1.3))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        k = seg(t, d * .5, d * .58)
        def A():
            jungle(ctx, t, shore=.6, dusk=True)
            c.drawRect(skia.Rect.MakeLTRB(0, H * .78, W, H), fill("#2a2318"))
            poyais_note(c, cx + 200, H * .86, 360, rot=-14, a=.85)
            text(c, "They paid for a country.", cx, 140, 60, "serifb", WHITE, ap(t, .2))
            text(c, "They got a beach, a fever, and a banknote.", cx, 220, 48, "serif", GOLD, ap(t, d * .25))
        def B():
            c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill("#2a2733", .7))
            c.drawCircle(cx, cy - 40, 460, fill("#ffcf7a", .1, 120))
            poyais_note(c, cx, cy - 40, 820, rot=0)
            c.drawRect(skia.Rect.MakeXYWH(cx - 460, cy - 280, 920, 480), stroke("#c9d6e8", 3, .4))
            label(c, "AT AUCTION · TODAY", cx, 110, 28, seg(t, d * .55, d * .55 + 1.2), WHITE)
            text(c, "Finally worth something.", cx, H - 100, 62, "serifb", GOLD, ap(t, d * .78))
        xfade(c, k, A, B)
        c.restore()

def sc_outro(ctx):
    c, cx, cy, t = ctx.c, ctx.cx, ctx.cy, ctx.t
    stamp(c, "CASE CLOSED", cx, cy - 110, 150, seg(t, .15, .45), rot=-5)
    label(c, "CASE CLOSED FILES", cx, cy + 110, 30, seg(t, .6, 1.4), GOLD)
    text(c, "New case every week. Subscribe so you don't miss it.", cx, cy + 210, 40, "serif", WHITE, ap(t, 1.1))

SCENES = {k[3:]: v for k, v in list(globals().items()) if k.startswith("sc_") and callable(v)}
HITS = [("who", 2, 0, .8), ("who", 4, 0, .6), ("grant", 1, 0, .72), ("sell", 2, 0, .9), ("arrival", 0, 0, .45), ("arrival", 2, 0, .55),
        ("arrival", 2, 0, .75), ("arrival", 3, 0, .72), ("rescue", 2, 0, .7), ("rescue", 3, 0, .85), ("unravel", 2, 0, .4), ("unravel", 2, 0, .82),
        ("end", 1, 0, .78), ("outro", -1, .15, 0)]
SHORT_HITS = []
WARM = {}

THUMB_WORDS = [(["NO SUCH", "PLACE."], 128), (["IT WASN'T", "THERE."], 112), (["250", "SAILED."], 150)]
def thumbnail(c, W, H, word):
    word, size = word
    sh = skia.GradientShader.MakeRadial(center=(W * .36, H * .5), radius=900, colors=[col("#2c4a3e"), col("#12201c"), col("#07080b")], positions=[0, .5, 1])
    c.drawPaint(skia.Paint(Shader=sh))
    c.drawCircle(W * .3, H * .5, 380, fill("#ffcf7a", .12, 90))
    poyais_note(c, W * .3, H * .5, 620, rot=-8)
    solid_stamp(c, "FAKE", W * .33, H * .7, 96, rot=-12)
    figure(c, W * .82, H + 30, 1.5, hat=False, rim=GOLD)
    for i, ln in enumerate(word): big_word(c, ln, W * .72, H * .2 + i * size * 1.02, size, "#ffd36b")


# ---------------- shorts (60-100 s, 9:16) ----------------
from shorts import hook_card, cta_card
def _note(c, cx, cy, t, d): poyais_note(c, cx, cy + 140, 560, rot=-6, a=.9 * eo(seg(t, 0, .8)))
def _book(c, cx, cy, t, d): guidebook(c, cx, cy + 130, 230, rot=-5, a=.9 * eo(seg(t, 0, .8)))
def _flag(c, cx, cy, t, d): poyais_flag(c, cx - 200, cy - 10, 400, a=.85 * eo(seg(t, 0, .8)), t=t)
SCENES["hook_a"] = hook_card(["A FAKE COUNTRY.", "REAL SETTLERS."], stamp_text="1822", prop=_flag)
SCENES["hook_b"] = hook_card(["HOW TO SELL", "A FAKE COUNTRY"], stamp_text="STEP BY STEP", prop=_note, rim=GOLD)
SCENES["hook_c"] = hook_card(["THEY WENT", "LOOKING FOR IT."], stamp_text="250 SAILED", prop=_book)
SCENES["cta_a"] = cta_card("CASE 003 · POYAIS", "PART 2 NEXT")
SCENES["cta_b"] = cta_card("CASE 003 · POYAIS", "PART 3 NEXT")
SCENES["cta_c"] = cta_card("CASE 003 · POYAIS", "FULL CASE")
SHORT_HITS += [("hook_a", -1, .15, .62), ("hook_b", -1, .15, .62), ("hook_c", -1, .15, .62)]
SHORT_VIEW = {}
