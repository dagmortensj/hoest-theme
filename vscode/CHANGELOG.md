# Changelog

## 3.5.1 (2026-10-30)

- A new icon: three leaves in orange, rust and green on the Høstkveld background, drawn from the palette by `src/icon.py`.

## 3.5.0 (2026-10-30)

- The extension is now called `hoest-theme`, matching the repository. VS Code treats it as a new extension, so uninstall the old one first: `code --uninstall-extension dagmorten.host-theme`.
- The status bar button appears only while Høstlys or Høstkveld is active, and works without the `workbench.preferred…ColorTheme` settings. It is also available in the command palette as **Høst: Switch between Høstlys and Høstkveld**.
- An icon for the extension.
- The build script reports every colour that lies outside sRGB and stops if a palette change pushes a new one outside without a decision. No colours changed because of this.

## 3.4.0 (2026-10-29)

- Høstlys and Høstkveld in their own repository, with matching iTerm presets.

## Earlier

Versions up to 3.3 were developed in the author's mac-setup repository: the theme family, rust as the sixth colour, the LaTeX injection grammars and the terminal colours.
