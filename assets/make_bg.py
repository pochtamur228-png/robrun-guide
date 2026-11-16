"""Backgrounds for the guide from the owner's own gameplay recordings (no official key art).

Run: python -I assets/make_bg.py <bridge_frame.png> <palms_frame.png>
  bridge: 1920x1080 frame at 04:56 of "2026-11-16 01-19-37.mp4" (bridge, sea, skyline)
  palms:  1920x1080 frame at 50:00 of the same file
Writes assets/hero.jpg (header) and assets/bg.jpg (blurred page background). HUD is cropped out.
"""
import sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter

OUT = Path(__file__).resolve().parent
bridge, palms = Image.open(sys.argv[1]).convert("RGB"), Image.open(sys.argv[2]).convert("RGB")

# Header: right half of the bridge shot — skyline, sea, lamp posts; below the compass, right of the car.
hero = bridge.crop((940, 95, 1660, 545)).resize((1008, 630), Image.LANCZOS)   # left of the tilted lamp post
hero = ImageEnhance.Color(hero).enhance(1.15)
hero = ImageEnhance.Contrast(hero).enhance(1.05)
hero.save(OUT / "hero.jpg", quality=80, optimize=True, progressive=True)

# Page background: palms, portrait crop away from the character, heavy blur, darker.
bg = palms.crop((1000, 90, 1640, 1000)).resize((540, 768), Image.LANCZOS)
bg = bg.filter(ImageFilter.GaussianBlur(14))
bg = ImageEnhance.Brightness(bg).enhance(0.55)
bg = ImageEnhance.Color(bg).enhance(1.2)
bg.save(OUT / "bg.jpg", quality=72, optimize=True, progressive=True)
for f in ("hero.jpg", "bg.jpg"):
    print(f, (OUT / f).stat().st_size // 1024, "KB")
