"""Vertical short helpers: long-scene adapter, hook / CTA cards, part header, auto captions.

A short is a list of (scene_id, lines). scene_id is any key of SCENES:
  - a long scene (drawn for 1920x1080) is shown through `vframe` in a full-bleed 9:16 frame,
    panning per SHORT_VIEW[sid] = (x_from, x_to) as fractions of 1920 (default centre).
    lines=None reuses the LONG lines verbatim, so the scene's animation cues still line up.
  - a native vertical scene (s_*, or a hook_card / cta_card made below).
"""
import skia
from engine import (Ctx, seg, eo, eio, back, clamp, text, tw, font, fill, stroke, figure, card, stamp,
                    label, wrap, WHITE, GOLD, RED, PAPER, INK)

BAND_MID = 856    # vertical centre of the long scene in the 1920-tall frame
BAND_S = 0.9      # its scale (window shows 1080 / 0.9 = 1200 px of the 1920 width)


ZOOMS = (0.9, 0.72, 0.6)   # try close first; widen a shot only when the action won't fit


class _TextSpy:
    """Canvas stand-in that forwards everything and records where text lands (scene pixels)."""
    def __init__(s, c, boxes): s._c = c; s._b = boxes
    def __getattr__(s, k): return getattr(s._c, k)
    def drawString(s, txt, x, y, f, paint, *a):
        s._c.drawString(txt, x, y, f, paint, *a)
        if paint.getAlphaf() < .3 or not str(txt).strip(): return
        m = s._c.getTotalMatrix(); w = f.measureText(txt); h = f.getSize()
        pts = [m.mapXY(x, y - h), m.mapXY(x + w, y - h), m.mapXY(x, y + h * .3), m.mapXY(x + w, y + h * .3)]
        s._b.append((min(p.x() for p in pts) * 4, max(p.x() for p in pts) * 4))   # undo the .25 scale


def track(fn, dur, cues):
    """Content-aware framing, one shot per narration line: aim the 9:16 window at what appears
    during that line (plus a little of everything on screen), never slice through text or a stamp,
    and pull wider when the line's action is spread out. Returns (fx(t), zoom(t))."""
    import numpy as np
    S = 480; surf = skia.Surface(S, 270)
    def ink(t, boxes=None):
        c = surf.getCanvas(); c.clear(skia.ColorTRANSPARENT); c.save(); c.scale(.25, .25)
        fn(Ctx(_TextSpy(c, boxes) if boxes is not None else c, 1920, 1080, float(max(0, min(t, dur))), dur, cues)); c.restore()
        px = surf.toarray().astype(np.float64)
        sat = (px[:, :, :3].max(2) - px[:, :, :3].min(2)) / 255
        lum = px[:, :, :3].mean(2) + px[:, :, 3] * .3
        det = np.abs(np.diff(lum, axis=1, prepend=lum[:, :1])) + np.abs(np.diff(lum, axis=0, prepend=lum[:1]))
        return det * (1 + 2 * sat) + px[:, :, 3] * .05   # detail (text, stamps, art) over big flat shapes
    shots = []; prev = .5
    for i, a in enumerate(cues):
        b = cues[i + 1] if i + 1 < len(cues) else dur
        boxes = []; start = ink(a + .05) if i else np.zeros((270, S)); end = ink(b - .25, boxes)
        boxes = [(l / 4, r / 4) for l, r in boxes if r > 0 and l < 1920 and r - l < 1900]
        m = np.clip(end - start, 0, None).sum(0) + .15 * end.sum(0); tot = m.sum()
        if tot <= 0: shots.append((a, prev, ZOOMS[0])); continue
        cs = np.concatenate([[0], np.cumsum(m)]); best = None
        for z in ZOOMS:
            w = min(S, int(S * 1080 / z / 1920)); e = max(8, w // 16)
            j = np.arange(S - w + 1); sums = cs[j + w] - cs[j]
            cut = (cs[j + e] - cs[j]) * (j > 0) + (cs[j + w] - cs[j + w - e]) * (j + w < S)
            score = (sums - 8 * cut) / tot
            for l, r in boxes:   # a line of text sliced by the frame edge is the worst look
                sl = ((j > l) & (j < r)) | ((j + w > l) & (j + w < r))
                score = score - sl * (.5 if r - l < w else .05)
            ok = np.where(score >= score.max() - .03)[0]; centres = (ok + w / 2) / S
            fx = float(centres[np.argmin(abs(centres - prev))]); cap = float(score.max())
            if best is None or cap > best[2] + .12: best = (fx, z, cap)
            if cap >= .78: break
        prev = best[0]; shots.append((a, best[0], best[1]))
    def ease(k):
        def f(t):
            x = shots[0][k]
            for sh in shots[1:]: x = x + (sh[k] - x) * eio(seg(t, sh[0] - .15, sh[0] + .75))
            return x
        return f
    return ease(1), ease(2)


def vframe(fn, view="auto"):
    """Show a 1920x1080 long scene inside a 1080x1920 frame. view: "auto" (track the action),
    (x_from, x_to) for a straight pan, or a float to hold still."""
    st = {}
    def g(ctx):
        c = ctx.c
        if "fx" not in st:
            if view == "auto": st["fx"], st["z"] = track(fn, ctx.dur, ctx.cues)
            else:
                st["z"] = lambda t: BAND_S
                if isinstance(view, tuple): st["fx"] = lambda t, d=ctx.dur: view[0] + (view[1] - view[0]) * eio(t / max(d, .1))
                else: st["fx"] = lambda t: float(view)
        z = st["z"](ctx.t); half = 540 / z / 1920
        fx = min(max(st["fx"](ctx.t), half), 1 - half)
        sub = Ctx(c, 1920, 1080, ctx.t, ctx.dur, ctx.cues)
        c.save(); c.translate(540 - fx * 1920 * z, BAND_MID - 540 * z); c.scale(z, z); fn(sub); c.restore()
    return g


def _fit(s, size, maxw=960):
    while tw(s, "sansb", size) > maxw and size > 40: size -= 4
    return size


def _pop_word(c, s, x, y, size, colr, p):
    if p <= 0: return
    k = .6 + .4 * back(clamp(p))
    c.save(); c.translate(x, y); c.scale(k, k)
    f = font("sansb", size); w = f.measureText(s)
    c.drawString(s, -w / 2 + 6, 8, f, fill("#000000", .9 * clamp(p * 2), 8))
    c.drawString(s, -w / 2, 0, f, stroke("#000000", size * .09, clamp(p * 2)))
    c.drawString(s, -w / 2, 0, f, fill(colr, clamp(p * 2)))
    c.restore()


def hook_card(lines, stamp_text=None, accent=-1, prop=None, rim=RED):
    """Cold-open card: big words pop in line by line, a silhouette, a stamp slam.
    prop(c, cx, cy, t, d) draws an episode-specific object behind the words."""
    def g(ctx):
        c, cx, cy, t, d = ctx.c, ctx.cx, ctx.cy, ctx.t, ctx.dur
        if prop: prop(c, cx, cy, t, d)
        figure(c, cx, cy + 800, 1.35, a=eo(seg(t, 0, .6)), hat=True, rim=rim)
        n = len(lines); gap = 150; y0 = cy - 360 - (n - 1) * gap / 2
        for i, s in enumerate(lines):
            size = _fit(s, 132)
            colr = GOLD if (i == accent or (accent == -1 and i == n - 1)) else WHITE
            _pop_word(c, s, cx, y0 + i * gap, size, colr, seg(t, .1 + i * min(.55, d * .5 / n), .45 + i * min(.55, d * .5 / n)))
        if stamp_text:
            stamp(c, stamp_text, cx, y0 + n * gap + 10, 78, seg(t, d * .62, d * .62 + .3), rot=-6)
    return g


def cta_card(top, big, sub=None):
    """End card: case folder with a stamp. top/big/sub are short strings."""
    def g(ctx):
        c, cx, cy, t, d = ctx.c, ctx.cx, ctx.cy, ctx.t, ctx.dur
        a = eo(seg(t, 0, .4))
        c.save(); c.translate(cx, cy - 160); c.rotate(-3 * (1 - a))
        c.drawRoundRect(skia.Rect.MakeXYWH(-380, -300, 280, 70), 12, 12, fill("#c9a56a", a))
        c.drawRoundRect(skia.Rect.MakeXYWH(-380, -250, 760, 520), 14, 14, fill("#d8b77c", a))
        c.drawRoundRect(skia.Rect.MakeXYWH(-350, -215, 700, 450), 8, 8, fill(PAPER, a))
        text(c, top, 0, -120, 46, "typeb", INK, a)
        c.restore()
        _pop_word(c, big, cx, cy + 10, _fit(big, 110, 640), RED, seg(t, .25, .7))
        if sub: text(c, sub, cx, cy + 300, 44, "sansb", WHITE, eo(seg(t, .6, 1.0)))
    return g


def header(case_no, part, parts, t0, total):
    """Top band drawn over every frame: case number, part, and a progress line."""
    def g(ctx, t):
        c = ctx.c; cx = ctx.cx
        label(c, f"CASE {case_no:03d}  ·  PART {part} OF {parts}" if parts > 1 else f"CASE {case_no:03d}", cx, 238, 34, 1.0)
        p = clamp((t0 + t) / total); w = 560
        c.drawRoundRect(skia.Rect.MakeXYWH(cx - w / 2, 282, w, 8), 4, 4, fill("#ffffff", .14))
        c.drawRoundRect(skia.Rect.MakeXYWH(cx - w / 2, 282, w * p, 8), 4, 4, fill(GOLD, .9))
    return g


SMALL = set("a an the to of and or in on at for is was his her its with by from that as but so be no".split())

def auto_chunks(s, max_words=4, max_chars=24):
    """Split narration into short caption chunks: break at punctuation, never end on a small word."""
    out, cur = [], []
    for w in s.replace("—", " ").split():
        cur.append(w)
        if w[-1] in ".?!:;,":
            out.append(" ".join(cur)); cur = []
        elif len(cur) >= max_words or len(" ".join(cur)) >= max_chars:
            carry = []
            while len(cur) > 1 and cur[-1].lower().strip(".,") in SMALL: carry.insert(0, cur.pop())
            out.append(" ".join(cur)); cur = carry
    if cur: out.append(" ".join(cur))
    merged = []
    for ch in out:   # glue tiny comma fragments ("First,") onto the next chunk
        if merged and merged[-1].endswith(",") and len(merged[-1]) <= 9 and len(merged[-1]) + len(ch) < 27:
            merged[-1] += " " + ch
        else: merged.append(ch)
    return merged


_ONES = "one two three four five six seven eight nine".split()
_TEENS = "ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "twenty thirty forty fifty sixty seventy eighty ninety".split()

def years(s):
    """'nineteen forty-five' -> '1945' for captions."""
    import re
    for ci, cent in ((18, "eighteen"), (19, "nineteen")):
        for ti, tn in enumerate(_TENS):
            for oi, on in enumerate(_ONES):
                s = re.sub(rf"\b{cent} {tn}-{on}\b", f"{ci}{ti + 2}{oi + 1}", s, flags=re.I)
            s = re.sub(rf"\b{cent} {tn}\b", f"{ci}{ti + 2}0", s, flags=re.I)
        for ti, tn in enumerate(_TEENS):
            s = re.sub(rf"\b{cent} {tn}\b", f"{ci}{ti + 10}", s, flags=re.I)
        for oi, on in enumerate(_ONES):
            s = re.sub(rf"\b{cent} oh {on}\b", f"{ci}0{oi + 1}", s, flags=re.I)
    return s
