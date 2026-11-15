"""Channel art for Case Closed Files: avatar (800x800) and YouTube banner (2560x1440)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "branding")

def bg(c, W, H, cxr=.5, cyr=.5):
    sh = skia.GradientShader.MakeRadial(center=(W * cxr, H * cyr), radius=max(W, H) * .75,
                                        colors=[col("#2b2f45"), col("#141725"), col("#07080b")], positions=[0, .55, 1])
    c.drawPaint(skia.Paint(Shader=sh))

def avatar(S=800):
    s = skia.Surface(S, S); c = s.getCanvas(); bg(c, S, S)
    cx = cy = S / 2
    c.drawCircle(cx, cy, S * .40, stroke(GOLD, S * .022))
    c.drawCircle(cx, cy, S * .355, stroke(GOLD, S * .006, .7))
    # case-file folder
    fw, fh = S * .46, S * .33; fx, fy = cx - fw / 2, cy - fh / 2 + S * .02
    tab = skia.Path(); tab.addRoundRect(skia.Rect.MakeXYWH(fx, fy - S * .05, fw * .4, S * .08), 10, 10); c.drawPath(tab, fill("#c9a96a"))
    c.drawRoundRect(skia.Rect.MakeXYWH(fx, fy, fw, fh), 12, 12, fill("#e3cf9e"))
    c.drawRoundRect(skia.Rect.MakeXYWH(fx, fy, fw, fh), 12, 12, stroke("#8a6a2e", 4))
    # red CLOSED stamp across folder
    c.save(); c.translate(cx, cy + S * .03); c.rotate(-14)
    f = font("sansb", S * .1); t = "CLOSED"; w = f.measureText(t) + S * .06; h = S * .14
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 10, 10, fill("#c0392b"))
    c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + 8, -h / 2 + 8, w - 16, h - 16), 6, 6, stroke("#f6e7c8", 4))
    c.drawString(t, -f.measureText(t) / 2, S * .036, f, fill("#f6e7c8")); c.restore()
    s.makeImageSnapshot().save(f"{OUT}/avatar.png", skia.kPNG)

def banner(W=2560, H=1440):
    s = skia.Surface(W, H); c = s.getCanvas(); bg(c, W, H, .5, .5)
    cx, cy = W / 2, H / 2
    # faint case-wall decor outside the safe zone
    tower(c, cx - 1050, cy + 420, 700, color="#0f111a", lattice="#2c3146", la=.5)
    painting(c, cx + 980, cy - 40, 300, 360, seed=3, a=.55)
    for i, (x, y, r) in enumerate(((cx - 700, cy - 430, -8), (cx + 600, cy + 400, 6))):
        c.saveLayerAlpha(None, 70); card(c, x, y, 420, 260, rot=r)
        text(c, "CASE FILE", 210, 70, 30, "sansb", INK, spacing=8); c.drawLine(40, 95, 380, 95, stroke(INK, 2, cap=False))
        for k in range(5): c.drawRect(skia.Rect.MakeXYWH(40, 125 + k * 22, 300 - (k % 2) * 60, 8), fill("#8a7c62"))
        c.restore(); c.restore()
    stamp(c, "CASE CLOSED", cx + 820, cy - 380, 60, 1, rot=-8, a=.45)
    # safe zone 1546x423 centred
    label(c, "TRUE CONS · HEISTS · FORGERIES", cx, cy - 120, 30, 1, GOLD)
    text(c, "CASE CLOSED FILES", cx, cy + 40, 122, "disp", WHITE, spacing=4)
    text(c, "History's greatest cons, animated and told like thrillers", cx, cy + 115, 42, "serif", "#d9cfb8")
    text(c, "NEW CASE EVERY WEEK", cx, cy + 175, 28, "sansb", GOLD, spacing=6)
    c.drawImage(vignette(W, H), 0, 0)
    s.makeImageSnapshot().save(f"{OUT}/banner.png", skia.kPNG)
    # safe-zone check image (TV/desktop/mobile crops)
    img = s.makeImageSnapshot(); s2 = skia.Surface(W, H); c2 = s2.getCanvas(); c2.drawImage(img, 0, 0)
    c2.drawRect(skia.Rect.MakeXYWH(cx - 773, cy - 211.5, 1546, 423), stroke("#00ff88", 4, cap=False))
    c2.drawRect(skia.Rect.MakeXYWH(cx - 1273, cy - 211.5, 2546, 423), stroke("#ff00aa", 3, cap=False))
    s2.makeImageSnapshot().save(f"{OUT}/banner_safezone_check.png", skia.kPNG)

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True); avatar(); banner(); print("branding ok")
