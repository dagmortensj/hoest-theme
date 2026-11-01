# The Høst palette: the single source of every colour in Høstlys and Høstkveld.
# build.py generates the VS Code themes and the iTerm presets from this file.
# Change a colour here, run `python3 src/build.py`, and everything else follows.
#
# Six colours (see docs/palette.md and docs/rules.md for the roles):
#   red     references and signals: \ref, \cite, links, errors
#   rust    structure in Høstlys, values in Høstkveld
#   orange  values in Høstlys, structure in Høstkveld
#   green   functions and environment names
#   blue    strings and mathematics
#   plum    classes, types, Greek letters and symbols
#
# Structure (keywords, \begin, \end, \section, the preamble) gets the stronger of the two
# warm colours against the background, and values (numbers, constants, parameters) the
# other. Rust is the darker of the two in both themes, so it is the stronger one on the
# light background and the weaker one on the dark background; the two trade places
# between the themes. The roles are set in _roles below.
#
# Høstkveld is derived from Høstlys (see below), so a change to one of the six colours
# in Høstlys carries over to Høstkveld.

from colorspace import OutOfGamut, from_oklch, in_gamut, to_oklch

COLORS = ["red", "rust", "orange", "green", "blue", "plum"]

HOESTLYS = {
    "type": "light",
    # The six colours.
    "red": "#781414",             # darkred
    "rust": "#99380e",            # halfway between red and orange in lightness, chroma and hue
    "orange": "#b85c00",          # darkorange
    "green": "#4a6b12",           # darkolive
    "blue": "#1e608c",            # darkblue
    "plum": "#6e3278",            # darkplum
    # Text and neutral tones
    "text": "#282828",
    "muted": "#7c6f64",           # brackets, descriptions, inactive tabs
    "comment": "#928374",
    "inactive": "#a89984",        # inactive icons and titles, ignored files
    "tab_inactive": "#7c6f64",
    "line_number": "#c9a77a",
    "placeholder": "#a89984",
    # Surfaces
    "background": "#fdfcf2",      # editor, panel, terminal
    "frame": "#f4f1e4",           # side bar, tabs, title and status bar
    "widget": "#f4f1e4",          # hover, suggestions, find widget in the editor
    "widget_border": "#e2dcc8",
    "input": "#fdfcf2",           # text fields and dropdowns
    "current_line": "#f6f2e2",
    "selection": "#e2d8bf",
    "selection_dim": "#efe8d6",   # inactive selection, matching words
    "find": "#e8cca9",
    "find_dim": "#f1dfc6",
    "bracket_match": "#ebdbb2",
    "guide": "#ebe5d3",           # indent guides, ruler
    "guide_active": "#d5cdb6",
    "whitespace": "#ddd5bf",
    "list_active": "#e2d8bf",
    "list_inactive": "#efe8d6",
    "list_hover": "#efe9d6",
    "command_center": "#ebe6d4",
    "command_center_active": "#e2dcc8",
    "scrollbar": "#3c3836",       # used with transparency
    # Terminal: black, white and their bright variants
    "ansi_black": "#282828",
    "ansi_white": "#e2dcc8",
    "ansi_bright_black": "#7c6f64",
    "ansi_bright_white": "#fdfcf2",
    # iTerm: the 16 ANSI colours are computed below; only the rest is listed here
    "iterm": {
        "Background Color": "#fdfcf2",
        "Foreground Color": "#282828",
        "Bold Color": "#282828",
        "Cursor Color": "#282828",
        "Cursor Text Color": "#fdfcf2",
        "Cursor Guide Color": ("#f4f1e4", 0.6),
        "Selection Color": "#e2d8bf",
        "Selected Text Color": "#282828",
        "Link Color": "#781414",
        "Badge Color": ("#99380e", 0.5),
    },
}

HOESTKVELD = {
    "type": "dark",
    # The six colours are derived from Høstlys below.
    "text": "#ebe2cb",
    "muted": "#a3978c",
    "comment": "#928374",
    "inactive": "#998c76",
    "tab_inactive": "#aa9d87",
    "line_number": "#7e7564",
    "placeholder": "#7e7564",
    "background": "#211e17",
    "frame": "#2d271d",
    "widget": "#29251d",
    "widget_border": "#38332a",
    "input": "#363022",
    "current_line": "#29251d",
    "selection": "#443d30",
    "selection_dim": "#38332a",
    "find": "#5c4220",
    "find_dim": "#3f2f1a",
    "bracket_match": "#443d30",
    "guide": "#38332a",
    "guide_active": "#544c3e",
    "whitespace": "#38332a",
    "list_active": "#3d3426",
    "list_inactive": "#363022",
    "list_hover": "#363022",
    "command_center": "#363022",
    "command_center_active": "#3d3426",
    "scrollbar": "#ebe2cb",
    "ansi_black": "#38332a",
    "ansi_white": "#ebe2cb",
    "ansi_bright_black": "#928374",
    "ansi_bright_white": "#f7f0de",
    "iterm_black": "#38332a",
    "iterm_white": "#efe7d2",
    "iterm_bright_black": "#a39584",
    "iterm_bright_white": "#fffaf0",
    # Høstkveld in iTerm is a little lighter and whiter, since the window is semi-transparent
    "iterm": {
        "Background Color": "#211e17",
        "Foreground Color": "#f3ecda",
        "Bold Color": "#fffaf0",
        "Cursor Color": "#f3ecda",
        "Cursor Text Color": "#211e17",
        "Cursor Guide Color": ("#29251d", 0.6),
        "Selection Color": "#4d4535",
        "Selected Text Color": "#fffaf0",
        "Link Color": "@red",
        "Badge Color": ("@rust", 0.5),
    },
}


# ---------- Colours outside sRGB ----------
#
# A hex code can only describe a colour in sRGB. Some of the colours the rules below ask
# for in Høstkveld lie outside it: a light orange or rust with that much chroma would need
# more than 100 % red. Every such colour must be listed here with the choice made for it,
# otherwise build.py stops and names the colour. The choices:
#   "clip"    cut each channel at 255. Lightness and chroma drop a little and the hue
#             moves a few degrees. All the colours below were chosen this way, by eye.
#   "chroma"  keep lightness and hue and lower the chroma until the colour fits (paler).
# `python3 src/build.py --check` lists each one with its target, the result and the
# distance between them.
OUT_OF_GAMUT = {
    "Høstkveld orange": "clip",                   # #ff851b
    "Høstkveld terminal bright orange": "clip",
    "Høstkveld terminal bright rust": "clip",
    "Høstkveld iTerm orange": "clip",
    "Høstkveld iTerm rust": "clip",
    "Høstkveld iTerm bright red": "clip",
    "Høstkveld iTerm bright orange": "clip",
    "Høstkveld iTerm bright rust": "clip",
    "Høstkveld iTerm bright blue": "clip",
    "Høstkveld iTerm Badge Color": "clip",        # rust
}

# Filled while the palette is built: (label, target (L, C, H), choice, hex)
GAMUT_REPORT = []


def color(label, L, C, H):
    """OKLCH to hex. A colour outside sRGB gets the choice listed in OUT_OF_GAMUT."""
    if in_gamut(L, C, H):
        return from_oklch(L, C, H)
    if label not in OUT_OF_GAMUT:
        raise OutOfGamut(L, C, H, label, hint=f'Add "{label}": "clip" or "chroma" to OUT_OF_GAMUT in src/palette.py.')
    result = from_oklch(L, C, H, OUT_OF_GAMUT[label])
    GAMUT_REPORT.append((label, (L, C, H), OUT_OF_GAMUT[label], result))
    return result


def adjusted(label, h, dL=0.0, kC=1.0):
    """The colour h with lightness shifted by dL and chroma multiplied by kC."""
    L, C, H = to_oklch(h)
    return color(label, L + dL, C * kC, H)


# ---------- Høstkveld is derived from Høstlys ----------
#
# The rule, in OKLCH (lightness L, chroma C, hue H):
#   L = 0.281 + 0.837 · L in Høstlys   same order and spacing, scaled to a dark background
#   C = 1.35 · C in Høstlys            every colour glows by the same amount
#   H = H in Høstlys                   the warm colours move slightly towards red, since
#                                      light colours otherwise look yellower than dark ones
LIGHTNESS = (0.281, 0.837)
CHROMA = 1.35
HUE_SHIFT = {"red": -2.3, "rust": -4.0, "orange": -4.0}


def for_dark(name, light):
    L, C, H = to_oklch(light)
    a, b = LIGHTNESS
    return color(f"Høstkveld {name}", a + b * L, CHROMA * C, H + HUE_SHIFT.get(name, 0.0))


for _name in COLORS:
    HOESTKVELD[_name] = for_dark(_name, HOESTLYS[_name])


# ---------- Roles built on the six colours ----------

def _roles(p, theme, dark):
    hover_shift = 0.06 if dark else -0.06  # the button gets lighter in the dark theme and darker in the light one on hover
    # Structure and values: the two warm colours trade places between the themes (see the top
    # of this file). The terminal slots below do not follow: there yellow is always orange and
    # cyan always rust, since the prompt, ls and git use the slots by their own conventions.
    p["structure"], p["value"] = (p["orange"], p["rust"]) if dark else (p["rust"], p["orange"])
    p.update({
        "focus": p["orange"] if dark else p["blue"],
        "button": p["blue"],
        "button_hover": adjusted(f"{theme} button hover", p["blue"], hover_shift),
        "link": p["red"],
        "badge": p["rust"],                                   # count badges, e.g. on the source control icon
        "diff_removed": p["red"] if dark else p["rust"],      # red at low opacity turns pink on a light background
    })
    # Terminal: the eight slots get the palette colours. The cyan slot holds rust, so all
    # six colours exist in the terminal and turquoise never appears. The bright variants
    # are the same colours, a little lighter.
    p["ansi"] = ansi(p, theme, 0.0)
    # iTerm: Høstkveld glows a little more than in VS Code. A terminal is used in short
    # sessions and the window is semi-transparent, so the colours can be lighter and more saturated.
    boost = ITERM_BOOST if dark else (0.0, 1.0)
    p["iterm"]["ansi"] = list(ansi(p, theme, *boost, iterm=True).values())
    for k, v in list(p["iterm"].items()):
        if isinstance(v, str) and v.startswith("@"):
            p["iterm"][k] = adjusted(f"{theme} iTerm {k}", p[v[1:]], *boost)
        elif isinstance(v, tuple) and v[0].startswith("@"):
            p["iterm"][k] = (adjusted(f"{theme} iTerm {k}", p[v[0][1:]], *boost), v[1])


ITERM_BOOST = (0.04, 1.10)  # lightness + 0.04 and chroma × 1.10 for Høstkveld in iTerm


# ANSI order: black, red, green, yellow, blue, magenta, cyan, white, then the bright ones
ANSI_NAMES = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta", "Cyan", "White"]
ANSI_COLORS = [None, "red", "green", "orange", "blue", "plum", "rust", None]


def ansi(p, theme, dL, kC=1.0, iterm=False):
    own = iterm and "iterm_black" in p
    black, white = (p["iterm_black"], p["iterm_white"]) if own else (p["ansi_black"], p["ansi_white"])
    bright_black, bright_white = (p["iterm_bright_black"], p["iterm_bright_white"]) if own else (p["ansi_bright_black"], p["ansi_bright_white"])
    where = f"{theme} iTerm" if iterm else f"{theme} terminal"
    out = {}
    for name, c in zip(ANSI_NAMES, ANSI_COLORS):
        out[name] = black if name == "Black" else white if name == "White" else adjusted(f"{where} {c}", p[c], dL, kC)
    for name, c in zip(ANSI_NAMES, ANSI_COLORS):
        out["Bright" + name] = bright_black if name == "Black" else bright_white if name == "White" else adjusted(f"{where} bright {c}", p[c], dL + 0.07, kC)
    return out


_roles(HOESTLYS, "Høstlys", dark=False)
_roles(HOESTKVELD, "Høstkveld", dark=True)

# A listed colour that is now inside sRGB needs no choice any more, so the list stays honest.
UNUSED_OUT_OF_GAMUT = sorted(set(OUT_OF_GAMUT) - {label for label, *_ in GAMUT_REPORT})
