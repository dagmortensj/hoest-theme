# The Høst palette

How the colours in Høstlys and Høstkveld were chosen, what each one means, and how to change them. Høstlys builds on the five colours of a set of LuaLaTeX templates and adds rust. Høstkveld is derived from Høstlys by a single rule, so the colours keep the same order and the same roles in both themes. Contrast is measured against the editor background; WCAG recommends at least 4.5 for normal text and 3 for bold or large text.

![The Høst palette](./palette.svg)

## Changing the colours

Every hex code lives in `src/palette.py` and nowhere else. `src/build.py` generates the two VS Code themes in `vscode/themes/`, the iTerm presets in `iterm/` and `docs/palette.svg` from it. The workflow:

1. Change a colour in `src/palette.py`, or a rule in `src/build.py`.
2. Run `python3 src/build.py` from the repository root. With `--check` it also prints the contrast of every text colour.
3. Raise `version` in `vscode/package.json`, then package and install the extension:

   ```zsh
   cd vscode
   npx @vscode/vsce package -o host-theme.vsix
   code --install-extension host-theme.vsix --force
   ```

   With a new version number it is easy to see under Extensions that the new package is in place.

Do not edit the files in `vscode/themes/` or `iterm/` by hand, since `build.py` overwrites them. The `examples/` folder has one file per language, which is the quickest way to see how a change looks.

## What the colours mean

The templates use red sparingly: for hyperlinks, boxes around key results and separators. Structure is shown with black and bold type, and the palette colours carry the content. The themes follow the same idea. Red marks landmarks and references, rust marks structure, and the other four colours carry content.

- **Red**: landmarks and references. `\section` and the other sectioning commands (bold), `\ref`, `\eqref`, `\cite`, `\url` and `\href` with their keys and addresses, links in Markdown and in the workbench, the `#` before Markdown headings, errors, and removed lines in diffs.
- **Rust**: structure. `\begin` and `\end` (bold), the preamble (`\documentclass`, `\usepackage`, `\usetikzlibrary`, `\definecolor`), definitions (`\newcommand`, `\NewDocumentCommand`, `\newtheorem`, `\def`), `\item`, TeX conditionals such as `\ifdefined` and `\fi`, list markers in Markdown, the entry type in BibTeX (`@book`), keywords in Python, shell scripts and other languages, HTML and XML tags, and the words of a tikz path (`node`, `at`, `cycle`). In the workbench, count badges such as the one on the source control icon.
- **Orange**: numbers and constants such as `True`, `False` and `None`. Upper-case names in Python (`M`, `G`, `LIMIT`) get the text colour like other variables, since single letters such as `M` are ordinary variables in physics code. In the workbench: the active line number, search matches, modified files and warnings.
- **Green**: functions and environments. The environment name in `\begin{equation}` (bold), the names of new commands (`\newcommand{\dd}`), drawing commands in tikz (`\draw`, `\node`, `\addplot`), function names in Python, and added lines in diffs.
- **Blue**: strings and mathematics. Everything inside `$...$`, `\[...\]` and maths environments, verbatim and `\texttt`, Python strings including their `f` or `r` prefix, and inline code in Markdown.
- **Plum**: types and symbols. Greek letters and symbols such as `\gamma`, `\infty` and `\Longrightarrow`, classes and types in Python (`Planet`, `float`), `self` and `cls`, decorators, special characters in f-strings and regular expressions, built-in types in C and similar languages (`int`, `double`), `this` and `super`, HTML attributes, and keys in JSON, YAML, BibTeX and LaTeX options.
- **Grey**: what supports the content: braces, brackets, `$`, comments and quotes.
- **Text colour**: prose, variables, parameters, operators and ordinary LaTeX commands such as `\frac`, `\emph`, `\caption` and `\label`.

## Bold type

Bold is for what you look for when scrolling:

- LaTeX: sectioning commands and their titles, and environments (`\begin`, `\end` and the name).
- Python: control and logical keywords: `def`, `class`, `if`, `elif`, `else`, `for`, `while`, `return`, `break`, `continue`, `pass`, `raise`, `try`, `except`, `finally`, `with`, `yield`, `match`, `case`, `and`, `or`, `not`, `in` and `is`. `import`, `from`, `as`, `lambda` and `async` are not bold.
- Markdown: headings.

## The LuaLaTeX templates

The five colours defined in the style files of the templates:

| Colour | Name in the templates | Hex |
|---|---|---|
| Red | `darkred` | `#781414` |
| Orange | `darkorange` | `#B85C00` |
| Green | `darkolive` | `#4A6B12` |
| Blue | `darkblue` | `#1E608C` |
| Plum | `darkplum` | `#6E3278` |

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

Red, orange, green, blue and plum are the colours of the templates. Rust sits exactly halfway between red and orange in lightness, chroma and hue, so the step from red through rust to orange is even.

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

Red has the lowest contrast. It is used mostly for bold headings and short references, where it reads well. Orange reaches the edge of what a standard screen can show, so in practice its chroma rises only 1.24 times. The frame is lighter than the editor, and there are no border lines.

## Terminal

A terminal has only eight colour slots (black, red, green, yellow, blue, magenta, cyan and white), plus a bright variant of each. Høst fills them with the palette: yellow is orange, magenta is plum and cyan is rust. All six colours are therefore available in the terminal, and turquoise never appears. Anything that uses the slots follows along when you switch between Høstkveld and Høstlys: the prompt, `ls`, git, fastfetch and command-line highlighting. The bright variants are the same colours, slightly lighter.

The roles are the same as in the editor if you set up your shell that way: rust for keywords, orange for folders and options, green for commands, blue for quoted text, plum for variables and symlinks, and red for errors. The author's own zsh, Powerlevel10k and fastfetch configuration is in [mac-setup](https://github.com/dagmortensj/mac-setup).

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

Høstkveld glows a little more in iTerm than in VS Code: lightness is 0.04 higher and chroma 1.10 times larger. A terminal is used in short sessions, and an iTerm window is often semi-transparent, so the colours can be stronger. Orange is already as saturated as a standard screen can show.

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

Code is coloured for LaTeX (with LaTeX Workshop), BibTeX, Python, Markdown with maths, JSON, YAML, shell scripts, diffs, git commits and the logs in the Output panel. Semantic highlighting is on for Python, so Pylance can tell classes, functions, constants and `self` apart even where the grammar cannot.

The LaTeX Workshop grammar recognises a lot, but leaves some common content as plain text. The extension therefore adds four small injection grammars in `vscode/syntaxes/`. They change only the colours, not how the rest of the file is parsed:

- `latex-host.injection.json`: definitions and the preamble (`\NewDocumentCommand`, `\DeclareMathOperator`, `\newtheorem`, `\definecolor`, `\usetikzlibrary` and similar get the same role as `\newcommand` and `\usepackage`), numbers and units in siunitx (`\qty`, `\num`, `\unit`), chemistry in mhchem (`\ce`) and file paths (`\includegraphics`, `\addbibresource`, `\graphicspath`).
- `latex-host-options.injection.json`: keys and values in options, such as `[width=0.8\linewidth]`, `[label=\alph*)]` and `\hypersetup{colorlinks=true}`, and lengths such as `2mm` and `11pt`.
- `latex-host-tikz.injection.json`: the contents of tikzpicture: numbers and units, option keys and the words of a path (`node`, `at`, `cycle`, `circle`, `to`).
- `latex-host-tikz-environments.injection.json`: makes `circuitikz` and `tikzcd` coloured like tikz.

In siunitx the number is orange and the unit has the text colour, also in maths, where the unit would otherwise be blue like a variable. Chemical formulas are blue like maths, and file paths are blue like strings.
