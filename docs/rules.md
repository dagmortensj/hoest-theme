# The colour rules

Every colour in Høst has one role, and the role is the same in every language and in both themes. This page is the specification. `src/build.py` follows it, and when a new language or grammar is added, each kind of token gets its colour by asking which role it has, never by what looks good in that one file.

## The principle

Colour is for what the eye looks for. The text colour is for what you read.

Names you read, such as variables, properties and prose, keep the text colour. What marks where something begins, what kind of thing a word is, or what the language provides gets a colour. The more often something occurs, the less a colour on it tells you, so the most frequent tokens stay neutral. This is the same rule the LaTeX colours were built on: `\section` and `\begin` are coloured, while `\frac`, `\label` and `\emph` keep the text colour.

## The colours

### Bold rust: landmarks

Where something begins or changes direction, the things you look for when scrolling.

- Code: definitions (`def`, `class`, `function`, `interface`, `type`, `fn`, `struct`, `enum`, `func`, `fun`) and control flow (`if`, `else`, `for`, `while`, `return`, `break`, `try`, `except`, `throw`, `await`, `yield`, `match`), plus the logical words `and`, `or`, `not`, `in` and `is`. Logical operators written as symbols (`&&`, `||`, `!`, `??`) are operators and keep the text colour.
- LaTeX: `\begin` and `\end`.
- Also bold: constructors (`constructor`, `init`), and `@mixin` and `@function` in SCSS.
- Not bold: `import`, `export`, `from`, `new`, `import type`, preprocessor lines such as `#include`, and CSS at-rules such as `@media`. They are structure, but not landmarks.

### Rust: the grammar of the language

The remaining keywords, the words that hold the code together.

- Code: `const`, `let`, `var`, `val`, `public`, `private`, `static`, `final`, `readonly`, `async`, `import`, `export`, `from`, `as`, `use`, `package`, `namespace`, `new`, `#include`, `lambda`, `=>` and `->`, operators written as words (`typeof`, `instanceof`, `satisfies`, `nameof`), HTML and XML tags, and SQL keywords.
- LaTeX: the preamble (`\documentclass`, `\usepackage`), definitions (`\newcommand`, `\def`), `\item`, TeX conditionals, and the words of a tikz path (`node`, `at`, `circle`).

### Orange: values and input

What comes into the code: literal values, and the parameters that will hold the values a function is given.

- Code: numbers, including prefixes, suffixes and exponents (`0x1F`, `1j`, `6.674e-11`), the language constants `True`, `False`, `None`, `null`, `nil`, enum members, and CSS values and units.
- Parameters in function signatures, in italic (see below).
- LaTeX: numbers and units, and macro parameters `#1` to `#9`, in italic.
- Not orange: upper-case names such as `G`, `M` or `MAKS_STEG`. In physics code they are ordinary variables and keep the text colour.

### Green: tools that do something

What you use to get work done, whether you wrote it or the language provides it.

- Code: function and method names, where they are defined and where they are called, special methods such as `__init__` and `__repr__` where they are defined, built-in functions (`print`, `len`, `range`), built-in types (`int`, `str`, `float`, `list`, `bool`, `number`, `string`, `double`, `f64`), and the classes the language itself provides (`ValueError`, `Error`, `Promise`). In Python a built-in type is a tool of the same kind as `print`: students write `int(input())` and `float(masse)`.
- CSS properties and HTML attributes (`margin`, `color`, `href`, `class`), attributes in JSX and XML (`className`, `key`, `id`), and media features in CSS (`min-width`): the fixed vocabulary of the language.
- LaTeX: environment names (`equation`, `tikzpicture`), the names of new commands (`\newcommand{\dd}`), and drawing commands in tikz (`\draw`, `\node`, `\fill`), which are the calls of a drawing.

### Blue: text and mathematics

Content that is read as text or as a formula.

- Code: strings, including their prefixes (`f"..."`, `r"..."`), template strings, regular expressions, and inline code in Markdown.
- LaTeX: everything in maths mode, verbatim, `\texttt`, file paths, and chemical formulas in `\ce`.

### Plum: what you or a library named, and symbols

Classes and types that someone defined, and characters that stand for something other than themselves.

- Code: keys in JSON, YAML, TOML and INI, classes and types from your own code and from libraries (`Planet`, `Legeme`, `ndarray`, `Optional`), `self`, `cls` and `this` (in italic), decorators, annotations and Rust attributes as one unit (`@property`, `@Override`, `#[derive(Debug)]`), generic type parameters (`T`, in italic), keys in object literals, CSS selectors (`.kurs`, `#prosjektil`, `:hover`, `from` and `to` in keyframes), and special characters inside strings (`\n`, `%d`, `{}` in f-strings, the special characters of a regular expression).
- LaTeX: Greek letters and symbols that stand for a quantity or an operation on one (`\gamma`, `\infty`, `\partial`, `\nabla`, `\sum`, `\int`), and keys in options (`width=`, `scale=`).

### Red: signals and references

What points elsewhere or demands attention. Red is reserved, so it never appears in ordinary code.

- Code: errors and invalid code, links, the `#` before Markdown headings, and removed lines in diffs.
- LaTeX: sectioning commands (`\section`, in bold), `\ref`, `\eqref`, `\cite`, `\url` and `\href`.

### Text colour: what you read

- Code: variables, parameters where they are used, properties and fields (`self.masse`), operators, and the names of modules, namespaces and packages (`numpy`, `namespace Fysikk`, `package main`, `import Foundation`), argument labels in Swift, and the arguments of shell commands (`cat fil.txt`).
- LaTeX: prose, and ordinary commands such as `\frac`, `\sqrt`, `\left`, `\emph`, `\caption` and `\label`. In a formula they are operators, the counterpart of `+` and `*` in code, and so are `=`, `<`, `>`, `|` and the operators, relations and arrows written as commands: `\cdot`, `\times`, `\pm`, `\leq`, `\neq`, `\to`, `\Rightarrow`, `\in`, `\cup`, `\ldots`.

### Grey: what supports the content

- Braces, brackets and parentheses, `$` in LaTeX, the punctuation of JSON and YAML, Markdown markers such as `**` and `` ``` ``, and comments in italic.

## Bold

Bold marks landmarks only: definitions and control flow in code, `\begin`, `\end` and sectioning commands in LaTeX, headings in Markdown, and the subject line of a git commit. Nothing else is bold. A word does not become bold because it is important, only because it marks where something begins or changes direction.

## Italic

Italic marks a placeholder, a name that stands for a value that is only known later. It is the convention of mathematical typesetting, where a variable is set in italic and a fixed function such as sin is set upright.

- Parameters in function signatures, in orange.
- `self`, `cls` and `this`, in plum.
- Generic type parameters such as `T` in `Simulering<T>`, in plum.
- Macro parameters `#1` to `#9` in LaTeX, in orange.
- Comments are italic for a different reason: they are not code.

Built-in types are not italic, even though several themes set them so. They are tools, not placeholders.

## Where the rules meet the grammars

The rules describe roles, but a colour can only follow a role that the grammar marks. Where a grammar does not tell two roles apart, Høst follows the grammar, and the cases are listed here rather than hidden.

- Kotlin: the grammar does not separate built-in types (`Int`, `Double`) from your own, so all types are plum.
- Rust: `impl` and `mod` share their scope with `pub` and `let`, so they cannot be bold.
- Java: `String` and your own classes share a scope, so both are plum.
- Ruby: class names and constants share a scope, so a constant such as `G` is plum as well.
- C++: types from the standard library (`std::string`) are only recognised by the language server, through semantic highlighting.
- TypeScript: the grammar does not tell a built-in class (`Error`, `Promise`) from your own, or a generic parameter `T` from its constraint in `<T extends Legeme>`. The language server does, so these follow the rules once semantic highlighting has loaded.
- Ruby and Lua: `and`, `or` and `not` share their scope with `&&` and `||`, so they keep the text colour.
- Java: `enum` shares its scope with `public` inside the enum, so it cannot be bold.
- C: the names of a `typedef`, `enum` or `union` and the members of an `enum` are not marked by the grammar, so they keep the text colour. The C/C++ extension colours them through semantic highlighting.
- Rust: enum variants (`Some`, `Ok`, your own) share a scope with types, so they are plum.
- Kotlin and Julia: the grammars mark neither parameters nor enum members, and Julia does not tell built-in types from your own, so `Float64` is plum.
- SQL: the grammar does not mark `TRUE`, `FALSE` or numbers with an exponent, so they keep the text colour.
- Python: a method decorated with `@property` is read like a field (`bane.er_tung`), and Pylance marks it as a property, so it keeps the text colour.
- Language servers such as Pylance add semantic tokens on top of the grammar. The semantic colours in `src/build.py` follow the same rules.

## Compared with Dracula and Monokai

Høst agrees with both themes on green function names, green HTML and CSS attribute names, orange italic parameters, and HTML tags in the keyword colour. Like them, it gives built-in types the colour of built-in functions, though Høst uses green for every tool where they use a separate colour for what the language provides.

Høst differs deliberately in three places. Landmarks are bold, which neither theme does. Operators keep the text colour, where both themes give them the keyword colour, which makes code calmer. Numbers and parameters share orange, told apart by italic, where both themes use separate colours.
