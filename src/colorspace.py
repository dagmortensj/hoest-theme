"""Conversion between hex and OKLCH, sRGB gamut handling and WCAG contrast.

OKLCH describes a colour by lightness (L, 0 to 1), chroma (C) and hue (H, degrees).
The space is built so that equal numeric steps look roughly equally large, which is
why Høstkveld is derived from Høstlys in it.

Not every OKLCH colour exists in sRGB, the colour space of hex codes. A colour with
high chroma at high lightness, such as a light, saturated orange, needs more than
100 % of a channel. from_oklch never handles this silently: the caller chooses what
happens through `out_of_gamut`.

    "error"   raise OutOfGamut (the default)
    "clip"    cut each channel at 0 and 255. Lightness and chroma drop a little and
              the hue moves a few degrees, in a way that depends on the colour.
    "chroma"  keep lightness and hue and lower the chroma until the colour fits.
              The result is paler than the target.
"""
import math

# A colour counts as inside sRGB if every channel, after gamma encoding, lies within
# half an 8-bit step of 0..255. Colours read from a hex code are then always inside,
# even when rounding gives a channel of -0.0001.
_TOLERANCE = 0.5 / 255


class OutOfGamut(ValueError):
    """The OKLCH colour has no exact counterpart in sRGB."""

    def __init__(self, L, C, H, label=None, hint="Choose out_of_gamut='clip' or 'chroma'."):
        self.L, self.C, self.H, self.label = L, C, H, label
        what = f"{label}: " if label else ""
        super().__init__(
            f"{what}OKLCH ({L:.3f}, {C:.3f}, {H:.1f}) lies outside sRGB. "
            f"The highest chroma at this lightness and hue is {max_chroma(L, H):.3f}. {hint}"
        )


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _encode(c):
    """Linear channel to gamma-encoded sRGB, 0 to 1, without clamping."""
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055


def _srgb(c):
    return max(0, min(255, round(_encode(c) * 255)))


def _rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def to_oklch(h):
    r, g, b = (_lin(x) for x in _rgb(h))
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l, m, s = (x ** (1 / 3) for x in (l, m, s))
    L = 0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s
    A = 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s
    B = 0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s
    return L, math.hypot(A, B), math.degrees(math.atan2(B, A)) % 360


def linear_srgb(L, C, H):
    """OKLCH to linear sRGB. Channels outside 0..1 mean the colour is outside sRGB."""
    A = C * math.cos(math.radians(H))
    B = C * math.sin(math.radians(H))
    l = (L + 0.3963377774 * A + 0.2158037573 * B) ** 3
    m = (L - 0.1055613458 * A - 0.0638541728 * B) ** 3
    s = (L - 0.0894841775 * A - 1.2914855480 * B) ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return r, g, b


def in_gamut(L, C, H):
    """True if the colour exists in sRGB, to within half an 8-bit step."""
    return all(-_TOLERANCE <= _encode(c) <= 1 + _TOLERANCE for c in linear_srgb(L, C, H))


def max_chroma(L, H):
    """The highest chroma sRGB can show at this lightness and hue (0 if none)."""
    if not in_gamut(L, 0.0, H):
        return 0.0
    lo, hi = 0.0, 0.5
    for _ in range(40):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if in_gamut(L, mid, H) else (lo, mid)
    return lo


def from_oklch(L, C, H, out_of_gamut="error", label=None):
    """OKLCH to hex. See the module docstring for `out_of_gamut`."""
    if not in_gamut(L, C, H):
        if out_of_gamut == "chroma" and in_gamut(L, 0.0, H):
            C = max_chroma(L, H)
        elif out_of_gamut != "clip":
            raise OutOfGamut(L, C, H, label)
    return "#%02x%02x%02x" % tuple(_srgb(c) for c in linear_srgb(L, C, H))


def delta_e(h1, h2):
    """Distance between two hex colours in OKLab. About 0.02 is just visible."""
    def lab(h):
        L, C, H = to_oklch(h)
        return L, C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    return math.dist(lab(h1), lab(h2))


def contrast(c1, c2):
    """WCAG contrast between two hex colours (1 to 21)."""
    def lum(h):
        r, g, b = (_lin(x) for x in _rgb(h))
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    a, b = sorted([lum(c1), lum(c2)], reverse=True)
    return (a + 0.05) / (b + 0.05)


def shift_lightness(h, dL, out_of_gamut="error", label=None):
    """The same colour, lighter (dL > 0) or darker (dL < 0)."""
    L, C, H = to_oklch(h)
    return from_oklch(L + dL, C, H, out_of_gamut, label)


def adjust(h, dL=0.0, kC=1.0, out_of_gamut="error", label=None):
    """The same hue with lightness shifted by dL and chroma multiplied by kC."""
    L, C, H = to_oklch(h)
    return from_oklch(L + dL, C * kC, H, out_of_gamut, label)
