#!/usr/bin/env python3
"""Draws vscode/icon.png, the icon of the extension, from the Høstkveld palette.

    python3 src/icon.py

Needs Pillow (pip install pillow). Run it again after changing a colour in palette.py.

Three leaves on the Høstkveld background, in orange, rust and green. The leaf shape is
that of beech and grey alder. The leaves are placed so that the narrowest gap between
any two of them is about the same, 15 px at 256 px, which keeps them apart also when
the icon is shown at 32 px. Veins and stalks scale with each leaf.
"""
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from PIL import Image, ImageDraw
from palette import HOESTKVELD

SIZE = 256
SCALE = 4                     # drawn four times larger and scaled down, for smooth edges
RADIUS = 56                   # corner radius of the background
OUT = Path(__file__).resolve().parent.parent / "vscode" / "icon.png"

# One leaf in its own coordinates: tip at the top, stalk at the bottom.
# Each piece is a cubic Bézier curve (start, control 1, control 2, end).
LEAF = [
    ((0, -44), (12, -30), (30, 0), (20, 22)),
    ((20, 22), (13, 34), (5, 37), (0, 38)),
    ((0, 38), (-5, 37), (-13, 34), (-20, 22)),
    ((-20, 22), (-30, 0), (-12, -30), (0, -44)),
]
STALK = ((0, 38), (0, 54), 3.5)    # from, to, width
VEIN = ((0, -36), (0, 34), 2.4)

# x, y, rotation in degrees (clockwise), size, palette colour
LEAVES = [
    (95, 95, -30, 1.25, "orange"),
    (170, 126, 24, 1.00, "rust"),
    (106, 183, -60, 0.85, "green"),
]


def bezier(p0, p1, p2, p3, n=48):
    for i in range(n):
        t = i / n
        u = 1 - t
        yield (u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0],
               u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1])


def placed(x, y, rotation, size):
    """A function that moves a point from leaf coordinates onto the canvas."""
    c, s = math.cos(math.radians(rotation)), math.sin(math.radians(rotation))
    def move(p):
        px, py = p[0] * size, p[1] * size
        return ((x + c * px - s * py) * SCALE, (y + s * px + c * py) * SCALE)
    return move


def stroke(draw, a, b, width, fill):
    """A straight line with round ends."""
    draw.line([a, b], fill=fill, width=round(width))
    r = width / 2
    for px, py in (a, b):
        draw.ellipse([px - r, py - r, px + r, py + r], fill=fill)


def main():
    s = SIZE * SCALE
    background = HOESTKVELD["background"]
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([0, 0, s - 1, s - 1], radius=RADIUS * SCALE, fill=background)
    for x, y, rotation, size, name in LEAVES:
        move = placed(x, y, rotation, size)
        colour = HOESTKVELD[name]
        a, b, w = STALK
        stroke(draw, move(a), move(b), w * size * SCALE, colour)
        draw.polygon([move(p) for piece in LEAF for p in bezier(*piece)], fill=colour)
        a, b, w = VEIN
        stroke(draw, move(a), move(b), w * size * SCALE, background)
    img.resize((SIZE, SIZE), Image.LANCZOS).save(OUT, optimize=True)
    print(f"OK: {OUT.relative_to(OUT.parent.parent)}")


if __name__ == "__main__":
    main()
