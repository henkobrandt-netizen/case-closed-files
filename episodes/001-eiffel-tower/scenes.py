from lib import *

def sc_cold(ctx):
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = ctx.ph(0)
    if a > 0:
        ctx.layer(a); paris(ctx, shift=-t * 9)
        label(c, "PARIS · 1925", 130, 150, 34, seg(t, .3, 1.6), align="l")
        label(c, "A PRIVATE SUITE · ONE OF THE CITY'S GRANDEST HOTELS", 130, 215, 18, seg(t, 3.0, 5.0), WHITE, .8, rule=False, align="l")
        for i in range(3): banknote(c, 300 + i * 70, lerp(H + 200, H - 170 - i * 20, ap(t, 6.4 + i * .25, .8)), 300, rot=-12 + i * 9)
        c.restore()
    t, a, d = ctx.ph(1)
    if a > 0:
        ctx.layer(a)
        tower(c, cx - 400, H * .93, 860, color="#0e1017", lattice=GOLD, reveal=eio(seg(t, 0, 3.2)), glow=26)
        v = int(7000 * eo(seg(t, 2.6, 5.2)))
        text(c, f"{v:,}", cx + 330, cy + 10, 210, "disp", GOLD, ap(t, 2.4))
        label(c, "TONNES OF IRON", cx + 330, cy + 90, 34, seg(t, 3.2, 4.6), WHITE)
        text(c, "“You may know it better as the Eiffel Tower.”", cx + 330, cy + 220, 34, "serif", WHITE, ap(t, d * .62) * .85)
        c.restore()
    t, a, d = ctx.ph(2)
    if a > 0:
        ctx.layer(a)
        figure(c, cx - 480, H + 40, 2.3, rim=GOLD)
        label(c, "THE SELLER", cx + 40, cy - 250, 24, seg(t, .2, 1.2), align="l")
        item(c, "WORKS FOR THE GOVERNMENT", cx + 100, cy - 130, 40, t, .6, ok=False)
        item(c, "OWNS THE TOWER", cx + 100, cy - 20, 40, t, d * .36, ok=False)
        item(c, "LEAVING FRANCE WITHIN THE HOUR", cx + 100, cy + 90, 40, t, d * .56, ok=True, color=GOLD)
        c.restore()
    t, a, d = ctx.ph(3)
    if a > 0:
        ctx.layer(a)
        tower(c, cx, H * .95, 900, color="#0e1017", lattice=GOLD, glow=30)
        stamp(c, "SOLD", cx - 60, cy - 30, 190, seg(t, 3.0, 3.4))
        stamp(c, "SOLD AGAIN", cx + 110, cy + 230, 110, seg(t, d * .78, d * .78 + .4), rot=7)
        c.restore()

def sc_title(ctx):
    c = ctx.c; cx, cy, t = ctx.cx, ctx.cy, ctx.t
    tower(c, cx, ctx.H * 1.02, 1000, color="#12141d", a=.9, lattice="#2a2f40")
    label(c, "CASE CLOSED FILES  ·  NO. 001", cx, cy - 190, 26, seg(t, .1, .7))
    text(c, "THE MAN WHO SOLD", cx, cy - 40 + (1 - ap(t, .2, .6)) * 30, 120, "disp", WHITE, ap(t, .2, .6), spacing=4)
    text(c, "THE EIFFEL TOWER", cx, cy + 110 + (1 - ap(t, .5, .6)) * 30, 150, "disp", GOLD, ap(t, .5, .6), spacing=4)
    text(c, "A true story · Paris, 1925", cx, cy + 220, 34, "serif", WHITE, ap(t, 1.0) * .8)

def sc_who(ctx):
    c = ctx.c; W, H, cx, cy, t = ctx.W, ctx.H, ctx.cx, ctx.cy, ctx.t
    t0, _, d0 = ctx.ph(0); t1, _, d1 = ctx.ph(1); t2, a2, d2 = ctx.ph(2)
    ca = 1 - seg(t, ctx.cues[2] - .5, ctx.cues[2])
    if ca > 0:
        ctx.layer(ca); w, h = 1240, 640
        c.save(); c.translate(cx, cy - 20); c.scale(1.2, 1.2); c.translate(-cx, -cy + 20)
        card(c, cx, cy - 20 + (1 - ap(t, 0, .8)) * 80, w, h, rot=-1.2)
        text(c, "DOSSIER", 60, 80, 40, "sansb", INK, align="l", spacing=10); text(c, "FILE 001", w - 60, 80, 22, "type", "#5a4d38", align="r")
        c.drawLine(60, 104, w - 60, 104, stroke(INK, 2, cap=False))
        c.drawRect(skia.Rect.MakeXYWH(60, 140, 330, 430), fill("#1b1e29"))
        c.save(); c.clipRect(skia.Rect.MakeXYWH(60, 140, 330, 430)); figure(c, 225, 590, 1.25, color="#07080b", rim=GOLD); c.restore()
        rows = [("NAME", "Victor Lustig", 1.2), ("BORN", "1890, Austria-Hungary", 4.4), ("LANGUAGES", "Several", 7.6), ("STYLES HIMSELF", "“Count” Lustig", d0 - 2.2)]
        for i, (k, v, ts) in enumerate(rows):
            y = 190 + i * 100
            text(c, k, 450, y, 18, "sansb", "#7a6a4c", ap(t0, ts - .3), align="l", spacing=4)
            typed(c, v, 450, y + 44, 40, seg(t0, ts, ts + .9), color="#1d1a14", cursor=True)
        if t1 > 0:
            stamp(c, "NOT A COUNT", 960, 400, 66, seg(t1, .5, .9), rot=-7)
            text(c, "ALIASES", 840, 190, 18, "sansb", "#7a6a4c", ap(t1, 3.2), align="l", spacing=4)
            typed(c, "Dozens", 840, 234, 40, seg(t1, 3.4, 4.0), color="#1d1a14")
        c.restore(); c.restore()
        if t1 > d1 * .52:
            label(c, "HIS REAL TALENT: KNOWING WHAT YOU WANT TO BELIEVE", cx, H - 60, 28, seg(t1, d1 * .52, d1 * .52 + 1.6))
        c.restore()
    if a2 > 0:
        ctx.layer(a2); liner(ctx, t2, d2)
        for i, (s, f) in enumerate((("BORED", .52), ("TRAPPED", .62), ("NO ONE TO CHECK A STORY", .72))):
            item(c, s, 150, H * .26 + i * 70, 34, t2, d2 * f, color=WHITE)
        c.restore()

def sc_box(ctx):
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy
    t0, _, d0 = ctx.ph(0); t1, _, d1 = ctx.ph(1); t2, a2, d2 = ctx.ph(2)
    ba = 1 - seg(ctx.t, ctx.cues[2] - .5, ctx.cues[2])
    if ba > 0:
        ctx.layer(ba)
        c.translate(cx, cy); c.scale(1.3, 1.3); c.translate(-cx, -cy)
        moneybox(ctx, t0, d0, t1, d1)
        label(c, "THE MONEY BOX", cx, 215, 24, seg(t0, .3, 1.5))
        text(c, "$100 in", cx - 520, cy - 80, 40, "serif", WHITE, ap(t0, d0 * .22) * (1 - seg(t1, 0, .5)))
        text(c, "$200 out", cx + 520, cy - 215, 40, "serif", GOLD, ap(t0, d0 * .88) * (1 - seg(t1, d1 * .4, d1 * .45)))
        if t1 > 0:
            text(c, "Loaded in advance with real bills.", cx, H - 200, 36, "serif", WHITE, ap(t1, d1 * .14) * (1 - seg(t1, d1 * .42, d1 * .46)))
            text(c, "Sold for thousands of dollars.", cx, H - 200, 36, "serif", GOLD, ap(t1, d1 * .47) * (1 - seg(t1, d1 * .68, d1 * .72)))
            fa = ap(t1, d1 * .66) * (1 - seg(t1, d1 * .82, d1 * .98))
            figure(c, cx + 640, H + 30, 1.5, a=fa * .9, rim=GOLD)
            text(c, "By the time it stopped, he was gone.", cx, H - 200, 36, "serif", WHITE, ap(t1, d1 * .74))
        c.restore()
    if a2 > 0:
        ctx.layer(a2)
        p = eo(seg(t2, 0, 1.6)); z = 1 + .12 * seg(t2, 1.6, d2)
        c.translate(cx, cy); c.scale(z, z); c.translate(-cx, -cy)
        newspaper(ctx, cx, lerp(H + 600, cy + 60, p), 900, 940, 2.5, ["THE EIFFEL TOWER:", "TOO COSTLY TO KEEP?"], "The bill for repairs keeps growing", "PARIS · SPRING 1925",
                  hp=seg(t2, d2 * .45, d2 * .75), circle=seg(t2, d2 * .8, d2 * .97))
        c.restore()

def sc_idea(ctx):
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = ctx.ph(0)
    if a > 0:
        ctx.layer(a); tx, ty, th = cx - 470, H * .93, 860
        tower(c, tx, ty, th, color="#1a1d28", lattice="#566080", reveal=1, la=.5)
        P = tower_path(th); c.save(); c.translate(tx, ty); c.clipPath(P, True); rnd = random.Random(9)
        for i in range(26):
            q = seg(t, d * .5 + i * .22, d * .5 + i * .22 + 1.2); yy = -rnd.uniform(.02, .8) * th; xx = rnd.uniform(-.2, .2) * th * (1 + yy / th) ** 1.5
            if q > 0: c.drawCircle(xx, yy, rnd.uniform(18, 50) * eo(q), fill("#c05a26", .75 * q, 9))
        c.restore()
        x = cx + 20
        item(c, "BUILT FOR THE 1889 WORLD'S FAIR", x, cy - 250, 46, t, d * .14, color=WHITE)
        item(c, "NEVER MEANT TO BE PERMANENT", x, cy - 160, 46, t, d * .36, color=WHITE)
        item(c, "36 YEARS LATER: RUST", x, cy - 70, 46, t, d * .52, color="#e07a3c")
        if t > d * .7:
            label(c, "COST OF REPAIRS AND REPAINTING", x, cy + 60, 26, seg(t, d * .7, d * .7 + 1), RED, rule=False, align="l")
            bar(c, x, cy + 90, 760, 30, eo(seg(t, d * .72, d * .98)), RED)
        c.restore()
    t, a, d = ctx.ph(1)
    if a > 0:
        ctx.layer(a)
        newspaper(ctx, cx, cy + 30, 1100, 620, -1.5, ["WOULD PARIS BE BETTER", "OFF WITHOUT IT?"], "Some wonder whether the tower is worth saving", "PARIS · SPRING 1925", hp=seg(t, .2, 2.4))
        text(c, "Most readers turned the page.", cx, 110, 36, "serif", WHITE, ap(t, d * .5) * (1 - seg(t, d * .7, d * .74)))
        stamp(c, "BUSINESS PLAN", cx + 130, cy + 150, 96, seg(t, d * .76, d * .76 + .35), rot=-8, color="#9a6a12")
        c.restore()

def sc_letter(ctx):
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy
    t0, _, d0 = ctx.ph(0); t1, _, d1 = ctx.ph(1)
    la = 1 - seg(t1, d1 * .42, d1 * .5)
    if la > 0:
        ctx.layer(la)
        letter(ctx, t0, d0, cx - 420, cy + 10, h=930)
        x = cx + 110
        label(c, "STEP ONE", x, cy - 240, 22, seg(t0, .4, 1.2), align="l", rule=False)
        text(c, "Forge the letterhead.", x, cy - 180, 54, "serif", WHITE, ap(t0, .6), align="l")
        label(c, "STEP TWO", x, cy - 60, 22, seg(t0, d0 * .62, d0 * .62 + .8), align="l", rule=False)
        text(c, "Invent a title.", x, cy, 54, "serif", WHITE, ap(t0, d0 * .64), align="l")
        text(c, "“Deputy Director General”", x, cy + 70, 44, "serifb", GOLD, ap(t0, d0 * .78), align="l")
        if t1 > 0:
            label(c, "STEP THREE", x, cy + 190, 22, seg(t1, .3, 1.1), align="l", rule=False)
            text(c, "Invite the scrap dealers.", x, cy + 250, 54, "serif", WHITE, ap(t1, .5), align="l")
            for i in range(5):
                q = seg(t1, 1.4 + i * .28, 2.3 + i * .28)
                if q > 0: envelope(c, lerp(cx - 300, x + 80 + i * 150, eo(q)), lerp(cy, cy + 370, eo(q)), 130, rot=lerp(-40, -8 + i * 4, q), a=seg(q, 0, .2))
        c.restore()
    ha = seg(t1, d1 * .44, d1 * .54)
    if ha > 0:
        ctx.layer(ha); hotel(ctx, t=t1)
        label(c, "HÔTEL DE CRILLON", cx, 150, 44, seg(t1, d1 * .5, d1 * .5 + 1.4))
        text(c, "Place de la Concorde, Paris", cx, 230, 32, "serif", WHITE, ap(t1, d1 * .58) * .85)
        text(c, "Where real ministers really did business.", cx, H - 60, 34, "serif", GOLD, ap(t1, d1 * .8))
        c.restore()

def sc_pitch(ctx):
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy
    t0, _, d0 = ctx.ph(0); t1, _, d1 = ctx.ph(1); t2, _, d2 = ctx.ph(2)
    sh = 0
    if 1.0 < t1 < 1.35: sh = math.sin(t1 * 90) * 10 * (1.35 - t1) / .35
    c.save(); c.translate(sh, sh * .6)
    rims = [seg(t2, .3 + i * .5, 1.0 + i * .5) if t2 > 0 else 0 for i in range(5)]
    table(ctx, rims, envs=seg(t2, d2 * .7, d2 * .95) if t2 > 0 else 0)
    f0 = 1 - seg(ctx.t, ctx.cues[1] - .4, ctx.cues[1])
    if f0 > 0:
        xl, xr = cx - 900, cx + 330
        item(c, "TOO COSTLY TO MAINTAIN", xl + 60, cy - 340, 40, t0, d0 * .27, color=WHITE)
        item(c, "TO BE SOLD FOR SCRAP", xl + 60, cy - 260, 40, t0, d0 * .47, color=RED)
        if t0 > d0 * .66:
            v = int(7000 * eo(seg(t0, d0 * .66, d0 * .82)))
            text(c, f"{v:,} TONNES", xr, cy - 310, 64, "disp", GOLD, ap(t0, d0 * .66) * f0, align="l")
            text(c, "to the highest bidder", xr, cy - 250, 36, "serif", WHITE, ap(t0, d0 * .86) * f0, align="l")
    if t1 > 0 and t2 <= .4:
        f1 = 1 - seg(t2, 0, .4)
        c.saveLayerAlpha(None, int(255 * f1))
        text(c, "One condition.", cx, 130, 44, "serif", WHITE, ap(t1, .2))
        stamp(c, "CONFIDENTIAL", cx - 520, cy - 230, 80, seg(t1, 1.0, 1.3), rot=-8)
        label(c, "NOT A WORD UNTIL IT IS SIGNED", cx + 520, cy - 230, 24, seg(t1, d1 * .55, d1 * .55 + 1.4), WHITE)
        c.restore()
    if t2 > 0:
        text(c, "The secrecy made them feel chosen.", cx, 130, 46, "serif", GOLD, ap(t2, 1.2) * (1 - seg(t2, d2 * .52, d2 * .56)))
        text(c, "A site visit to the tower. Then: sealed bids.", cx, 130, 46, "serif", WHITE, ap(t2, d2 * .58))
    c.restore()

def sc_mark(ctx):
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy
    t0, _, d0 = ctx.ph(0); t1, _, d1 = ctx.ph(1); t2, a2, d2 = ctx.ph(2)
    pa = 1 - seg(ctx.t, ctx.cues[2] - .5, ctx.cues[2])
    if pa > 0:
        ctx.layer(pa)
        row = 1 - seg(t0, 2.2, 3.0)
        for k in range(5):
            if k == 3: continue
            figure(c, cx + (k - 2) * 300, cy + 330, .95, hat=False, rim="#2b3044", a=row * .9)
        z = eio(seg(t0, 2.2, 3.2))
        figure(c, lerp(cx + 300, cx - 500, z), lerp(cy + 330, H + 60, z), lerp(.95, 2.1, z), hat=False, rim=GOLD if t0 > 1.6 else "#2b3044")
        x = cx - 20
        label(c, "THE MARK", x, cy - 300, 22, seg(t0, 2.6, 3.4), align="l", rule=False)
        text(c, "André Poisson", x, cy - 220, 84, "disp", WHITE, ap(t0, 2.8), align="l")
        f = 1 - seg(t1, 0, .5)
        item(c, "NEW TO PARIS", x + 50, cy - 110, 40, t0, d0 * .34, color=col_fade(WHITE, f))
        item(c, "AMBITIOUS", x + 50, cy - 40, 40, t0, d0 * .44, color=col_fade(WHITE, f))
        item(c, "DESPERATE TO BE TAKEN SERIOUSLY", x + 50, cy + 30, 40, t0, d0 * .54, color=col_fade(WHITE, f))
        text(c, "This deal would make his name.", x, cy + 150, 48, "serif", GOLD, ap(t0, d0 * .82) * f, align="l")
        if t1 > 0:
            for i, (s, fr) in enumerate((("Why the hotel?", .56), ("Why the hurry?", .7), ("Why all the secrecy?", .84))):
                text(c, s, x + 20 + i * 40, cy - 90 + i * 84, 56, "serif", "#f08a7c", ap(t1, d1 * fr), align="l")
            c.save(); c.translate(-cx + x + 380, 0); suspicion(ctx, .08 + .8 * eo(seg(t1, d1 * .3, d1 * .95)), cy + 260, ap(t1, .4), w=760); c.restore()
        c.restore()
    if a2 > 0:
        ctx.layer(a2)
        figure(c, cx - 520, H + 60 + (1 - ap(t2, 0, 1)) * 80, 2.2, rim=GOLD)
        text(c, "What Lustig did next", cx + 180, cy - 30, 76, "disp", WHITE, ap(t2, .2))
        text(c, "is why con men still study him.", cx + 180, cy + 70, 56, "serif", GOLD, ap(t2, 1.6))
        c.restore()

def sc_bribe(ctx):
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy
    t0, _, d0 = ctx.ph(0); t1, _, d1 = ctx.ph(1); t2, a2, d2 = ctx.ph(2)
    pa = 1 - seg(ctx.t, ctx.cues[2] - .5, ctx.cues[2])
    if pa > 0:
        ctx.layer(pa)
        two(ctx, env=seg(t1, .3, 2.0) if t1 > 0 else None)
        label(c, "A PRIVATE MEETING", cx, 110, 24, seg(t0, .3, 1.6))
        q = [("“I am only a civil servant.”", .3, .47), ("“Expected to live well. Paid very little.”", .47, .72), ("“Perhaps we could come to an arrangement…”", .8, 1.01)]
        for s, f0, f1 in q:
            al = ap(t0, d0 * f0) * (1 - seg(t0, d0 * f1 - .4, d0 * f1)) if f1 < 1 else ap(t0, d0 * f0) * (1 - seg(t1, 0, .5))
            text(c, s, cx, cy - 250, 52, "serif", WHITE, al)
        if t1 > 0:
            stamp(c, "A BRIBE", cx, cy - 270, 100, seg(t1, .6, .95), rot=-5)
            v = lerp(.88, .04, eio(seg(t1, d1 * .2, d1 * .5)))
            suspicion(ctx, v, cy - 110, ap(t1, d1 * .16))
            text(c, "Only a real official would be this corrupt.", cx, H - 70, 40, "serif", GOLD, ap(t1, d1 * .62))
        c.restore()
    if a2 > 0:
        ctx.layer(a2)
        text(c, "He cured the doubt", cx, cy - 30, 96, "disp", WHITE, ap(t2, .1))
        text(c, "by confessing to a smaller crime.", cx, cy + 90, 72, "disp", GOLD, ap(t2, 1.5))
        c.restore()

def sc_payoff(ctx):
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = ctx.ph(0)
    if a > 0:
        ctx.layer(a); k = seg(t, d * .58, d * .66)
        if k < 1:
            c.saveLayerAlpha(None, int(255 * (1 - k)))
            notes_pile(ctx, seg(t, .2, d * .5), cx, cy + 250, n=18, w=330)
            text(c, "Poisson paid.", cx, 150, 64, "disp", WHITE, ap(t, .1))
            item(c, "THE PRICE OF THE TOWER", cx + 330, cy - 60, 30, t, d * .33, color=WHITE)
            item(c, "+ THE BRIBE", cx + 330, cy + 10, 30, t, d * .43, color=GOLD)
            c.restore()
        if k > 0:
            c.saveLayerAlpha(None, int(255 * k)); route(ctx, seg(t, d * .64, d * .98), "PARIS", "VIENNA", sp=520); c.restore()
        c.restore()
    t, a, d = ctx.ph(1)
    if a > 0:
        ctx.layer(a); k = seg(t, d * .6, d * .68)
        if k < 1:
            c.saveLayerAlpha(None, int(255 * (1 - k)))
            day = 1 + int(seg(t, d * .12, d * .5) * 13)
            for i in range(3, 0, -1): card(c, cx - 300 + i * 14, cy + 40 - i * 12, 760, 520, rot=-3 + i * 1.5, a=.6); c.restore()
            newspaper(ctx, cx - 300, cy + 40, 760, 520, -3 + (day % 2) * 1.2, ["NOTHING TO REPORT"], "", "PARIS · MORNING EDITION")
            text(c, f"DAY {day}", cx + 420, cy - 160, 110, "disp", GOLD, ap(t, d * .1))
            item(c, "NO STORY", cx + 330, cy - 30, 40, t, d * .46, ok=False)
            item(c, "NO POLICE", cx + 330, cy + 60, 40, t, d * .52, ok=False)
            c.restore()
        if k > 0: poisson_alone(ctx, t - d * .6, k)
        c.restore()

def sc_twice(ctx):
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = ctx.ph(0)
    if a > 0:
        ctx.layer(a); k = seg(t, d * .3, d * .38)
        if k < 1:
            c.saveLayerAlpha(None, int(255 * (1 - k))); route(ctx, seg(t, .3, d * .3), "PARIS", "VIENNA", rev=True, sp=520)
            text(c, "He went back.", cx, 150, 64, "disp", WHITE, ap(t, d * .2)); c.restore()
        if k > 0:
            c.saveLayerAlpha(None, int(255 * k))
            tower(c, cx - 450, H * .93, 860, color="#0e1017", lattice=GOLD, glow=24)
            stamp(c, "SOLD", cx - 470, cy - 80, 110, 1, rot=-10, a=.5)
            x = cx + 120
            item(c, "SAME CITY", x, cy - 200, 46, t, d * .44, ok=True)
            item(c, "SAME TOWER", x, cy - 100, 46, t, d * .54, ok=True)
            item(c, "SAME STORY", x, cy, 46, t, d * .64, ok=True)
            item(c, "NEW SCRAP DEALERS", x, cy + 100, 46, t, d * .78, ok=True, color=GOLD)
            stamp(c, "FOR SALE AGAIN", cx - 380, cy + 150, 78, seg(t, d * .86, d * .86 + .35), rot=6)
            c.restore()
        c.restore()
    t, a, d = ctx.ph(1)
    if a > 0:
        ctx.layer(a); k = seg(t, d * .46, d * .56)
        if k < 1:
            c.saveLayerAlpha(None, int(255 * (1 - k)))
            pul = .5 + .5 * math.sin(t * 7)
            c.drawPaint(skia.Paint(Color=col(RED, .10 + .12 * pul)))
            figure(c, cx, H + 40, 2.0, rim=RED)
            text(c, "This time, one of them", cx, 150, 56, "serif", WHITE, ap(t, .1)); text(c, "went to the police.", cx, 225, 56, "serifb", "#f08a7c", ap(t, .9))
            c.restore()
        if k > 0:
            c.saveLayerAlpha(None, int(255 * k)); liner(ctx, t - d * .46, d * .54 + .4, lab="NEXT STOP: AMERICA"); c.restore()
        c.restore()

def sc_america(ctx):
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy
    t0, _, d0 = ctx.ph(0); t1, _, d1 = ctx.ph(1); t2, a2, d2 = ctx.ph(2)
    pa = 1 - seg(ctx.t, ctx.cues[2] - .5, ctx.cues[2])
    if pa > 0:
        ctx.layer(pa); ny(ctx, .7)
        label(c, "AMERICA", cx, 110, 30, seg(t0, .2, 1.2))
        fa = ap(t0, d0 * .12, .8); xl, xr = cx - 480, cx + 480
        figure(c, xl, H + 30, 1.9, wide=1.25, rim="#b8c4e0", a=fa); figure(c, xr, H + 30, 1.7, rim=GOLD, a=fa)
        label(c, "AL CAPONE", xl, cy - 330, 24, seg(t0, d0 * .16, d0 * .16 + .8), WHITE, rule=False); label(c, "LUSTIG", xr, cy - 300, 24, seg(t0, d0 * .16, d0 * .16 + .8), GOLD, rule=False)
        g = seg(t0, d0 * .3, d0 * .44); bk = seg(t0, d0 * .7, d0 * .86)
        if g > 0 and t1 <= .3:
            x = lerp(xl + 160, xr - 160, eio(g)) if bk <= 0 else lerp(xr - 160, xl + 160, eio(bk))
            chip(c, "$50,000", x, cy + 60, a=seg(g, 0, .2) * (1 - seg(t1, 0, .3)), color="#9db58a")
        text(c, "Two months later: every cent returned.", cx, cy - 150, 40, "serif", WHITE, ap(t0, d0 * .62) * (1 - seg(t1, 0, .4)))
        if t1 > 0:
            g2 = seg(t1, d1 * .25, d1 * .5)
            if g2 > 0: chip(c, "$5,000", lerp(xl + 160, xr - 160, eio(g2)), cy + 60, a=seg(g2, 0, .2))
            text(c, "A reward, for his “honesty”.", cx, cy - 150, 40, "serif", WHITE, ap(t1, d1 * .2) * (1 - seg(t1, d1 * .62, d1 * .66)))
            text(c, "Which was all Lustig had wanted.", cx, cy - 150, 44, "serifb", GOLD, ap(t1, d1 * .68))
        c.restore()
    if a2 > 0:
        ctx.layer(a2); t = t2; d = d2
        for r in range(5):
            for k in range(9):
                x = ((k * 330 + t * (190 + r * 26) + r * 120) % (W + 400)) - 200
                banknote(c, x, 170 + r * 200, 250, rot=-6 + r * 3, a=.5)
        c.drawRect(skia.Rect.MakeXYWH(cx - 640, cy - 190, 1280, 400), fill("#07080b", .82, 40))
        label(c, "COUNTERFEITING · WITH CHEMIST TOM SHAW", cx, cy - 150, 24, seg(t, .5, 2.2))
        v = int(100000 * eo(seg(t, d * .42, d * .68)))
        text(c, f"${v:,}", cx, cy + 50, 190, "disp", GOLD, ap(t, d * .4))
        text(c, "in fake bills, every month", cx, cy + 130, 40, "serif", WHITE, ap(t, d * .6))
        stamp(c, "WANTED", cx + 520, cy + 300, 100, seg(t, d * .88, d * .88 + .35), rot=-8)
        c.restore()

def sc_caught(ctx):
    c = ctx.c; W, H, cx, cy, t, d = ctx.W, ctx.H, ctx.cx, ctx.cy, ctx.t, ctx.dur
    k1 = seg(t, d * .26, d * .31); k2 = seg(t, d * .4, d * .46)
    if k1 < 1:
        ctx.layer(1 - k1)
        for i in range(4):
            ph_ = (t * .9 + i * .25) % 1
            c.drawCircle(cx, cy, 80 + ph_ * 420, stroke(GOLD, 5, (1 - ph_) * .6))
        c.drawCircle(cx, cy, 86, fill(GOLD)); c.drawCircle(cx, cy, 62, fill(INK))
        for i in range(10):
            an = i * math.pi / 5 + t * .0; c.drawCircle(cx + math.cos(an) * 40, cy + math.sin(an) * 40, 7, fill(GOLD))
        label(c, "MAY 1935", cx, 130, 30, seg(t, .2, 1.2)); text(c, "An anonymous phone call.", cx, H - 120, 46, "serif", WHITE, ap(t, d * .12))
        c.restore()
    if k1 > 0 and k2 < 1:
        ctx.layer(k1 * (1 - k2)); ny(ctx, .6)
        figure(c, cx, H + 40, 2.1, rim=RED)
        stamp(c, "ARRESTED", cx, cy + 40, 130, seg(t, d * .32, d * .32 + .35), rot=-7)
        label(c, "A NEW YORK STREET", cx, 130, 30, seg(t, d * .29, d * .29 + 1))
        c.restore()
    if k2 > 0:
        ctx.layer(k2); cols, rows, lw, lh = 7, 3, 170, 230; x0 = cx - cols * lw / 2; y0 = cy - rows * lh / 2 + 40
        tr, tc = 1, 4; op = eo(seg(t, d * .62, d * .7))
        for r in range(rows):
            for q in range(cols):
                x = x0 + q * lw; y = y0 + r * lh
                c.drawRect(skia.Rect.MakeXYWH(x + 6, y + 6, lw - 12, lh - 12), fill("#07080b"))
                if (r, q) == (tr, tc):
                    c.drawRect(skia.Rect.MakeXYWH(x + 6, y + 6, lw - 12, lh - 12), fill("#ffd48a", .16 * op))
                    for i in range(5): banknote(c, x + lw / 2, y + lh - 40 - i * 16, 120, rot=(-1) ** i * 4, a=op)
                    c.drawRect(skia.Rect.MakeXYWH(x + 30, y + 40, lw - 60, 50), fill("#6d5a3a", op)); c.drawRect(skia.Rect.MakeXYWH(x + 36, y + 46, lw - 72, 38), stroke("#2a2216", 2, op))
                    dw = (lw - 12) * (1 - op)
                else: dw = lw - 12
                if dw > 2:
                    c.drawRect(skia.Rect.MakeXYWH(x + 6, y + 6, dw, lh - 12), fill("#252a3a")); c.drawRect(skia.Rect.MakeXYWH(x + 6, y + 6, dw, lh - 12), stroke("#3a4158", 3, cap=False))
                    if dw > 60:
                        for i in range(3): c.drawRect(skia.Rect.MakeXYWH(x + 30, y + 30 + i * 14, dw - 50, 5), fill("#12151e"))
                        c.drawCircle(x + dw - 22, y + lh / 2, 8, fill(GOLD if (r, q) == (tr, tc) else "#596080"))
        kx = lerp(-100, x0 + tc * lw + lw - 28, eio(seg(t, d * .46, d * .6))); ky = y0 + tr * lh + lh / 2
        ka = 1 - seg(t, d * .62, d * .66)
        if ka > 0:
            c.drawCircle(kx - 90, ky, 26, stroke(GOLD, 10, ka)); c.drawLine(kx - 64, ky, kx, ky, stroke(GOLD, 10, ka)); c.drawLine(kx - 14, ky, kx - 14, ky + 18, stroke(GOLD, 8, ka)); c.drawLine(kx - 30, ky, kx - 30, ky + 14, stroke(GOLD, 8, ka))
        label(c, "TIMES SQUARE SUBWAY STATION · A LOCKER", cx, 110, 26, seg(t, d * .47, d * .47 + 1.5))
        text(c, "$51,000 in counterfeit bills", cx, H - 110, 46, "serifb", GOLD, ap(t, d * .74))
        text(c, "and the plates used to print them.", cx, H - 50, 38, "serif", WHITE, ap(t, d * .88))
        c.restore()

def sc_escape(ctx):
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy
    t0, _, d0 = ctx.ph(0); t1, _, d1 = ctx.ph(1)
    bx0, bx1 = cx + 60, cx + 860; top = 40; ground = H * .93
    c.drawCircle(cx - 620, 190, 52, fill("#f1e6c8", .9)); c.drawCircle(cx - 620, 190, 170, fill("#f1e6c8", .08, 60))
    c.drawRect(skia.Rect.MakeLTRB(bx0, top, bx1, ground), fill("#1a1c26"))
    for y in range(int(top), int(ground), 26): c.drawLine(bx0, y, bx1, y, stroke("#0f1118", 2, .8, cap=False))
    cols, rows = 5, 6; ww, wh = 84, 112; gx = (bx1 - bx0 - cols * ww) / (cols + 1); gy = 44
    wx = lambda q: bx0 + gx + q * (ww + gx); wy = lambda r: top + 40 + r * (wh + gy)
    for r in range(rows):
        for q in range(cols):
            lit = (r, q) == (1, 2)
            c.drawRect(skia.Rect.MakeXYWH(wx(q), wy(r), ww, wh), fill("#ffcf7a" if lit else "#090a0e", .9 if lit else 1))
            if not lit:
                for i in range(1, 4): c.drawLine(wx(q) + i * ww / 4, wy(r), wx(q) + i * ww / 4, wy(r) + wh, stroke("#2c3040", 3, cap=False))
            c.drawRect(skia.Rect.MakeXYWH(wx(q) - 6, wy(r) + wh, ww + 12, 8), fill("#2a2d3a"))
    c.drawRect(skia.Rect.MakeLTRB(0, ground, W, H), fill("#090a0e"))
    rx = wx(2) + ww / 2; ry0 = wy(1) + wh; rp = eo(seg(t0, d0 * .34, d0 * .58)); ry1 = lerp(ry0, ground - 30, rp)
    if rp > 0:
        c.drawLine(rx, ry0, rx, ry1, stroke(PAPER, 7)); y = ry0 + 40
        while y < ry1: c.drawCircle(rx, y, 8, fill(PAPER)); y += 70
    if t0 > d0 * .62:
        stop_y = lerp(ry0, ground, .46)
        if t1 <= 0: y = lerp(ry0 + 30, stop_y, eio(seg(t0, d0 * .62, d0))); climber(c, rx + 16, y, 2.0, t0)
        elif t1 < d1 * .52: climber(c, rx + 16, stop_y, 2.0, t1, wipe=True)
        elif t1 < d1 * .8: climber(c, rx + 16, lerp(stop_y, ground - 40, eio(seg(t1, d1 * .52, d1 * .8))), 2.0, t1)
        else: climber(c, lerp(rx + 16, -200, seg(t1, d1 * .8, d1 * 1.0) ** 1.2), ground - 50, 2.0, t1, run=True)
    x = 120
    label(c, "1 SEPTEMBER 1935", x, 330, 30, seg(t0, .3, 1.5), align="l")
    text(c, "The day before his trial.", x, 420, 46, "serif", WHITE, ap(t0, d0 * .14), align="l")
    text(c, "Federal detention, Manhattan.", x, 485, 36, "serif", WHITE, ap(t0, d0 * .5) * .8, align="l")
    if t1 > 0:
        text(c, "“Just cleaning the windows.”", x, 640, 50, "serifb", GOLD, ap(t1, d1 * .12) * (1 - seg(t1, d1 * .56, d1 * .6)), align="l")
        text(c, "Then he ran.", x, 640, 64, "disp", WHITE, ap(t1, d1 * .78), align="l")

def sc_end(ctx):
    c = ctx.c; W, H, cx, cy = ctx.W, ctx.H, ctx.cx, ctx.cy
    t, a, d = ctx.ph(0)
    if a > 0:
        ctx.layer(a); k = seg(t, d * .42, d * .5)
        if k < 1:
            c.saveLayerAlpha(None, int(255 * (1 - k))); figure(c, cx, H + 40, 2.1, rim=RED)
            text(c, "He lasted about a month.", cx, 150, 60, "disp", WHITE, ap(t, .1))
            stamp(c, "CAUGHT · PITTSBURGH", cx, cy + 60, 92, seg(t, d * .24, d * .24 + .35), rot=-6); c.restore()
        if k > 0:
            c.saveLayerAlpha(None, int(255 * k)); alcatraz(ctx, t)
            label(c, "ALCATRAZ", cx, 150, 44, seg(t, d * .52, d * .52 + 1.2)); text(c, "Sentence: 20 years", cx, 240, 44, "serif", WHITE, ap(t, d * .62)); c.restore()
        c.restore()
    t, a, d = ctx.ph(1)
    if a > 0:
        ctx.layer(a); w, h = 1100, 600
        c.translate(cx, cy); c.scale(1.25, 1.25); c.translate(-cx, -cy)
        card(c, cx, cy + 10, w, h, rot=1.2)
        text(c, "CERTIFICATE OF DEATH", w / 2, 90, 44, "serifb", INK, spacing=8); c.drawLine(80, 120, w - 80, 120, stroke(INK, 2, cap=False)); c.drawLine(80, 128, w - 80, 128, stroke(INK, 1, cap=False))
        rows = [("NAME", "Victor Lustig", .4, 38), ("DIED", "1947, in federal custody", d * .2, 38), ("OCCUPATION", "Apprentice salesman", d * .86, 58)]
        ks = [.4, d * .2, d * .52]
        for i, (kk, v, ts, sz) in enumerate(rows):
            y = 210 + i * 120
            text(c, kk, 90, y, 20, "sansb", "#7a6a4c", ap(t, ks[i] - .2), align="l", spacing=5)
            c.drawLine(90, y + 62, w - 90, y + 62, stroke("#8a7c62", 1.5, ap(t, ks[i] - .2), cap=False))
            typed(c, v, 90, y + 50, sz, seg(t, ts, ts + 1.0), color="#1d1a14", cursor=True)
        text(c, "AS THE STORY GOES", 90, h - 36, 14, "sansb", "#8c7d60", align="l", spacing=3)
        c.restore(); c.restore()
    t, a, d = ctx.ph(2)
    if a > 0:
        ctx.layer(a); paris(ctx, tower_gold=seg(t, 1, d * .7), tx=.5, lit=.05, sun=seg(t, .5, d * .9))
        text(c, "He never owned it.", cx - 520, 190, 50, "serif", WHITE, ap(t, .4) * (1 - seg(t, d * .7, d * .76)))
        text(c, "STILL STANDING.", cx, 200, 120, "disp", WHITE, ap(t, d * .8, 1.0), spacing=10)
        c.restore()

def sc_outro(ctx):
    c = ctx.c; cx, cy, t = ctx.cx, ctx.cy, ctx.t
    stamp(c, "CASE CLOSED", cx, cy - 110, 150, seg(t, .15, .45), rot=-5)
    label(c, "CASE CLOSED FILES", cx, cy + 110, 30, seg(t, .6, 1.4), GOLD)
    text(c, "New case every week. Subscribe so you don't miss it.", cx, cy + 210, 40, "serif", WHITE, ap(t, 1.1))

# ------------------------------------------------------------------ shorts (vertical)
def s_hook(ctx):
    c = ctx.c; W, H, cx, cy, t, d = ctx.W, ctx.H, ctx.cx, ctx.cy, ctx.t, ctx.dur
    c.drawCircle(cx, cy - 200, 520, fill("#ffd48a", .07, 140))
    tower(c, cx, cy + 480, 1180, color="#0e1017", lattice=GOLD, reveal=eio(seg(t, 0, 1.1)), glow=30)
    label(c, "PARIS · 1925", cx, 250, 40, seg(t, .1, .9))
    stamp(c, "SOLD", cx, cy - 60, 230, seg(t, 2.3, 2.6))
    stamp(c, "NOT HIS TO SELL", cx, cy + 250, 92, seg(t, d * .74, d * .74 + .3), rot=6, color="#e8b23a")

def s_letter(ctx):
    letter(ctx, ctx.t * 2.2, ctx.dur * 1.1, ctx.cx, ctx.cy - 190, h=980)

def s_bribe(ctx):
    c = ctx.c; cx, cy = ctx.cx, ctx.cy; t0, _, d0 = ctx.ph(0); t1, _, d1 = ctx.ph(1)
    c.save(); c.translate(0, -160)
    two(ctx, sp=270, env=seg(t0, d0 * .62, d0 * .95))
    v = .1 + .8 * eo(seg(t0, .2, d0 * .45)) if t1 <= 0 else lerp(.9, .04, eio(seg(t1, .2, d1 * .5)))
    suspicion(ctx, v, cy - 330, 1, w=640)
    stamp(c, "A BRIBE?", cx, cy - 620, 110, seg(t0, d0 * .66, d0 * .66 + .3), rot=-5)
    if t1 > 0: text(c, "CORRUPT = REAL", cx, cy - 190, 76, "disp", GOLD, ap(t1, d1 * .45))
    c.restore()

def s_pay(ctx):
    c = ctx.c; cx, cy, t, d = ctx.cx, ctx.cy, ctx.t, ctx.dur
    k1 = seg(t, d * .12, d * .18); k2 = seg(t, d * .52, d * .58)
    c.save(); c.translate(0, -200)
    if k1 < 1: c.saveLayerAlpha(None, int(255 * (1 - k1))); notes_pile(ctx, seg(t, 0, d * .1), cx, cy + 260, n=14, w=380); c.restore()
    if k1 > 0 and k2 < 1: c.saveLayerAlpha(None, int(255 * k1 * (1 - k2))); route(ctx, seg(t, d * .16, d * .48), "PARIS", "VIENNA", sp=360); c.restore()
    if k2 > 0: poisson_alone(ctx, t - d * .52, k2, txt="TOO EMBARRASSED TO REPORT IT")
    c.restore()

def s_twice(ctx):
    c = ctx.c; cx, cy, t, d = ctx.cx, ctx.cy, ctx.t, ctx.dur
    c.drawCircle(cx, cy - 200, 520, fill("#ffd48a", .07, 140))
    tower(c, cx, cy + 480, 1180, color="#0e1017", lattice=GOLD, glow=30)
    stamp(c, "SOLD", cx - 40, cy - 160, 200, 1, a=.55)
    stamp(c, "SOLD AGAIN?", cx + 20, cy + 150, 120, seg(t, d * .5, d * .5 + .3), rot=7)
    label(c, "FULL CASE ON CASE CLOSED FILES", cx, 250, 30, seg(t, d * .7, d), WHITE)

SCENES = {k[3:] if k.startswith("sc_") else k: v for k, v in list(globals().items()) if k.startswith(("sc_", "s_"))}

# stamp thuds: (scene, line index or -1 for whole scene, offset s, fraction of span)
HITS = [("cold", 3, 3.0, 0), ("cold", 3, 0, .78), ("who", 1, .5, 0), ("idea", 1, 0, .76), ("letter", 0, 0, .8),
        ("pitch", 1, 1.0, 0), ("bribe", 1, .6, 0), ("twice", 0, 0, .86), ("america", 2, 0, .88), ("end", 0, 0, .24),
        ("caught", -1, 0, .32), ("outro", -1, .3, 0)]
SHORT_HITS = [("s_hook", -1, 2.3, 0), ("s_hook", -1, 0, .74), ("s_letter", -1, 0, .4), ("s_bribe", 0, 0, .66), ("s_twice", -1, 0, .5)]
WARM = {"end": lambda t, d, cues: seg(t, cues[2], cues[2] + 4)}

THUMB_WORDS = [("TWICE.", 150), ("NOT HIS.", 120), ("FAKE COUNT", 82)]
def thumbnail(c, W, H, word):
    word, size = word
    sh = skia.GradientShader.MakeRadial(center=(W * .36, H * .55), radius=900, colors=[col("#3a3550"), col("#151827"), col("#07080b")], positions=[0, .5, 1])
    c.drawPaint(skia.Paint(Shader=sh)); c.drawCircle(W * .33, H * .52, 330, fill("#ffb84d", .28, 110))
    tower(c, W * .33, H * 1.0, 700, color="#0b0c12", lattice=GOLD, glow=38, la=.75)
    solid_stamp(c, "SOLD", W * .33, H * .5, 130, rot=-12)
    figure(c, W * .8, H + 30, 1.55, rim=GOLD)
    big_word(c, word, W * .75, H * .30, size, "#ffd36b")
