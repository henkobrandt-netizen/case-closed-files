from lib import *

NOT = GOLD          # Notarbartolo's rim colour
COP = "#8fa0c8"     # detectives
def beat(ctx, i):
    t, a, d = ctx.ph(i)
    if a > 0: ctx.layer(a)
    return t, a, d
def xfade(c, k, draw_a, draw_b):
    if k < 1:
        c.saveLayerAlpha(None, int(255 * (1 - k))); draw_a(); c.restore()
    if k > 0:
        c.saveLayerAlpha(None, int(255 * k)); draw_b(); c.restore()
def floor_mess(c, cx, y, w, t, a=1.0, seed=4):
    """Vault floor: scattered papers, open boxes, stones."""
    rnd = random.Random(seed)
    c.drawRect(skia.Rect.MakeLTRB(cx - w / 2, y, cx + w / 2, y + 400), fill("#1a1712", a))
    for i in range(14):
        x = cx + rnd.uniform(-w / 2, w / 2); yy = y + rnd.uniform(30, 260); r = rnd.uniform(-30, 30)
        c.save(); c.translate(x, yy); c.rotate(r); c.drawRect(skia.Rect.MakeXYWH(-60, -40, 120, 80), fill(PAPER, a * .75)); c.restore()
    for i in range(6):
        x = cx + rnd.uniform(-w / 2.4, w / 2.4); yy = y + rnd.uniform(60, 240)
        c.drawRect(skia.Rect.MakeXYWH(x - 70, yy - 30, 140, 60), fill("#4a505e", a)); c.drawRect(skia.Rect.MakeXYWH(x - 60, yy - 22, 120, 30), fill("#0a0b0e", a))
    scatter_gems(c, cx - w / 2, y + 40, w, 230, 26, a, seed=seed, t=t)

def boxes_inside(cx, cy, r, opened=40, t=0.0):
    def f(c):
        deposit_wall(c, cx - r * 1.2, cy - r * 1.05, 10, 8, r * .24, r * .27, opened=opened, t=t)
    return f

# ------------------------------------------------------------------ cold open
def sc_cold(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        label(c, "MONDAY 17 FEBRUARY 2003 · ANTWERP", 110, 120, 30, seg(t, .2, 1.6), align="l")
        text(c, "Two floors", 110, 260, 70, "serifb", WHITE, ap(t, d * .25), align="l")
        text(c, "under the street.", 110, 340, 70, "serifb", WHITE, ap(t, d * .35), align="l")
        text(c, "The door is open.", 110, 470, 62, "serifb", GOLD, ap(t, d * .7), align="l")
        vault_door(c, cx + 430, cy + 40, 360, open=seg(t, d * .55, d * .95), rot=t * 8, inside=boxes_inside(cx + 430, cy + 40, 360, 46, t))
        person(c, cx - 120, H - 40, 330, rim=COP, a=ap(t, d * .6))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        deposit_wall(c, cx - 760, 120, 16, 4, 95, 90, opened=40, t=t)
        floor_mess(c, cx, H * .57, 1700, t)
        label(c, "THREE TONS OF STEEL · WIDE OPEN", cx, 80, 28, seg(t, .1, 1.3))
        text(c, "papers · empty boxes · jewellery · loose stones", cx, H - 70, 40, "serif", WHITE, ap(t, d * .45))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        c.drawRoundRect(skia.Rect.MakeXYWH(cx - 820, cy - 330, 640, 520), 20, 20, fill("#0d1016"))
        c.drawRoundRect(skia.Rect.MakeXYWH(cx - 820, cy - 330, 640, 520), 20, 20, stroke("#2e3446", 4))
        label(c, "ALARM LOG · WEEKEND", cx - 500, cy - 260, 26, seg(t, .1, 1.2), GOLD)
        for i, s in enumerate(("SAT 15 FEB", "SUN 16 FEB", "MON 17 FEB")):
            q = ap(t, .4 + i * .5)
            text(c, s, cx - 760, cy - 160 + i * 100, 36, "type", WHITE, q, align="l")
            text(c, "NO EVENTS", cx - 240, cy - 160 + i * 100, 36, "typeb", GREEN, q, align="r")
        text(c, "“Then how is it that the door", cx + 400, cy - 120, 50, "serifb", WHITE, ap(t, d * .55))
        text(c, "is wide open, and I'm standing", cx + 400, cy - 50, 50, "serifb", WHITE, ap(t, d * .62))
        text(c, "inside the vault?”", cx + 400, cy + 20, 50, "serifb", GOLD, ap(t, d * .69))
        text(c, "— Det. Agim De Bruycker, as told to Wired", cx + 400, cy + 100, 30, "serif", WHITE, ap(t, d * .75) * .8)
        person(c, cx + 400, H + 60, 300, rim=COP, a=ap(t, d * .4) * .9)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        kinds = ("dial", "key", "seismic", "magnet", "grate", "camera", "keypad", "light", "heat", "radar")
        for i, k in enumerate(kinds):
            x = cx - 810 + i * 180
            layer_tile(c, x, 300, 150, k, "", a=ap(t, .1 + i * .08), beaten=seg(t, 1.2 + i * .1, 1.6 + i * .1))
        text(c, "10 LAYERS · 0 ALARMS", cx, 520, 64, "disp", WHITE, ap(t, d * .2))
        q = ap(t, d * .45)
        sandwich(c, cx, 760, 520 * (0.85 + .15 * q), rot=-4, a=q)
        text(c, "WHO? HOW?", cx, H - 70, 70, "disp", GOLD, ap(t, d * .8))
        c.restore()

def sc_title(ctx):
    c, cx, cy, t = ctx.c, ctx.cx, ctx.cy, ctx.t
    c.drawCircle(cx, cy - 20, 420, fill(ICE, .05, 120))
    gem(c, cx, cy - 300, 120, a=ap(t, .1, .6), shine=.5 + .5 * math.sin(t * 3))
    label(c, "CASE CLOSED FILES  ·  NO. 004", cx, cy - 170, 26, seg(t, .1, .7))
    text(c, "THE HEIST OF", cx, cy - 20 + (1 - ap(t, .2, .6)) * 30, 128, "disp", WHITE, ap(t, .2, .6), spacing=4)
    text(c, "THE CENTURY", cx, cy + 130 + (1 - ap(t, .5, .6)) * 30, 140, "disp", GOLD, ap(t, .5, .6), spacing=4)
    text(c, "A true story · Antwerp, Belgium, 2000–2003", cx, cy + 240, 34, "serif", WHITE, ap(t, 1.0) * .8)

# ------------------------------------------------------------------ the district
def sc_district(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        skyline(c, W, H * .78, 31, "#171b27", 1, 80, 260, 0, lit=.18)
        label(c, "ANTWERP · THE DIAMOND DISTRICT", cx, 110, 30, seg(t, .1, 1.4))
        text(c, "$23 BILLION", cx, 300, 130, "disp", GOLD, ap(t, d * .5))
        text(c, "in trade, every year", cx, 380, 40, "serif", WHITE, ap(t, d * .6) * .85)
        for i in range(9): gem(c, 260 + i * 175, 520 + (i % 2) * 40, 46, a=ap(t, d * .5 + i * .1) * .8, shine=.6 * (i % 3 == 0))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        c.drawRect(skia.Rect.MakeLTRB(0, H * .72, W, H), fill("#14161c"))
        skyline(c, W, H * .72, 5, "#1b1f2d", 1, 200, 380, 0, lit=.12)
        for i in range(7):
            x = 260 + i * 70; q = ap(t, .2 + i * .1)
            c.drawRoundRect(skia.Rect.MakeXYWH(x, H * .72 - 120 * q, 34, 120 * q + 30), 10, 10, fill("#8a909c")); c.drawRect(skia.Rect.MakeXYWH(x, H * .72 - 100 * q, 34, 14), fill(RED, q))
        label(c, "STEEL PILLARS", 470, H * .72 + 80, 24, seg(t, .5, 1.5), WHITE, rule=False)
        for i, (x, y) in enumerate(((1100, 300), (1450, 380), (1750, 260))):
            q = ap(t, d * .3 + i * .2); sensor_icon(c, "camera", x, y, 90, GOLD, q)
            P = skia.Path(); P.moveTo(x + 40, y); P.lineTo(x + 260, y + 300); P.lineTo(x - 60, y + 330); P.close(); c.drawPath(P, fill(GOLD, .07 * q))
        chip(c, "A POLICE STATION JUST FOR THESE STREETS", cx, H - 70, a=ap(t, d * .7), size=36, color=COP)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        building(c, cx, H * .62, floors=6, under=2, w=820, cut=seg(t, d * .45, d * .8), vault_glow=seg(t, d * .7, d * .95))
        label(c, "SCHUPSTRAAT · ANTWERP DIAMOND CENTRE", cx, 90, 28, seg(t, .1, 1.4))
        text(c, "OFFICES", cx + 560, H * .3, 40, "sansb", WHITE, ap(t, d * .3), align="l")
        text(c, "2 FLOORS DOWN", cx + 560, H * .62 + 150, 40, "sansb", GOLD, ap(t, d * .75), align="l")
        c.restore()
    for li in (3, 4):
        t, a, d = beat(ctx, li)
        if a > 0:
            rows = [("dial", "COMBINATION DIAL"), ("key", "FOOT-LONG KEY"), ("seismic", "SEISMIC SENSOR"), ("magnet", "MAGNETIC PLATES"), ("heat", "HEAT + MOTION"),
                    ("light", "LIGHT SENSOR"), ("radar", "DOPPLER RADAR"), ("camera", "CAMERAS")]
            for i, (k, n) in enumerate(rows):
                x = cx - 720 + (i % 4) * 480; y = 330 + (i // 4) * 380
                if li == 3 and i >= 4: continue
                t0 = (i * d * .22) if li == 3 else (0 if i < 4 else (i - 4) * d * .2)
                layer_tile(c, x, y, 300, k, n, a=ap(t, t0) * (.55 if (li == 4 and i < 4) else 1))
            if li == 3:
                text(c, "0–99 · 100,000,000 combinations", cx, H - 60, 44, "sansb", GOLD, ap(t, d * .2))
            else:
                text(c, "TEN LAYERS. NOBODY HAD EVER BROKEN IN.", cx, H - 50, 46, "sansb", GOLD, ap(t, d * .7))
            c.restore()
    t, a, d = beat(ctx, 5)
    if a > 0:
        deposit_wall(c, cx - 820, 140, 12, 6, 95, 100, opened=0)
        c.drawRoundRect(skia.Rect.MakeXYWH(cx + 380, 170, 470, 560), 20, 20, fill("#0d1016", .95))
        text(c, "¾", cx + 615, 420, 220, "disp", GOLD, ap(t, d * .4))
        text(c, "of the business,", cx + 615, 520, 40, "serif", WHITE, ap(t, d * .5))
        text(c, "no paperwork", cx + 615, 580, 46, "serifb", WHITE, ap(t, d * .55))
        text(c, "(one detective's estimate)", cx + 615, 650, 28, "serif", WHITE, ap(t, d * .6) * .7)
        stamp(c, "REMEMBER THIS", cx - 250, H - 150, 66, seg(t, d * .82, d * .82 + .35), rot=-5, color="#e8b23a")
        c.restore()

# ------------------------------------------------------------------ the tenant
def sc_tenant(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        w, h = 1300, 620; card(c, cx, cy + (1 - ap(t, 0, .7)) * 80, w, h, rot=-1.0)
        text(c, "DOSSIER", 60, 80, 40, "sansb", INK, align="l", spacing=10); text(c, "FILE 004", w - 60, 80, 22, "type", "#5a4d38", align="r")
        c.drawLine(60, 104, w - 60, 104, stroke(INK, 2, cap=False))
        c.drawRect(skia.Rect.MakeXYWH(60, 140, 340, 420), fill("#1b1e29"))
        c.save(); c.clipRect(skia.Rect.MakeXYWH(60, 140, 340, 420)); figure(c, 230, 590, 1.25, hat=False, rim=NOT); c.restore()
        rows = [("TENANT SINCE", "November 2000", .6), ("FROM", "Turin, Italy", d * .25), ("TRADE", "Gem importer", d * .45), ("NAME", "Leonardo Notarbartolo", d * .7)]
        for i, (k, v, ts) in enumerate(rows):
            y = 190 + i * 100
            text(c, k, 460, y, 18, "sansb", "#7a6a4c", ap(t, ts - .3), align="l", spacing=4)
            typed(c, v, 460, y + 44, 38, seg(t, ts, ts + .9), color="#1d1a14", cursor=True)
        c.restore(); c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        for i, s in enumerate(("BUYS SMALL STONES", "PAYS HIS BILLS", "MAKES FRIENDS")):
            item(c, s, 140, 260 + i * 100, 44, t, .2 + i * d * .12, ok=True)
        id_card(c, cx + 420, cy - 40, 620, rot=4, a=ap(t, d * .55), title="ANTWERP DIAMOND CENTRE", name="TENANT", sub="VAULT ACCESS · DAYTIME")
        q = ap(t, d * .75)
        deposit_wall(c, 140, 640, 6, 2, 90, 80, a=q)
        c.drawRect(skia.Rect.MakeXYWH(140 + 2 * 90, 640, 90, 80), stroke(GOLD, 6, q))
        text(c, "HIS OWN BOX", 140 + 2.5 * 90, 840, 30, "sansb", GOLD, q)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        vault_door(c, cx + 80, cy + 30, 300, rot=t * 5)
        for i, (k, x, y, n) in enumerate((("camera", cx - 560, 220, "CAMERA"), ("heat", cx + 600, 230, "HEAT SENSOR"), ("light", cx + 640, cy + 200, "LIGHT SENSOR"), ("magnet", cx - 600, cy + 150, "MAGNETIC PLATES"))):
            q = ap(t, .3 + i * d * .15)
            sensor_icon(c, k, x, y, 90, GOLD, q); label(c, n, x, y + 80, 22, seg(t, .3 + i * d * .15, 1.3 + i * d * .15), WHITE, a=q, rule=False)
            dashed(c, [(x, y), (cx + 80, cy + 30)], seg(t, .3 + i * d * .15, .9 + i * d * .15), GOLD, 3, a=.6 * q)
        q = ap(t, d * .7)
        c.save(); c.translate(cx + 260, H - 110); c.rotate(-8)
        c.drawRoundRect(skia.Rect.MakeXYWH(0, -14, 360, 28), 14, 14, fill("#1d2333", q)); c.drawRect(skia.Rect.MakeXYWH(330, -10, 50, 20), fill(GOLD, q)); c.drawCircle(60, 0, 7, fill("#6fb8ff", q))
        c.restore()
        text(c, "a pen with a camera", cx + 450, H - 30, 32, "serif", WHITE, q * .85)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill("#1a1d26", .6))
        vault_door(c, cx - 360, cy + 140, 300, rot=0)
        c.drawCircle(cx - 360, cy - 250, 26, fill("#ffe2a0", .9)); c.drawCircle(cx - 360, cy - 250, 90, fill("#ffe2a0", .15, 30))
        q = seg(t, d * .15, d * .35); c.drawCircle(cx - 312, cy - 250, 9, fill("#ff3b30", q)); c.drawCircle(cx - 312, cy - 250, 26, stroke(RED, 3, q))
        dashed(c, [(cx - 312, cy - 250), (cx + 200, cy - 250), (cx + 360, cy + 100)], seg(t, d * .3, d * .55), RED, 3, a=.8)
        extinguisher(c, cx + 420, H - 100, 1.5, cam=seg(t, d * .55, d * .65), t=t)
        text(c, "THE RECORDER", cx + 720, cy - 120, 36, "sansb", GOLD, ap(t, d * .6), align="r")
        text(c, "Nobody looks twice at a fire extinguisher.", cx, H - 30, 44, "serifb", WHITE, ap(t, d * .75))
        label(c, "HIS OWN ACCOUNT · ILLUSTRATION", cx, 90, 24, seg(t, .1, 1.3), WHITE)
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        figure(c, cx - 420, H + 40, 2.0, hat=False, rim=NOT)
        text(c, "Seeing the vault was easy.", cx + 320, cy - 80, 60, "serifb", WHITE, ap(t, .2))
        text(c, "Beating it was something else.", cx + 320, cy + 10, 60, "serifb", GOLD, ap(t, d * .3))
        stamp(c, "NEEDED: A TEAM", cx + 320, cy + 190, 74, seg(t, d * .65, d * .65 + .35), rot=-5)
        c.restore()

# ------------------------------------------------------------------ the crew
CREW = [("THE GENIUS", "alarms + electronics", "police: Elio D'Onorio", "#6fb8ff"), ("THE MONSTER", "locks · driver · strength", "police: Ferdinando Finotto", RED),
        ("THE KING OF KEYS", "a master key forger", "never identified", GOLD), ("SPEEDY", "a nervous old friend", "police: Pietro Tavano", "#9db58a")]
def crew_row(c, cx, cy, t, reveal, a=1.0, dim_all=0.0, hi=-1):
    for i, (n, role, who, colr) in enumerate(CREW):
        x = cx - 690 + i * 460; q = seg(reveal, i, i + .6) if reveal < 4 else 1
        if q <= 0: continue
        al = a * eo(q) * (1 - dim_all * (0 if i == hi else .6))
        c.drawRoundRect(skia.Rect.MakeXYWH(x - 200, cy - 330, 400, 600), 18, 18, fill("#0d1016", al * .95))
        c.drawRoundRect(skia.Rect.MakeXYWH(x - 200, cy - 330, 400, 600), 18, 18, stroke(colr, 4, al))
        c.save(); c.clipRect(skia.Rect.MakeXYWH(x - 200, cy - 330, 400, 380)); figure(c, x, cy + 50, 1.05, hat=i == 2, rim=colr, a=al); c.restore()
        if i == 2: text(c, "?", x, cy - 120, 120, "disp", GOLD, al)
        text(c, n, x, cy + 110, 36 if len(n) < 12 else 30, "sansb", colr, al, spacing=2)
        text(c, role, x, cy + 165, 28, "serif", WHITE, al * .9)
        text(c, who, x, cy + 225, 22, "type", WHITE, al * .7)
def sc_crew(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    for li in range(4):
        t, a, d = beat(ctx, li)
        if a > 0:
            crew_row(c, cx, cy + 40, t, li + seg(t, .2, 1.0) if li < 3 else 4, dim_all=seg(t, d * .5, d * .7) if li == 3 else 0, hi=3)
            label(c, "THE CREW · NICKNAMES FROM NOTARBARTOLO", cx, 90, 26, 1)
            if li == 3: stamp(c, "REMEMBER SPEEDY", cx + 690, cy - 280, 46, seg(t, d * .78, d * .78 + .35), rot=-6, color="#e8b23a")
            c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        k = seg(t, d * .6, d * .68)
        def A():
            c.drawRect(skia.Rect.MakeXYWH(cx - 760, cy - 300, 1520, 640), stroke("#4a505e", 4))
            for i in range(6): c.drawLine(cx - 760, cy - 300 + i * 128, cx + 760, cy - 300 + i * 128, stroke("#ffffff", 1, .05))
            label(c, "A WAREHOUSE · A COPY OF THE VAULT?", cx, 140, 28, seg(t, .1, 1.3))
            vault_door(c, cx - 300, cy + 40, 220, rot=t * 10)
            for i, ph in enumerate((0, .3, .6)): person(c, cx + 160 + i * 170, cy + 330, 260, rim=GOLD, step=(t * .8 + ph) % 1)
            for i, kind in enumerate(("magnet", "heat", "light")): sensor_icon(c, kind, cx - 300 + (i - 1) * 180, cy - 280, 70, "#d8cdb4", .9)
            stamp(c, "UNCONFIRMED", cx + 360, cy - 140, 66, seg(t, d * .35, d * .35 + .35), rot=-7)
        def B():
            crew_row(c, cx, cy + 60, t, 4, a=.5)
            c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill("#07080b", .55))
            text(c, "THE SCHOOL", cx, cy - 40, 140, "disp", WHITE, 1, spacing=4)
            text(c, "OF TURIN", cx, cy + 110, 140, "disp", GOLD, 1, spacing=4)
        xfade(c, k, A, B)
        c.restore()

# ------------------------------------------------------------------ the night
def facade(ctx, t, a=1.0, shield=0.0, climb=0.0):
    c, W, H = ctx.c, ctx.W, ctx.H; base = H * .9
    c.drawCircle(W * .86, H * .16, 54, fill("#f1e6c8", .9 * a)); c.drawCircle(W * .86, H * .16, 180, fill("#f1e6c8", .08 * a, 60))
    c.drawRect(skia.Rect.MakeXYWH(820, 120, 900, base - 120), fill("#171b26", a))
    for f_ in range(6):
        for k in range(7):
            c.drawRect(skia.Rect.MakeXYWH(860 + k * 122, 160 + f_ * 110, 80, 64), fill("#0b0d12", a))
    c.drawRect(skia.Rect.MakeXYWH(560, base - 330, 260, 24), fill("#2e3446", a)); text(c, "TERRACE", 690, base - 345, 20, "sansb", "#8c7d60", a, spacing=3)
    c.drawRect(skia.Rect.MakeXYWH(860, base - 440, 80, 90), fill("#2a3142", a)); text(c, "WINDOW", 900, base - 455, 18, "sansb", "#8c7d60", a, spacing=2)
    c.drawRect(skia.Rect.MakeLTRB(0, base, W, H), fill("#0a0c08", a))
    for i in range(7): tree(c, 60 + i * 85, base, .7, a, "#0b1410", t, seed=i + 40)
    text(c, "PRIVATE GARDEN", 300, base + 60, 22, "sansb", "#6d8a6d", a, spacing=3)
    # sensor beam on terrace
    sensor_icon(c, "heat", 600, base - 360, 50, RED, a)
    Pb = skia.Path(); Pb.moveTo(600, base - 350); Pb.lineTo(820, base - 250); Pb.lineTo(820, base - 330); Pb.close(); c.drawPath(Pb, fill(RED, .12 * a))
    # climbers along garden -> terrace -> window
    pts = [(200, base), (520, base), (600, base - 330), (760, base - 330), (900, base - 350)]
    for k in range(3):
        p = clamp(climb - k * .14)
        if p <= 0: continue
        segs = [math.dist(pts[i], pts[i + 1]) for i in range(4)]; L = sum(segs) * p; i = 0
        while i < 3 and L > segs[i]: L -= segs[i]; i += 1
        f = L / segs[i]; x = lerp(pts[i][0], pts[i + 1][0], f); y = lerp(pts[i][1], pts[i + 1][1], f)
        person(c, x, y, 160, a=a * (1 - seg(p, .95, 1)), rim="#4a5a70", step=(t * 1.4 + k * .3) % 1, crouch=.5)
        if shield > 0 and i >= 1:
            c.drawRoundRect(skia.Rect.MakeXYWH(x + 18, y - 120, 40, 120), 6, 6, fill("#f4efe4", .55 * a * shield))

def sc_night(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        c.drawRect(skia.Rect.MakeXYWH(cx - 900, 120, 1800, 700), fill("#151821"))
        sensor_icon(c, "heat", cx + 260, 240, 160, GOLD, 1)
        c.drawRoundRect(skia.Rect.MakeXYWH(cx + 150, 190, 220, 80), 12, 12, stroke("#4a505e", 3))
        q = seg(t, d * .45, d * .8)
        c.drawRoundRect(skia.Rect.MakeXYWH(cx + 150, 190, 220, 120), 12, 12, fill("#f4efe4", .18 * q, 6))
        spray_can(c, cx - 180 + 80 * eo(seg(t, d * .2, d * .45)), 700, 1.4, a=ap(t, d * .15), spray=q * (1 - seg(t, d * .85, d)), t=t, toward=(1, -.95))
        label(c, "FRIDAY 14 FEBRUARY · VALENTINE'S DAY", 110, 90, 28, seg(t, .1, 1.5), align="l")
        text(c, "women's hairspray", cx - 560, 440, 48, "serifb", WHITE, ap(t, d * .3))
        text(c, "on the heat sensor", cx - 560, 510, 48, "serifb", GOLD, ap(t, d * .38))
        text(c, "It looks like nothing.", cx - 560, H - 120, 46, "serif", WHITE, ap(t, d * .85))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        facade(ctx, t, climb=seg(t, d * .1, d * .95), shield=seg(t, d * .5, d * .6))
        label(c, "SATURDAY NIGHT · AFTER MIDNIGHT", 110, 90, 28, seg(t, .1, 1.5), align="l")
        text(c, "a homemade polyester shield", 500, 300, 36, "serifb", GOLD, ap(t, d * .6))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        vault_door(c, cx + 330, cy + 40, 380, rot=0)
        x0 = cx - 360; y0 = cy - 120
        c.drawRect(skia.Rect.MakeXYWH(x0 - 90, y0, 80, 180), fill("#8a909c")); c.drawRect(skia.Rect.MakeXYWH(x0 + 10, y0, 80, 180), fill("#8a909c"))
        for (xx, yy) in ((x0 - 70, y0 + 20), (x0 - 70, y0 + 150), (x0 + 70, y0 + 20), (x0 + 70, y0 + 150)):
            r_ = t * 300 if t < d * .4 else d * .4 * 300
            c.drawCircle(xx, yy, 10, fill("#3a3f4e")); c.save(); c.translate(xx, yy); c.rotate(r_); c.drawLine(-7, 0, 7, 0, stroke("#c9c2b0", 3)); c.restore()
        text(c, "MAGNETIC PLATES", x0, y0 - 40, 30, "sansb", WHITE, ap(t, .2))
        text(c, "screws loosened in advance", x0, y0 + 240, 30, "serif", WHITE, ap(t, d * .2) * .85)
        q = seg(t, d * .45, d * .7)
        c.drawRoundRect(skia.Rect.MakeXYWH(x0 - 120, lerp(y0 - 400, y0 - 20, eo(q)), 240, 220), 8, 8, fill("#c9ccd4", .9 * ap(t, d * .45)))
        c.drawRoundRect(skia.Rect.MakeXYWH(x0 - 120, lerp(y0 - 400, y0 - 20, eo(q)), 240, 220), 8, 8, stroke("#ffffff", 3, ap(t, d * .45)))
        text(c, "ALUMINIUM", x0, lerp(y0 - 400, y0 - 20, eo(q)) + 120, 30, "sansb", INK, ap(t, d * .5))
        mark(c, x0 + 150, y0 - 60, 60, seg(t, d * .78, d * .9), False)
        label(c, "LAYER: MAGNETIC SENSOR", cx, 80, 26, seg(t, .1, 1.2))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        for i, (k, n, cover) in enumerate((("light", "LIGHT SENSOR", "TAPE"), ("heat", "HEAT SENSOR", "STYROFOAM BOX"))):
            x = cx - 450 + i * 900; y = 360; q = seg(t, .3 + i * d * .25, .9 + i * d * .25)
            sensor_icon(c, k, x, y, 200, GOLD, 1)
            if i == 0:
                c.save(); c.translate(x, y); c.rotate(-12)
                c.drawRect(skia.Rect.MakeXYWH(-140 * eo(q), -34, 280 * eo(q), 68), fill("#c9b37a", .95)); c.restore()
            else:
                yy = lerp(y - 400, y - 110, eo(q)); c.drawRect(skia.Rect.MakeXYWH(x - 150, yy, 300, 230), fill("#e9eef3", .95 * clamp(q * 3))); c.drawRect(skia.Rect.MakeXYWH(x - 150, yy, 300, 230), stroke("#9aa0ad", 3, clamp(q * 3)))
            text(c, n, x, y + 220, 36, "sansb", WHITE, ap(t, .2 + i * d * .2)); text(c, "→ " + cover, x, y + 280, 34, "sansb", GOLD, q)
        chip(c, "NO FORCED ENTRY · THEY KNEW THE CODE", cx, H - 120, a=ap(t, d * .62), size=40)
        c.restore()
    t, a, d = beat(ctx, 4)
    if a > 0:
        k = seg(t, d * .55, d * .65)
        def A():
            c.drawRect(skia.Rect.MakeXYWH(cx - 520, 140, 1040, 680), fill("#14120f")); c.drawRect(skia.Rect.MakeXYWH(cx - 520, 140, 1040, 680), stroke("#3a3226", 4))
            c.drawLine(cx - 200, 200, cx - 200, 260, stroke("#8a909c", 6)); c.drawCircle(cx - 200, 262, 10, fill("#8a909c"))
            key_long(c, cx - 200, 300, 520, rot=8 * math.sin(t * 1.5) + 80)
            text(c, "“hanging in a storage room”", cx + 220, 420, 42, "serifb", WHITE, ap(t, d * .15))
            text(c, "— Notarbartolo's account", cx + 220, 480, 30, "serif", GOLD, ap(t, d * .2))
            text(c, "Police: copied keys in the bags", cx + 220, 620, 36, "sansb", COP, ap(t, d * .35))
            label(c, "THE FOOT-LONG KEY", cx, 90, 28, seg(t, .1, 1.3))
        def B():
            vault_door(c, cx, cy + 20, 400, open=seg(t, d * .62, d * .98), rot=t * 20, inside=boxes_inside(cx, cy + 20, 400, 0, t))
            label(c, "THREE TONS OF STEEL", cx, 70, 28, 1)
        xfade(c, k, A, B)
        c.restore()
    t, a, d = beat(ctx, 5)
    if a > 0:
        n = int(lerp(0, 96, seg(t, .3, d * .55)))
        deposit_wall(c, cx - 900, 130, 16, 6, 85, 100, opened=n, t=t)
        floor_mess(c, cx, 760, 1900, t, a=.8, seed=9)
        c.drawRoundRect(skia.Rect.MakeXYWH(cx + 520, 160, 400, 330), 18, 18, fill("#07080b", .9))
        text(c, "05:30", cx + 720, 250, 60, "typeb", WHITE, ap(t, .2))
        text(c, str(int(lerp(0, 123, seg(t, .3, d * .55)))), cx + 720, 380, 110, "disp", GOLD, ap(t, .3))
        text(c, "boxes · police count", cx + 720, 430, 28, "sans", WHITE, ap(t, .3))
        text(c, "(his account: 109)", cx + 720, 470, 26, "serif", WHITE, ap(t, d * .5) * .7)
        chip(c, "ALARMS: 0", cx, H - 70, a=ap(t, d * .85), size=48, color=GREEN)
        c.restore()

# ------------------------------------------------------------------ the loot
def sc_loot(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        c.drawCircle(cx, cy, 420, fill(ICE, .06, 120))
        rnd = random.Random(8)
        for i in range(60):
            q = seg(t, i / 60 * d * .5, i / 60 * d * .5 + .6)
            if q > 0: gem(c, cx + rnd.uniform(-600, 600), lerp(-100, cy + 150 + rnd.uniform(-60, 200), eo(q)), rnd.uniform(26, 60), a=q, rot=rnd.uniform(-30, 30), shine=(i % 7 == 0) * .8)
        v = int(lerp(0, 100, eo(seg(t, .3, d * .55))))
        text(c, f"${v} MILLION", cx, 250, 140, "disp", GOLD, ap(t, .2))
        text(c, "police and insurers' estimate", cx, 320, 36, "serif", WHITE, ap(t, .4) * .85)
        chip(c, "THE BIGGEST DIAMOND HEIST IN HISTORY", cx, H - 70, a=ap(t, d * .6), size=38)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        for i, (who, num, l1, colr) in enumerate((("POLICE + INSURERS", "~$100M", "stolen from the boxes", COP), ("NOTARBARTOLO", "~$20M", "“we were set up”", GOLD))):
            x = cx - 430 + i * 860; q = ap(t, .3 + i * d * .2)
            c.drawRoundRect(skia.Rect.MakeXYWH(x - 380, cy - 280, 760, 470), 20, 20, fill("#ffffff", .05 * q)); c.drawRoundRect(skia.Rect.MakeXYWH(x - 380, cy - 280, 760, 470), 20, 20, stroke(colr, 4, q))
            label(c, who, x, cy - 200, 28, seg(t, .3 + i * d * .2, 1.5 + i * d * .2), colr, rule=False)
            text(c, num, x, cy - 30, 130, "disp", WHITE, q); text(c, l1, x, cy + 70, 40, "serifb", WHITE, q)
        text(c, "He says: an insurance scam on stones already gone.", cx, H - 170, 38, "serif", WHITE, ap(t, d * .45))
        text(c, "The book Flawless: his story doesn't hold up.", cx, H - 100, 38, "serifb", GOLD, ap(t, d * .78))
        label(c, "DISPUTED", cx, 110, 30, seg(t, .1, 1.2), RED)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        deposit_wall(c, cx - 820, 140, 12, 4, 95, 100, opened=30, t=t, gems=False)
        text(c, "¾ · no paperwork", cx - 250, 640, 46, "sansb", GOLD, ap(t, .3))
        text(c, "Nobody may ever know what was in those boxes.", cx - 250, 710, 36, "serif", WHITE, ap(t, d * .2))
        for i in range(3): trash_bag(c, cx + 480 + i * 130, H - 120, .9 + .1 * i, a=ap(t, d * .6 + i * .2), rot=(i - 1) * 6)
        text(c, "Last job: the rubbish.", cx + 600, H - 380, 44, "serifb", WHITE, ap(t, d * .75))
        c.restore()

# ------------------------------------------------------------------ the forest
def sc_forest(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        route(ctx, seg(t, .2, d * .8), "ANTWERP", "BRUSSELS", sp=520)
        label(c, "SUNDAY EVENING · THE E19", cx, 110, 30, seg(t, .1, 1.3))
        text(c, "Notarbartolo and Speedy", cx, H - 160, 50, "serifb", WHITE, ap(t, d * .3))
        text(c, "+ a bag of rubbish from the job", cx, H - 90, 40, "serif", GOLD, ap(t, d * .5))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        forest(ctx, t, cars=1)
        car(c, cx + 380, H * .9, .9, lights=1)
        q = seg(t, d * .45, d * .8)
        if q > 0:
            x = lerp(cx + 220, cx - 260, q); y = lerp(H * .8, H * .74, q) - math.sin(q * math.pi) * 200
            trash_bag(c, x, y, .55, rot=q * 300)
        person(c, cx + 230, H * .9, 220, rim="#9db58a", arms=seg(t, d * .35, d * .5))
        text(c, "Speedy is coming apart.", cx - 420, 160, 54, "serifb", WHITE, ap(t, .3))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        forest(ctx, t, road=False, dusk=False)
        c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill("#d8e4f0", .04))
        figure(c, cx - 450, H + 40, 1.9, hat=True, rim="#c9a56a")
        trash_bag(c, cx + 300, H * .86, .8, rot=8); trash_bag(c, cx + 470, H * .88, .6, rot=-10)
        for i, s in enumerate(("AUGUST VAN CAMP", "RETIRED GROCER · 59", "HATES LITTER")):
            chip(c, s, cx + 380, 200 + i * 110, a=ap(t, .2 + i * d * .2), size=40, color=GOLD if i < 2 else RED)
        label(c, "MONDAY · THE SAME DAY THE VAULT IS FOUND", cx, H - 40, 24, seg(t, d * .7, d * .7 + 1.2), WHITE, rule=False)
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        c.drawRect(skia.Rect.MakeXYWH(cx - 900, 160, 1800, 760), fill("#1e1a14"))
        for i in range(6): c.drawLine(cx - 900, 160 + i * 152, cx + 900, 160 + i * 152, stroke("#000000", 2, .25))
        label(c, "EVIDENCE · FOUND IN THE FOREST", cx, 110, 28, seg(t, .1, 1.3))
        objs = [(videotape, cx - 640, 400, 300, -8, "VIDEOTAPE"), (wine_bottle, cx - 230, 560, 1.15, 12, "WINE BOTTLE"), (envelope, cx + 200, 420, 300, 6, "DIAMOND CENTRE ENVELOPES")]
        for i, (f, x, y, s, r, n) in enumerate(objs):
            q = ap(t, .2 + i * d * .14)
            if q <= 0: continue
            if f is envelope: f(c, x, y, s, rot=r, a=q, seal=False); envelope(c, x + 70, y + 60, s, rot=-r, a=q, seal=False)
            else: f(c, x, y, s, rot=r, a=q)
            label(c, n, x, y + (230 if f is not wine_bottle else 60), 20, seg(t, .2 + i * d * .14, 1.4 + i * d * .14), WHITE, a=q, rule=False)
        q = seg(t, d * .7, d * .85)
        c.drawCircle(cx + 600, 650, 260, fill("#ffe2a0", .12 * q, 60))
        sandwich(c, cx + 600, 650, 420 * (1.2 - .2 * eo(q)), rot=-6, a=eo(q))
        text(c, "HALF A SALAMI SANDWICH", cx + 600, 830, 30, "sansb", GOLD, q, spacing=2)
        c.restore()

# ------------------------------------------------------------------ the rubbish talks
def sc_found(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        card(c, cx - 400, cy, 620, 720, rot=-3)
        text(c, "INVOICE", 310, 90, 52, "serifb", INK, spacing=4); c.drawLine(60, 120, 560, 120, stroke(INK, 2, cap=False))
        typed(c, "1 x surveillance system", 60, 220, 30, seg(t, .3, 1.6), color="#1d1a14")
        typed(c, "Buyer: L. Notarbartolo", 60, 290, 30, seg(t, 1.2, 2.4), color="#1d1a14")
        for i in range(6): c.drawRect(skia.Rect.MakeXYWH(60, 360 + i * 40, 420 - i * 30, 10), fill("#8a7c62", .5))
        P = skia.Path(); P.moveTo(620, 0)
        for i in range(12): P.lineTo(620 - (24 if i % 2 else 0), i * 60)
        c.drawPath(P, stroke("#14110c", 6))
        text(c, "ILLUSTRATION", 40, 690, 14, "sansb", "#8c7d60", align="l", spacing=3)
        c.restore()
        q = ap(t, d * .5)
        card(c, cx + 430, cy + 40, 540, 300, rot=4, a=q, color="#f4efe4")
        text(c, "ELIO D'ONORIO", 270, 120, 42, "serifb", INK, q, spacing=2); text(c, "business card", 270, 180, 26, "serif", "#5a4d38", q)
        text(c, "ILLUSTRATION", 30, 280, 12, "sansb", "#8c7d60", q, align="l", spacing=3)
        c.restore()
        label(c, "THE RUBBISH STARTS TO TALK", cx, 100, 28, seg(t, .1, 1.3))
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        sandwich(c, cx, 300, 520, rot=-4)
        for i, (who, l1, l2, colr) in enumerate((("SOME ACCOUNTS", "DNA", "on the sandwich", "#6fb8ff"), ("WIRED'S ACCOUNT", "A RECEIPT", "→ supermarket camera", GOLD))):
            x = cx - 430 + i * 860; q = ap(t, d * .15 + i * d * .3)
            c.drawRoundRect(skia.Rect.MakeXYWH(x - 360, 520, 720, 380), 20, 20, fill("#ffffff", .05 * q)); c.drawRoundRect(skia.Rect.MakeXYWH(x - 360, 520, 720, 380), 20, 20, stroke(colr, 4, q))
            label(c, who, x, 590, 26, seg(t, d * .15 + i * d * .3, 1.2 + d * .15 + i * d * .3), colr, rule=False)
            text(c, l1, x, 700, 80, "disp", WHITE, q); text(c, l2, x, 780, 38, "serif", WHITE, q)
        q = seg(t, d * .75, d * .85)
        if q > 0:
            c.save(); c.translate(cx + 430, 840); sensor_icon(c, "camera", 0, 0, 80, RED, q); c.restore()
            text(c, "THE MONSTER", cx + 430, 880, 30, "sansb", RED, q)
        label(c, "ACCOUNTS DIFFER", cx, 80, 26, seg(t, .1, 1.2), RED)
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        for i in range(10): layer_tile(c, cx - 810 + i * 180, 280, 150, ("dial", "key", "seismic", "magnet", "grate", "camera", "keypad", "light", "heat", "radar")[i], "", beaten=1)
        text(c, "Ten layers of security: beaten.", cx, 520, 58, "serifb", WHITE, ap(t, .2))
        figure(c, cx - 520, H + 40, 1.6, hat=True, rim="#c9a56a", a=ap(t, d * .35))
        text(c, "One retired grocer:", cx + 200, 700, 54, "serifb", WHITE, ap(t, d * .4))
        text(c, "not beaten.", cx + 200, 780, 64, "serifb", GOLD, ap(t, d * .55))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        k = seg(t, d * .6, d * .68)
        def A():
            building(c, cx, H * .82, floors=8, under=0, w=900, lit=.3)
            person(c, cx - 300, H * .82, 260, rim=NOT, step=(t * .7) % 1 if t < d * .3 else .25)
            for i in range(2): person(c, cx + 200 + i * 170, H * .82, 270, rim=COP, a=ap(t, d * .3 + i * .3))
            stamp(c, "RECOGNISED", cx, 200, 80, seg(t, d * .35, d * .35 + .35), rot=-5)
            label(c, "DAYS LATER · BACK FOR HIS MAIL (BY ONE ACCOUNT)", cx, 80, 24, seg(t, .1, 1.3))
        def B():
            c.drawRoundRect(skia.Rect.MakeXYWH(cx - 360, cy - 330, 720, 600), 20, 20, fill("#2a2e38")); c.drawRoundRect(skia.Rect.MakeXYWH(cx - 320, cy - 290, 640, 520), 12, 12, fill("#0b0c10"))
            for i in range(17):
                gem(c, cx - 240 + (i % 6) * 96, cy - 180 + (i // 6) * 140, 60, shine=(i % 5 == 0) * (.5 + .5 * math.sin(t * 4 + i)), a=ap(t, d * .68 + i * .05))
            label(c, "TURIN · HIS SAFE", cx, 120, 28, 1)
            text(c, "17 polished diamonds", cx, H - 90, 56, "serifb", GOLD, ap(t, d * .75))
        xfade(c, k, A, B)
        c.restore()

# ------------------------------------------------------------------ the trial
def sc_trial(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        w, h = 1200, 700; card(c, cx, cy + 20, w, h, rot=-.8)
        text(c, "COURT OF APPEAL · ANTWERP", w / 2, 90, 42, "serifb", INK, spacing=3); c.drawLine(80, 120, w - 80, 120, stroke(INK, 2, cap=False))
        text(c, "MAY 2005", w / 2, 165, 24, "serif", "#5a4d38", spacing=5)
        rows = [("Notarbartolo", "10 years + 1 million euro fine"), ("The Genius", "5 years"), ("The Monster", "5 years"), ("Speedy", "5 years"), ("The King of Keys", "never charged")]
        for i, (n, s) in enumerate(rows):
            q = ap(t, .3 + i * d * .12); y = 250 + i * 80
            text(c, n, 120, y, 36, "serifb", "#1d1a14", q, align="l"); text(c, s, w - 120, y, 34, "typeb", RED if i == 0 else "#3b3324", q, align="r")
        text(c, "SUMMARY", 60, h - 30, 14, "sansb", "#8c7d60", align="l", spacing=3)
        c.restore()
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        c.drawCircle(cx, cy - 40, 380, fill(ICE, .05, 120))
        q = seg(t, d * .2, d * .8); rnd = random.Random(12)
        for i in range(30):
            gem(c, cx + rnd.uniform(-520, 520), cy - 60 + rnd.uniform(-220, 200), rnd.uniform(36, 70), a=1 - q * rnd.uniform(.7, 1), shine=0)
        solid_stamp(c, "NEVER RECOVERED", cx, cy + 260, 86, rot=-5) if t > d * .6 else None
        label(c, "WHERE DID THE DIAMONDS GO?", cx, 110, 30, seg(t, .1, 1.3))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        figure(c, cx - 500, H + 40, 2.0, hat=False, rim=NOT)
        c.drawRoundRect(skia.Rect.MakeXYWH(cx - 100, cy - 260, 900, 420), 20, 20, fill("#0d1016", .95)); c.drawRoundRect(skia.Rect.MakeXYWH(cx - 100, cy - 260, 900, 420), 20, 20, stroke(GOLD, 3))
        label(c, "HIS VERSION · A DOCUMENTARY, 2025", cx + 350, cy - 190, 26, seg(t, .1, 1.3), rule=False)
        text(c, "Someone else ran the job.", cx + 350, cy - 60, 52, "serifb", WHITE, ap(t, d * .3))
        text(c, "My part was small.", cx + 350, cy + 20, 52, "serifb", GOLD, ap(t, d * .5))
        text(c, "(paraphrased)", cx + 350, cy + 110, 26, "serif", WHITE, ap(t, d * .5) * .6)
        c.restore()

# ------------------------------------------------------------------ the end
def sc_end(ctx):
    c, W, H, cx, cy = ctx.c, ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = beat(ctx, 0)
    if a > 0:
        k = seg(t, d * .25, d * .32)
        def A():
            c.drawRect(skia.Rect.MakeXYWH(cx - 300, 200, 600, 640), stroke("#4a505e", 6))
            for i in range(8): c.drawLine(cx - 300 + i * 85, 200, cx - 300 + i * 85, 840, stroke("#4a505e", 6))
            text(c, "PAROLE · MARCH 2009", cx, 140, 50, "disp", WHITE, ap(t, .2))
            person(c, lerp(cx, cx + 700, eo(seg(t, .5, d * .25))), H - 120, 300, rim=NOT, step=(t * .9) % 1)
        def B():
            c.drawRect(skia.Rect.MakeLTRB(0, H * .8, W, H), fill("#16181e"))
            car(c, cx - 300, H * .8, 1.5, lights=1, color="#1b2030")
            c.drawRoundRect(skia.Rect.MakeXYWH(cx - 600, H * .8 - 300, 200, 70), 10, 10, fill(PAPER, ap(t, d * .45)))
            for i in range(21):
                q = ap(t, d * .4 + i * .05)
                c.drawRect(skia.Rect.MakeXYWH(cx + 300 + (i % 7) * 70, 260 + (i // 7) * 90, 56, 70), fill(PAPER, q * .9))
                gem(c, cx + 328 + (i % 7) * 70, 300 + (i // 7) * 90, 26, a=q)
            text(c, "21 packets · about 1 kg of stones", cx + 510, 600, 34, "sansb", GOLD, ap(t, d * .5))
            text(c, "Lawyer: legal scrap, €10,000–18,000", cx + 510, 660, 32, "serif", WHITE, ap(t, d * .7))
            label(c, "MILAN · JULY 2009", cx, 110, 30, 1)
            stamp(c, "NEVER SETTLED", cx + 510, 780, 50, seg(t, d * .85, d * .85 + .35), rot=-4)
        xfade(c, k, A, B)
        c.restore()
    t, a, d = beat(ctx, 1)
    if a > 0:
        route(ctx, seg(t, .2, d * .5), "UNITED STATES", "PARIS", sp=560)
        stamp(c, "ARRESTED · 2013", cx - 360, cy + 300, 64, seg(t, d * .35, d * .35 + .35), rot=-6)
        text(c, "for breaking his parole", cx - 360, cy + 400, 34, "serif", WHITE, ap(t, d * .4))
        chip(c, "RELEASED 2017", cx + 400, cy + 330, a=ap(t, d * .8), size=44, color="#9db58a")
        label(c, "A TRIP ABOUT FILM RIGHTS TO HIS STORY", cx, 110, 28, seg(t, d * .5, d * .5 + 1.2))
        c.restore()
    t, a, d = beat(ctx, 2)
    if a > 0:
        skyline(c, W, H * .8, 77, "#1b1f2d", 1, 60, 160, 0, lit=.08)
        c.drawRect(skia.Rect.MakeLTRB(0, H * .8, W, H), fill("#0b0d12"))
        figure(c, cx + 520, H + 40, 1.4, hat=False, rim=NOT, a=.9)
        label(c, "NEAR TURIN · TODAY (REPORTEDLY)", cx, 110, 28, seg(t, .1, 1.3))
        for i in range(5): gem(c, cx - 600 + i * 150, cy - 40, 70, a=.25 + .15 * math.sin(t * 2 + i), shine=0)
        text(c, "up to $100,000,000", cx - 300, cy + 110, 56, "disp", GOLD, ap(t, d * .45))
        text(c, "never found", cx - 300, cy + 180, 44, "serifb", WHITE, ap(t, d * .6))
        c.restore()
    t, a, d = beat(ctx, 3)
    if a > 0:
        k = seg(t, d * .45, d * .52)
        def A():
            kinds = ("dial", "key", "seismic", "magnet", "grate", "camera", "keypad", "light", "heat", "radar")
            for i, kk in enumerate(kinds): layer_tile(c, cx - 810 + i * 180, 360, 150, kk, "", a=ap(t, .1 + i * .06))
            text(c, "100,000,000 combinations", cx, 600, 56, "disp", WHITE, ap(t, d * .15))
            text(c, "A vault no one had ever beaten.", cx, 700, 50, "serifb", GOLD, ap(t, d * .3))
            label(c, "“THE HEIST OF THE CENTURY”", cx, 130, 30, seg(t, .1, 1.3))
        def B():
            forest(ctx, t, road=False)
            c.drawRect(skia.Rect.MakeLTRB(0, 0, W, H), fill("#07080b", .45))
            person(c, cx - 620, H * .86, 260, rim="#9db58a", a=ap(t, d * .5))
            figure(c, cx - 200, H + 40, 1.2, hat=True, rim="#c9a56a", a=ap(t, d * .58))
            c.drawCircle(cx + 420, cy + 100, 300, fill("#ffe2a0", .1, 70))
            sandwich(c, cx + 420, cy + 100, 520, rot=-5, a=ap(t, d * .66))
            text(c, "a nervous man · an angry grocer · half a sandwich", cx, 150, 44, "serifb", WHITE, ap(t, d * .6))
            text(c, "The diamonds are still out there.", cx, H - 60, 52, "serifb", GOLD, ap(t, d * .85))
        xfade(c, k, A, B)
        c.restore()

def sc_outro(ctx):
    c, cx, cy, t = ctx.c, ctx.cx, ctx.cy, ctx.t
    stamp(c, "CASE CLOSED", cx, cy - 110, 150, seg(t, .15, .45), rot=-5)
    label(c, "CASE CLOSED FILES", cx, cy + 110, 30, seg(t, .6, 1.4), GOLD)
    text(c, "New case every week. Subscribe so you don't miss it.", cx, cy + 210, 40, "serif", WHITE, ap(t, 1.1))

SCENES = {k[3:]: v for k, v in list(globals().items()) if k.startswith("sc_") and callable(v)}
HITS = [("cold", 3, 0, .45), ("district", 5, 0, .82), ("tenant", 4, 0, .65), ("crew", 3, 0, .78), ("crew", 4, 0, .35), ("night", 2, 0, .78),
        ("night", 5, 0, .85), ("forest", 3, 0, .7), ("found", 3, 0, .35), ("trial", 1, 0, .6), ("end", 0, 0, .85), ("end", 1, 0, .35), ("outro", -1, .15, 0)]
SHORT_HITS = []
WARM = {}

THUMB_WORDS = [(["ONE BAD", "LUNCH."], 130), (["$100M", "GONE."], 150), (["ZERO", "ALARMS."], 130)]
def thumbnail(c, W, H, word):
    word, size = word
    sh = skia.GradientShader.MakeRadial(center=(W * .34, H * .55), radius=900, colors=[col("#2a3348"), col("#141824"), col("#07080b")], positions=[0, .5, 1])
    c.drawPaint(skia.Paint(Shader=sh))
    vault_door(c, W * .3, H * .55, 300, open=.0, rot=20)
    c.drawCircle(W * .3, H * .62, 300, fill("#ffcf7a", .1, 90))
    sandwich(c, W * .3, H * .78, 470, rot=-6)
    for i, (gx, gy) in enumerate(((.06, .14), (.55, .16), (.58, .5), (.05, .55))): gem(c, W * gx, H * gy, 58, shine=.9 if i % 2 == 0 else 0)
    figure(c, W * .84, H + 30, 1.45, hat=False, rim=GOLD)
    for i, ln in enumerate(word):
        sz = size
        while tw(ln, "sansb", sz) > 560: sz -= 6
        big_word(c, ln, W * .76, H * .24 + i * size * 1.02, sz, "#ffd36b")


# ---------------- shorts (60-100 s, 9:16) ----------------
from shorts import hook_card, cta_card
def _door(c, cx, cy, t, d): vault_door(c, cx, cy + 160, 330, rot=t * 15, a=.9 * eo(seg(t, 0, .8)))
def _spray(c, cx, cy, t, d): spray_can(c, cx + 300, cy + 240, 1.6, a=.9 * eo(seg(t, 0, .8)), spray=1, t=t, toward=(-1, -.6))
def _bag(c, cx, cy, t, d):
    q = .9 * eo(seg(t, 0, .8)); trash_bag(c, cx - 250, cy + 260, 1.1, a=q, rot=-6); sandwich(c, cx + 220, cy + 180, 380, rot=-8, a=q)
SCENES["hook_a"] = hook_card(["10 LAYERS.", "0 ALARMS."], stamp_text="ANTWERP 2003", prop=_door)
SCENES["hook_b"] = hook_card(["STEP ONE:", "HAIRSPRAY."], stamp_text="THE HOW", prop=_spray, rim=GOLD)
SCENES["hook_c"] = hook_card(["$100 MILLION.", "ONE BAD BAG."], stamp_text="THE MISTAKE", prop=_bag)
SCENES["cta_a"] = cta_card("CASE 004 · ANTWERP", "PART 2 NEXT")
SCENES["cta_b"] = cta_card("CASE 004 · ANTWERP", "PART 3 NEXT")
SCENES["cta_c"] = cta_card("CASE 004 · ANTWERP", "FULL CASE")
SHORT_HITS += [("hook_a", -1, .15, .62), ("hook_b", -1, .15, .62), ("hook_c", -1, .15, .62)]
SHORT_VIEW = {}
