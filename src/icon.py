#!/usr/bin/env python3
"""Draws vscode/icon.png, the icon of the extension, from the Høstkveld palette.

    python3 src/icon.py

Needs Pillow (pip install pillow). Run it again after changing a colour in palette.py.
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from PIL import Image, ImageDraw
from palette import COLORS, HOESTKVELD

SIZE = 256
SCALE = 4                     # drawn four times larger and scaled down, for smooth edges
OUT = Path(__file__).resolve().parent.parent / "vscode" / "icon.png"


def main():
    s = SIZE * SCALE
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, s - 1, s - 1], radius=48 * SCALE, fill=HOESTKVELD["background"])
    # Six quarter circles around the lower left corner, red outermost and plum innermost
    cx, cy = 44 * SCALE, 212 * SCALE
    band, gap = 22 * SCALE, 6 * SCALE
    outer = 6 * band + 5 * gap
    for i, name in enumerate(COLORS):
        r = outer - i * (band + gap)
        d.pieslice([cx - r, cy - r, cx + r, cy + r], 270, 360, fill=HOESTKVELD[name])
        inner = r - band
        d.pieslice([cx - inner, cy - inner, cx + inner, cy + inner], 270, 360, fill=HOESTKVELD["background"])
    img.resize((SIZE, SIZE), Image.LANCZOS).save(OUT, optimize=True)
    print(f"OK: {OUT.relative_to(OUT.parent.parent)}")


if __name__ == "__main__":
    main()
