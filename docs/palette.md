# The Høst palette

How the colours in Høstlys and Høstkveld were chosen, what each one means, and how to change them. Høstlys is six autumn colours on a warm, light background. Høstkveld is derived from Høstlys by a single rule, so the colours keep the same order in both themes, and all but the two warm colours keep the same roles. Contrast is measured against the editor background; WCAG recommends at least 4.5 for normal text and 3 for bold or large text.

![The Høst palette](./palette.svg)

## Changing the colours

Every hex code lives in `src/palette.py` and nowhere else. `src/build.py` generates the two VS Code themes in `vscode/themes/`, the iTerm presets in `iterm/`, `docs/palette.svg` and `docs/roles.svg` from it (and `docs/roles.png` for the Marketplace, when `rsvg-convert` is installed). The workflow:

1. Change a colour in `src/palette.py`, or a rule in `src/build.py`.
2. Run `python3 src/build.py` from the repository root. With `--check` it also prints the contrast of every text colour and the colours that lie outside sRGB. If a change pushes a colour outside sRGB, the build stops and says what to add to `OUT_OF_GAMUT`.
3. Raise `version` in `vscode/package.json`, add a line to `vscode/CHANGELOG.md`, then package and install the extension:

   ```zsh
   cd vscode
   npx @vscode/vsce package -o hoest-theme.vsix
   code --install-extension hoest-theme.vsix --force
   ```

   With a new version number it is easy to see under Extensions that the new package is in place.

Do not edit the files in `vscode/themes/` or `iterm/` by hand, since `build.py` overwrites them. The `test/` folder has one file per language, which is the quickest way to see how a change looks; `test/README.md` describes how to check them.

## What the colours mean

Each colour has one role in every language: a structure colour for the grammar of the language, bold for landmarks; a value colour for values and input; green for tools that do something; blue for text and mathematics; plum for classes, types and symbols; and red for signals and references. The structure colour is the stronger of the two warm colours against the background and the value colour the other, so structure is rust in Høstlys and orange in Høstkveld, and values the opposite. Bold marks landmarks and italic marks placeholders. The full rules, with examples in code and LaTeX and the cases where a grammar sets limits, are in [rules.md](rules.md).

## Høstlys (light)

| Role | Hex | Contrast |
|---|---|---|
| Red | `#781414` | 10.7 |
| Rust | `#99380E` | 7.0 |
| Orange | `#B85C00` | 4.5 |
| Green | `#4A6B12` | 6.0 |
| Blue | `#1E608C` | 6.6 |
| Plum | `#6E3278` | 8.5 |
| Text | `#282828` | 14.3 |
| Brackets | `#7C6F64` | 4.7 |
| Comments | `#928374` | 3.6 |
| Editor | `#FDFCF2` | |
| Frame | `#F4F1E4` | |
| Selection | `#E2D8BF` | |
| Search match | `#E8CCA9` | |

Red, orange, green, blue and plum are the five base colours. Rust sits exactly halfway between red and orange in lightness, chroma and hue, so the step from red through rust to orange is even. The text colour, the greys and the comment colour come from [Gruvbox](https://github.com/morhetz/gruvbox).

Removed lines in diffs have a rust background at low opacity, since red at low opacity turns pink on the light background.

## Høstkveld (dark)

| Role | Hex | Contrast |
|---|---|---|
| Red | `#D54444` | 3.8 |
| Rust | `#F4623A` | 5.3 |
| Orange | `#FF851B` | 6.8 |
| Green | `#7CAC2F` | 6.2 |
| Blue | `#419FDF` | 5.7 |
| Plum | `#BB62C9` | 4.5 |
| Text | `#EBE2CB` | 12.9 |
| Brackets | `#A3978C` | 5.8 |
| Comments | `#928374` | 4.5 |
| Editor | `#211E17` | |
| Frame | `#2D271D` | |
| Selection | `#443D30` | |
| Search match | `#5C4220` | |

The six colours are derived from Høstlys in the OKLCH colour space, where equal numeric steps look roughly equally large:

- **Lightness**: L = 0.281 + 0.837 · L in Høstlys. The colours keep the order and spacing they have in Høstlys, scaled up for a dark background.
- **Chroma**: 1.35 times the chroma in Høstlys, the same for every colour.
- **Hue**: the same as in Høstlys, except that red, rust and orange move 2 to 4 degrees towards red, since light colours otherwise look yellower than dark ones.

Red has the lowest contrast. It is used only for short references, links and errors, where it reads well. The frame is lighter than the editor, and there are no border lines.

### Colours outside sRGB

A hex code can only describe colours in sRGB, the colour space of a standard screen. For orange the rule asks for a colour that sRGB does not contain: OKLCH (0.762, 0.195, 49.8) would need 116 % red. The colour is therefore clipped, which means that each channel is cut at 255. That gives `#FF851B`, OKLCH (0.740, 0.179, 53.5), slightly darker and less saturated than the target, with the hue close to that of orange in Høstlys. This result was chosen by eye. The alternative, keeping lightness and hue and lowering the chroma until the colour fits, gives `#FF904D`, a paler apricot. A Display P3 screen could show the target itself, but VS Code themes and iTerm presets are written in sRGB.

The bright terminal colours and the stronger iTerm colours meet the same limit for orange, rust, bright red and bright blue. Every colour outside sRGB is listed in `OUT_OF_GAMUT` in `src/palette.py` with the choice made for it, either `clip` or `chroma`. If a change to the palette pushes a new colour outside sRGB, the build stops and names it. `python3 src/build.py --check` lists all of them with the target, the result and the distance between them.

## Terminal

A terminal has only eight colour slots (black, red, green, yellow, blue, magenta, cyan and white), plus a bright variant of each. Høst fills them with the palette: yellow is orange, magenta is plum and cyan is rust. All six colours are therefore available in the terminal, and turquoise never appears. Anything that uses the slots follows along when you switch between Høstkveld and Høstlys: the prompt, `ls`, git, fastfetch and command-line highlighting. The bright variants are the same colours, slightly lighter.

The slots hold the hues, not the roles, so the terminal does not take part in the exchange of rust and orange between the themes: the prompt, `ls` and git use the slots by their own conventions, and the prompt is part of the interface rather than of the code. With the shell set up for Høstkveld, the roles match the editor there: orange for keywords and folders, rust for options, green for commands, blue for quoted text, plum for variables and symlinks, and red for errors. The author's own zsh, Powerlevel10k and fastfetch configuration is in [mac-setup](https://github.com/dagmortensj/mac-setup).

### Høstlys (VS Code and iTerm)

Background `#FDFCF2`, text `#282828`, selection `#E2D8BF`.

| Slot | Normal | Bright |
|---|---|---|
| Black | `#282828` | `#7C6F64` |
| Red | `#781414` | `#8F2C28` |
| Green | `#4A6B12` | `#5D802C` |
| Yellow (orange) | `#B85C00` | `#D07128` |
| Blue | `#1E608C` | `#3575A2` |
| Magenta (plum) | `#6E3278` | `#83468D` |
| Cyan (rust) | `#99380E` | `#B04D28` |
| White | `#E2DCC8` | `#FDFCF2` |

### Høstkveld in VS Code

Background `#211E17`, text `#EBE2CB`, selection `#443D30`.

| Slot | Normal | Bright |
|---|---|---|
| Black | `#38332A` | `#928374` |
| Red | `#D54444` | `#EE5C58` |
| Green | `#7CAC2F` | `#91C349` |
| Yellow (orange) | `#FF851B` | `#FF9C3D` |
| Blue | `#419FDF` | `#59B5F7` |
| Magenta (plum) | `#BB62C9` | `#D278E0` |
| Cyan (rust) | `#F4623A` | `#FF7951` |
| White | `#EBE2CB` | `#F7F0DE` |

### Høstkveld in iTerm

Background `#211E17`, text `#F3ECDA`, selection `#4D4535`, bold text `#FFFAF0`.

Høstkveld glows a little more in iTerm than in VS Code: lightness is 0.04 higher and chroma 1.10 times larger. A terminal is used in short sessions, and an iTerm window is often semi-transparent, so the colours can be stronger. Orange, rust and the bright red and blue reach the edge of sRGB here, and are clipped as described under [Colours outside sRGB](#colours-outside-srgb).

| Slot | Normal | Bright |
|---|---|---|
| Black | `#38332A` | `#A39584` |
| Red | `#EB4749` | `#FF605E` |
| Green | `#85BA2A` | `#9AD147` |
| Yellow (orange) | `#FF8C00` | `#FFA334` |
| Blue | `#41ACF4` | `#5AC3FF` |
| Magenta (plum) | `#CC69DC` | `#E47FF4` |
| Cyan (rust) | `#FF6739` | `#FF7E52` |
| White | `#EFE7D2` | `#FFFAF0` |

## What the theme covers

The workbench uses palette colours everywhere, including diff and merge views, peek, debugging, testing, Jupyter notebooks, the command palette, menus, settings and chat. No part falls back on VS Code's own blues and turquoises.

Code is coloured for LaTeX (with LaTeX Workshop), BibTeX, Python, Markdown with maths, JSON, YAML, shell scripts, diffs, git commits and the logs in the Output panel, and by the same rules for TypeScript, JavaScript, Java, C#, C, C++, Go, Rust, Kotlin, Swift, PHP, Ruby, SQL, HTML and CSS. Semantic highlighting is on, so language servers such as Pylance can tell classes, built-in types, parameters and `self` apart even where the grammar cannot.

The LaTeX Workshop grammar recognises a lot, but leaves some common content as plain text. The extension therefore adds four small injection grammars in `vscode/syntaxes/`. They change only the colours, not how the rest of the file is parsed:

- `latex-hoest.injection.json`: definitions and the preamble (`\NewDocumentCommand`, `\DeclareMathOperator`, `\newtheorem`, `\definecolor`, `\usetikzlibrary` and similar get the same role as `\newcommand` and `\usepackage`), numbers and units in siunitx (`\qty`, `\num`, `\unit`), chemistry in mhchem (`\ce`) and file paths (`\includegraphics`, `\addbibresource`, `\graphicspath`).
- `latex-hoest-options.injection.json`: keys and values in options, such as `[width=0.8\linewidth]`, `[label=\alph*)]` and `\hypersetup{colorlinks=true}`, and lengths such as `2mm` and `11pt`.
- `latex-hoest-tikz.injection.json`: the contents of tikzpicture: numbers and units, option keys and the words of a path (`node`, `at`, `cycle`, `circle`, `to`).
- `latex-hoest-tikz-environments.injection.json`: makes `circuitikz` and `tikzcd` coloured like tikz.

In siunitx the number has the value colour and the unit has the text colour, also in maths, where the unit would otherwise be blue like a variable. Chemical formulas are blue like maths, and file paths are blue like strings.
