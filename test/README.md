# Syntax test files

One file per language, each at most 36 lines, so that a whole file fits in one screenshot of the editor. Together they cover the roles in [docs/rules.md](../docs/rules.md): definitions and control flow, other keywords, numbers and constants, parameters, functions, built-in and user-defined types, strings and their special characters, decorators and attributes, keys, comments, and the constructs that are special to each language.

The files are not meant to run. Some refer to names that are not defined, so a language server may underline them.

## How to test

1. Install the latest build and reload the window (**Developer: Reload Window**):

   ```
   code --install-extension vscode/hoest-theme.vsix --force
   ```

2. Open the folder in VS Code and set the window so that 36 lines are visible.
3. Open each file in Høstkveld, wait until the language server has started (a few seconds), and take a screenshot. Language servers add semantic highlighting on top of the grammar, so a screenshot taken too early shows only the grammar.
4. Repeat a few files in Høstlys (`python.py`, `typescript.ts`, `index.html`, `latex.tex`). The rules are the same, so this checks contrast rather than roles.
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

The other files (HTML, CSS, SCSS, JSON, JSONC, YAML, TOML, INI, XML, Markdown, LaTeX, SQL, shell, Dockerfile, Makefile, diff) use the grammar only, apart from LaTeX, which needs LaTeX Workshop.
