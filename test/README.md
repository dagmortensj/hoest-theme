# Syntax test files

One file per language, each at most about 60 lines, so that a whole file fits in one screenshot of the editor at a smaller zoom. The first part of each file has the ordinary constructs, and a second part, headed *Vanskelige tilfeller*, the awkward ones. Together they cover the roles in [docs/rules.md](../docs/rules.md): definitions and control flow, other keywords, numbers and constants, parameters in the signature and where they are used, every operator and compound assignment, operators next to literals and inside strings and comments (where they must keep the string or comment colour), operator overloading, functions, built-in and user-defined types, strings in every form the language has (raw, multi-line, interpolated, heredoc), decorators and attributes, keys, labels, comments, and the constructs that are special to each language.

The files are not meant to run. Some refer to names that are not defined, so a language server may underline them.

## How to test

1. Install the latest build and reload the window (**Developer: Reload Window**):

   ```
   code --install-extension vscode/hoest-theme.vsix --force
   ```

2. Open the folder in VS Code and zoom out until the whole file is visible.
3. Open each file in Høstkveld, wait until the language server has started (a few seconds), and take a screenshot. Language servers add semantic highlighting on top of the grammar, so a screenshot taken too early shows only the grammar.
4. Høstkveld alone finds colouring errors, since the rules are the same in both themes. A few files in Høstlys (`python.py`, `typescript.ts`, `index.html`, `latex.tex`) check contrast.
5. Where a colour looks wrong, put the cursor on the word and run **Developer: Inspect Editor Tokens and Scopes**. A screenshot of that panel shows which rule applies.

## Language extensions

Without an extension, VS Code colours a language from its grammar alone. With one, the language server adds semantic tokens. Test the languages you have extensions for as they are; it is how most users of that language will see the theme.

| Files | Extension that adds semantic highlighting |
|---|---|
| `python.py`, `python_klasser.py` | Python (Pylance) |
| `typescript.ts`, `javascript.js`, `react.tsx` | built in |
| `c.c`, `cpp.cpp` | C/C++ |
| `csharp.cs` | C# |
| `java.java` | Language Support for Java |
| `go.go` | Go |
| `rust.rs` | rust-analyzer |
| `kotlin.kt` | Kotlin (needed for any colours at all) |
| `swift.swift`, `julia.jl`, `r.r`, `lua.lua`, `php.php`, `ruby.rb` | optional |

The other files (HTML, CSS, SCSS, JSON, JSONC, YAML, TOML, INI, XML, Markdown, LaTeX, SQL, shell, Dockerfile, Makefile, diff) use the grammar only, apart from LaTeX, which needs LaTeX Workshop. `latex.tex` covers the preamble, maths, lists and tikz; `latex_miljoer.tex` covers figures, tables, theorems, matrices, pgfplots and options spread over several lines.
