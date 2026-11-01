#!/usr/bin/env python3
"""Draws docs/loevfall.png and docs/banner.png from the palette.

    python3 src/banner.py

Needs Pillow (pip install pillow). Run it again after changing a colour in palette.py.

Løvfall (docs/loevfall.png) is the icon's three leaves with three smaller ones in red, blue
and plum, so that all six colours are there. It is the template for the banner, and kept
on its own for anything else that needs it.

The banner (docs/banner.png) is Løvfall twice: Høstkveld on the left as it is, and Høstlys
on the right, mirrored about the seam. Every leaf keeps its hue across the seam except the
two large warm ones, which trade places: the leaf that is orange in Høstkveld is rust in
Høstlys and the other way round, as structure and values do in the themes. A thin edge in the
comment grey, the one colour the two themes share, keeps the shape visible on a white page
as well as on a dark one.

The leaf shape, the placing of the three large leaves and the drawing helpers come from
icon.py, so the icon and the banner can never drift apart.
"""
import math
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from PIL import Image, ImageDraw
from icon import LEAF, LEAVES, RADIUS, SIZE, STALK, VEIN, bezier, stroke
from palette import HOESTKVELD, HOESTLYS

DOCS = Path(__file__).resolve().parent.parent / "docs"
SCALE = 8                     # drawn eight times larger and scaled down, for smooth edges
BANNER_SCALE = 4              # the banner is written at 2048 × 1024, four times the icon size, for Retina screens
EDGE = 1                      # the edge of the banner, in icon pixels: 2 px at 1024 × 512

# The three small leaves, as in the icon list: x, y, rotation in degrees (clockwise), size, colour
SMALL = [
    (176.0, 47.0, 211.0, 0.405, "red"),
    (42.0, 150.0, 70.0, 0.385, "blue"),
    (191.8, 209.0, 316.5, 0.400, "plum"),
]
LOEVFALL = LEAVES + SMALL
TRADE = {"orange": "rust", "rust": "orange"}


def placed(x, y, rotation, size, dx=0):
    """A function that moves a point from leaf coordinates onto the canvas, shifted dx to the right."""
    c, s = math.cos(math.radians(rotation)), math.sin(math.radians(rotation))
    def move(p):
        px, py = p[0] * size, p[1] * size
        return ((dx + x + c * px - s * py) * SCALE, (y + s * px + c * py) * SCALE)
    return move


def leaves(draw, palette, dx=0, mirror=False):
    """Løvfall in one palette. Mirrored, the leaves are flipped about the vertical axis and the
    two large warm colours trade places."""
    background = palette["background"]
    for x, y, rotation, size, name in LOEVFALL:
        if mirror:
            x, rotation, name = SIZE - x, -rotation, TRADE.get(name, name)
        move = placed(x, y, rotation, size, dx)
        colour = palette[name]
        a, b, w = STALK
        stroke(draw, move(a), move(b), w * size * SCALE, colour)
        draw.polygon([move(p) for piece in LEAF for p in bezier(*piece)], fill=colour)
        a, b, w = VEIN
        stroke(draw, move(a), move(b), w * size * SCALE, background)


def rounded(width, height, fill):
    img = Image.new("RGBA", (width * SCALE, height * SCALE), (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle([0, 0, width * SCALE - 1, height * SCALE - 1], radius=RADIUS * SCALE, fill=fill)
    return img


def loevfall():
    img = rounded(SIZE, SIZE, HOESTKVELD["background"])
    leaves(ImageDraw.Draw(img), HOESTKVELD)
    out = DOCS / "loevfall.png"
    img.resize((SIZE, SIZE), Image.LANCZOS).save(out, optimize=True)
    print(f"OK: docs/{out.name}")


def banner():
    width, height = 2 * SIZE, SIZE
    img = rounded(width, height, HOESTLYS["background"])
    # the left half is the same rounded shape in the Høstkveld background, cut at the seam
    left = rounded(width, height, HOESTKVELD["background"]).crop((0, 0, SIZE * SCALE, height * SCALE))
    img.paste(left, (0, 0), left)
    draw = ImageDraw.Draw(img)
    leaves(draw, HOESTKVELD)
    leaves(draw, HOESTLYS, dx=SIZE, mirror=True)
    draw.rounded_rectangle([0, 0, width * SCALE - 1, height * SCALE - 1],
                           radius=RADIUS * SCALE, outline=HOESTKVELD["comment"], width=EDGE * SCALE)
    out = DOCS / "banner.png"
    img.resize((width * BANNER_SCALE, height * BANNER_SCALE), Image.LANCZOS).save(out, optimize=True)
    print(f"OK: docs/{out.name} ({width * BANNER_SCALE} × {height * BANNER_SCALE})")


if __name__ == "__main__":
    loevfall()
    banner()
