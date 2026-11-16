"""Art for the ROB RUN guide bot: avatar 640x640, mini-app cover 640x360, icons 180/32.

Run: python -I assets/make_art.py   (from RobRun_Guide/). Pillow only.
Style: night-heist — asphalt, money-green, hazard tape, police red/blue glow.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = Path(__file__).resolve().parent
BG, CASH, ALARM, SIREN, COP, FG = (10, 12, 15), (63, 209, 122), (242, 194, 48), (255, 74, 74), (61, 123, 255), (236, 233, 225)
FONT = None
for f in ("C:/Windows/Fonts/ariblk.ttf", "C:/Windows/Fonts/impact.ttf", "C:/Windows/Fonts/arialbd.ttf"):
    if Path(f).exists():
        FONT = f
        break


def font(px):
    return ImageFont.truetype(FONT, px) if FONT else ImageFont.load_default()


def glow(size, xy, r, color, alpha=150):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = xy
    d.ellipse((x - r, y - r, x + r, y + r), fill=color + (alpha,))
    return layer.filter(ImageFilter.GaussianBlur(r * 0.55))


def tape(img, y, h):
    d = ImageDraw.Draw(img)
    w = img.width
    for x in range(-h * 2, w + h * 2, h * 2):
        d.polygon([(x, y), (x + h, y), (x + h * 2, y + h), (x + h, y + h)], fill=ALARM)
    d.rectangle((0, y, w, y), fill=ALARM)


def mask_icon(d, cx, cy, s):
    """Robber mask: green bandana face with two eye holes."""
    d.rounded_rectangle((cx - s, cy - s * 0.55, cx + s, cy + s * 0.55), radius=s * 0.5, fill=CASH)
    for ex in (cx - s * 0.42, cx + s * 0.42):
        d.ellipse((ex - s * 0.24, cy - s * 0.2, ex + s * 0.24, cy + s * 0.16), fill=BG)
    # bag-strap / dollar
    d.text((cx, cy + s * 0.95), "$", font=font(int(s * 0.9)), fill=ALARM, anchor="mm")


def base(w, h):
    img = Image.new("RGBA", (w, h), BG + (255,))
    img.alpha_composite(glow((w, h), (int(w * 0.12), int(h * 0.1)), int(min(w, h) * 0.45), SIREN, 110))
    img.alpha_composite(glow((w, h), (int(w * 0.88), int(h * 0.1)), int(min(w, h) * 0.45), COP, 120))
    return img


def avatar():
    s = 640
    img = base(s, s)
    d = ImageDraw.Draw(img)
    mask_icon(d, s // 2, int(s * 0.28), 150)
    d.text((s // 2, int(s * 0.76)), "ROB RUN", font=font(78), fill=FG, anchor="mm")
    d.text((s // 2, int(s * 0.90)), "ПОМОЩНИК", font=font(34), fill=CASH, anchor="mm")
    img.convert("RGB").save(OUT / "avatar.png")
    img.convert("RGB").resize((180, 180), Image.LANCZOS).save(OUT / "icon-180.png")
    ic = base(64, 64)
    mask_icon(ImageDraw.Draw(ic), 32, 26, 22)
    ic.convert("RGB").resize((32, 32), Image.LANCZOS).save(OUT / "icon-32.png")


def cover():
    w, h = 640, 360
    img = base(w, h)
    tape(img, h - 26, 26)
    d = ImageDraw.Draw(img)
    mask_icon(d, 130, 150, 95)
    d.text((245, 110), "ROB RUN", font=font(62), fill=FG, anchor="lm")
    d.text((247, 172), "Справочник игрока", font=font(28), fill=CASH, anchor="lm")
    d.text((247, 216), "Гайд · Таймер вайпа", font=font(20), fill=(160, 170, 180), anchor="lm")
    d.text((247, 244), "Калькулятор · Напоминания", font=font(20), fill=(160, 170, 180), anchor="lm")
    img.convert("RGB").save(OUT / "cover.png")


avatar()
cover()
print("art ok")
