# Høst

<!-- First paragraph: written by Dag-Morten in his own words. Replace the placeholder below before publishing. -->
*[Placeholder for the first paragraph, in my own words: why I made Høst, and what it is for.]*

**Høstlys** (autumn light) is a light theme and **Høstkveld** (autumn evening) a dark one, both in earth tones. *Høst* is Norwegian for autumn. The palette is six deep autumn colours on warm, slightly rustic earth tones.

![Høstkveld](https://raw.githubusercontent.com/dagmortensj/hoest-theme/main/docs/screenshots/hoestkveld.png)

![Høstlys](https://raw.githubusercontent.com/dagmortensj/hoest-theme/main/docs/screenshots/hoestlys.png)

## Six colours, one role each

Each colour has the same role in every language and in both themes:

![The roles of the six colours](https://raw.githubusercontent.com/dagmortensj/hoest-theme/main/docs/roles.png)

| Colour | Role | Examples |
|---|---|---|
| Rust | Structure and keywords, landmarks in bold | `def`, `class`, `if`, `return` in bold, `import`, `const`, `\begin`, the preamble |
| Orange | Values and input | `3.14`, `True`, `None`, parameters in italic |
| Green | Tools that do something | function names, `print`, built-in types such as `int` and `str`, CSS properties, `equation`, `\draw` |
| Blue | Text and mathematics | `"text"`, everything inside `$...$` |
| Plum | Classes and types, and symbols | your classes and those of libraries, `self` in italic, `@property`, keys in JSON and YAML, `\n`, `\gamma` |
| Red | Signals and references | `\section`, `\ref`, `\cite`, links, errors |

Comments, braces and brackets are grey, and variables, operators and prose keep the text colour. Bold marks landmarks such as definitions and control flow, and italic marks placeholders such as parameters and `self`. Høstkveld is derived from Høstlys by a single rule in the OKLCH colour space, so the colours keep their order and roles in both themes.

## What it covers

- The whole workbench, including diff and merge views, debugging, testing, notebooks, the command palette, settings and chat.
- LaTeX with [LaTeX Workshop](https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop), plus four small injection grammars for what LaTeX Workshop leaves as plain text: tikz, circuitikz and tikzcd, option keys, siunitx, mhchem and file paths.
- Python, with semantic highlighting for Pylance.
- The same roles in TypeScript, JavaScript, Java, C#, C, C++, Go, Rust, Kotlin, Swift, PHP, Ruby, SQL, HTML and CSS.
- Markdown with maths, BibTeX, JSON, YAML, TOML, shell, diff, git commits and logs.

## Switching between light and dark

While Høstlys or Høstkveld is active, a button at the right of the status bar switches between them. The same command is in the command palette as **Høst: Switch between Høstlys and Høstkveld**. If you also want VS Code's own light/dark switching, for example when it follows the system appearance, set the pair in your settings:

```jsonc
"workbench.preferredLightColorTheme": "Høstlys",
"workbench.preferredDarkColorTheme": "Høstkveld",
```

## More

Matching iTerm presets, the full palette with contrast values, and the build script that generates the themes are at [github.com/dagmortensj/hoest-theme](https://github.com/dagmortensj/hoest-theme).

## Credits

Høst is designed by Dag-Morten and made with [Claude](https://claude.ai). Apart from the first paragraph of this page, the documentation is written with Claude. The neutral tones come from [Gruvbox](https://github.com/morhetz/gruvbox) by Pavel Pertsev.
