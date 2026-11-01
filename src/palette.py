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
    "rust": "#96370d",            # halfway between red and orange in lightness, chroma and hue
    "orange": "#b25900",          # darkorange; the darkest orange that keeps 4.5 against the background
    "green": "#4a6b12",           # darkolive
    "blue": "#1e608c",            # darkblue
    "plum": "#6e3278",            # darkplum
    # Text and greys: derived from the background below. The line numbers are tan, a colour of their own.
    "line_number": "#c9a77a",
    # Surfaces: the background is set in BACKGROUND below, and every other surface is a step
    # down from it (SURFACES), so no surface is written as a hex code here.
    # iTerm: the 16 ANSI colours are computed below; only the rest is listed here
    "iterm": {
        "Background Color": "@background",
        "Foreground Color": "@text",
        "Bold Color": "@text",
        "Cursor Color": "@text",
        "Cursor Text Color": "@background",
        "Cursor Guide Color": ("@frame", 0.6),
        "Selection Color": "@selection",
        "Selected Text Color": "@text",
        "Link Color": "@red",
        "Badge Color": ("@rust", 0.5),
    },
}

HOESTKVELD = {
    "type": "dark",
    # The six colours are derived from Høstlys below, the surfaces from BACKGROUND and
    # SURFACES, and the text and greys from the background. Nothing is a hex code here.
    # Høstkveld in iTerm is a little lighter and whiter, since the window is semi-transparent;
    # the colours that are not "@" references are filled in by _surfaces below.
    "iterm": {
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
    "Høstkveld orange": "clip",                   # #ff831e
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


# ---------- The surfaces are a ladder from the background ----------
#
# Both backgrounds lie on one hue, 88°, so the two themes share a neutral axis. Høstlys is
# cream rather than near-white, lightness 0.975 with a faint warmth; Høstkveld is a dark
# brown at 0.236. Every other surface has the background's hue and is a step away from it
# in lightness (down in Høstlys, up in Høstkveld) with its own chroma, from the table
# below. The search highlights take the hue of the greys (halfway between orange and the
# background), so they read as a tint rather than a shade. The whites of the Høstkveld
# terminal are on the background's hue too, like the text.
BACKGROUND = {"Høstlys": (0.975, 0.022, 88.0), "Høstkveld": (0.236, 0.014, 88.0)}  # (L, C, H)
SURFACES = {
    # role: ((distance from the background in lightness, chroma) in Høstlys, the same in Høstkveld)
    "frame": ((0.042, 0.029), (0.040, 0.020)),                  # side bar, tabs, title and status bar
    "widget": ((0.042, 0.029), (0.030, 0.015)),                 # hover, suggestions, find widget in the editor
    "widget_border": ((0.095, 0.037), (0.087, 0.017)),
    "input": ((0.000, 0.022), (0.075, 0.025)),                  # text fields and dropdowns; the background in Høstlys
    "current_line": ((0.029, 0.031), (0.030, 0.015)),
    "selection": ((0.105, 0.044), (0.127, 0.023)),
    "selection_dim": ((0.057, 0.034), (0.087, 0.017)),          # inactive selection, matching words
    "find": ((0.129, 0.065), (0.164, 0.061)),                   # on the grey hue
    "find_dim": ((0.077, 0.048), (0.082, 0.041)),               # on the grey hue
    "bracket_match": ((0.095, 0.066), (0.127, 0.023)),
    "guide": ((0.067, 0.034), (0.087, 0.017)),                  # indent guides, ruler
    "guide_active": ((0.140, 0.041), (0.184, 0.025)),
    "whitespace": ((0.115, 0.040), (0.087, 0.017)),
    "list_active": ((0.105, 0.044), (0.094, 0.027)),
    "list_inactive": ((0.057, 0.034), (0.075, 0.025)),
    "list_hover": ((0.055, 0.035), (0.075, 0.025)),
    "command_center": ((0.065, 0.034), (0.075, 0.025)),
    "command_center_active": ((0.095, 0.037), (0.094, 0.027)),
    # Terminal: Høstlys has a white and a bright white (the background), Høstkveld a black
    "ansi_white": ((0.095, 0.037), None),
    "ansi_bright_white": ((0.000, 0.022), None),
    "ansi_black": (None, (0.087, 0.017)),
    "iterm_black": (None, (0.087, 0.017)),
    "iterm_selection": (None, (0.158, 0.028)),                  # iTerm selection, a little lighter than in VS Code
}
# Høstkveld's whites: the text colour's rule (the background's hue) at their own lightness and chroma
WHITES = {
    "ansi_bright_white": (0.956, 0.025),
    "iterm_white": (0.929, 0.029),
    "iterm_bright_white": (0.986, 0.014),
    "iterm_text": (0.944, 0.025),
}


def _surfaces(p, theme, dark):
    L, C, H = BACKGROUND[theme]
    H_grey = (to_oklch(p["orange"])[2] + H) / 2
    p["background"] = from_oklch(L, C, H)     # editor, panel, terminal
    for role, steps in SURFACES.items():
        step = steps[1] if dark else steps[0]
        if step is None:
            continue
        dL, c = step
        p[role] = from_oklch(L + dL if dark else L - dL, c, H_grey if role.startswith("find") else H)
    if dark:
        for role, (l, c) in WHITES.items():
            p[role] = from_oklch(l, c, H)
        p["iterm"].update({
            "Background Color": p["background"],
            "Foreground Color": p["iterm_text"],
            "Bold Color": p["iterm_bright_white"],
            "Cursor Color": p["iterm_text"],
            "Cursor Text Color": p["background"],
            "Cursor Guide Color": (p["widget"], 0.6),
            "Selection Color": p["iterm_selection"],
            "Selected Text Color": p["iterm_bright_white"],
        })


_surfaces(HOESTLYS, "Høstlys", dark=False)
_surfaces(HOESTKVELD, "Høstkveld", dark=True)


# ---------- The text colour and the greys are derived from the background ----------
#
# No grey is written as a hex code. Each comes from the background and orange, in OKLCH:
#   text    the hue of the background, so the text carries the same faint warmth as the
#           surface it sits on: chroma 0.015 in Høstlys (near-black with a hint of warmth)
#           and 0.030 in Høstkveld (cream)
#   greys   the hue halfway between orange and the background, chroma 0.030: warm and
#           earthy without leaning towards either; the lightness is set per role below
# The scrollbar and the terminal's black (Høstlys) and white (Høstkveld) are the text
# colour; bright black is a grey.
TEXT = {"Høstlys": (0.277, 0.015), "Høstkveld": (0.914, 0.030)}  # (L, C)
GREY_CHROMA = 0.030
GREYS = {
    # role: lightness in (Høstlys, Høstkveld)
    "muted": (0.535, 0.684),        # brackets, descriptions, inactive panel titles
    "comment": (0.600, 0.619),
    "inactive": (0.690, 0.646),     # inactive icons and titles, ignored files
    "tab_inactive": (0.535, 0.701),
    "placeholder": (0.690, 0.566),  # also the line numbers in Høstkveld
}


def _neutrals(p, theme, dark):
    H_bg = to_oklch(p["background"])[2]
    H_grey = (to_oklch(p["orange"])[2] + H_bg) / 2
    L_text, C_text = TEXT[theme]
    text = lambda L: from_oklch(L, C_text, H_bg)
    grey = lambda L: from_oklch(L, GREY_CHROMA, H_grey)
    p["text"] = text(L_text)
    for role, (L_light, L_dark) in GREYS.items():
        p[role] = grey(L_dark if dark else L_light)
    if dark:
        p["line_number"] = p["placeholder"]
        p["scrollbar"] = p["text"]
        p["ansi_white"] = p["text"]
        p["ansi_bright_black"] = p["comment"]
        p["iterm_bright_black"] = grey(0.677)
    else:
        p["scrollbar"] = text(0.344)             # used with transparency
        p["ansi_black"] = p["text"]
        p["ansi_bright_black"] = p["muted"]


_neutrals(HOESTLYS, "Høstlys", dark=False)
_neutrals(HOESTKVELD, "Høstkveld", dark=True)


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
