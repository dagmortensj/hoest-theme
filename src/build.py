#!/usr/bin/env python3
"""Builds Høstlys and Høstkveld from palette.py.

    python3 src/build.py           writes vscode/themes/*.json, iterm/*.itermcolors and docs/palette.svg
    python3 src/build.py --check   also prints the contrast of the text colours

Afterwards, raise the version in vscode/package.json and package the extension:
    cd vscode && npx @vscode/vsce package -o host-theme.vsix

Colours in the workbench and in the code are named by their role in the palette
("red", "selection" and so on), never by hex code. The hex codes live only in palette.py.
"""
import json
import plistlib
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ in the repo
from colorspace import contrast
from palette import COLORS, HOSTKVELD, HOSTLYS

ROOT = Path(__file__).resolve().parent.parent
THEMES = ROOT / "vscode" / "themes"
ITERM = ROOT / "iterm"
DOCS = ROOT / "docs"


# ---------- small helpers ----------

def a(color, alpha):
    """The colour with transparency, alpha between 0 and 1."""
    return (color, alpha)


NONE = "#00000000"  # fully transparent: no border


def pick(p, dark, light):
    """Pick a different palette colour for Høstkveld and Høstlys."""
    return dark if p["type"] == "dark" else light


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def resolve(p, value):
    """Turn a palette name, (name, alpha) or a hex code into a hex string."""
    if isinstance(value, tuple):
        color, alpha = value
        return resolve(p, color)[:7] + format(round(alpha * 255), "02x")
    if value.startswith("#"):
        return value.lower()
    return p[value].lower()


# ---------- the workbench ----------

def ui(p):
    """All workbench colours. Key -> palette name."""
    return {
        # Base colours the rest of VS Code builds on
        "foreground": "text",
        "focusBorder": "focus",
        "widget.border": NONE,
        "descriptionForeground": "muted",

        # The editor
        "editor.background": "background",
        "editor.foreground": "text",
        "editorCursor.foreground": "text",
        "editor.selectionBackground": "selection",
        "editor.inactiveSelectionBackground": "selection_dim",
        "editor.selectionHighlightBackground": "selection_dim",
        "editor.wordHighlightBackground": "selection_dim",
        "editor.wordHighlightStrongBackground": "selection_dim",
        "editor.findMatchBackground": "find",
        "editor.findMatchBorder": "orange",
        "editor.findMatchHighlightBackground": "find_dim",
        "editor.findRangeHighlightBackground": "current_line",
        "editor.lineHighlightBackground": "current_line",
        "editor.lineHighlightBorder": NONE,
        "editorLineNumber.foreground": "line_number",
        "editorLineNumber.activeForeground": "orange",
        "editorIndentGuide.background1": "guide",
        "editorIndentGuide.activeBackground1": "guide_active",
        "editorWhitespace.foreground": "whitespace",
        "editorRuler.foreground": "guide",
        "editorBracketMatch.background": "bracket_match",
        "editorBracketMatch.border": NONE,
        **{f"editorBracketHighlight.foreground{i}": "muted" for i in range(1, 7)},
        "editorBracketHighlight.unexpectedBracket.foreground": "red",
        "editorGutter.background": "background",
        "editorGroupHeader.tabsBackground": "frame",
        "editorGroup.border": NONE,
        "editorWidget.background": "widget",
        "editorWidget.border": "widget_border",
        "editorHoverWidget.background": "widget",
        "editorHoverWidget.border": "widget_border",
        "editorSuggestWidget.background": "widget",
        "editorSuggestWidget.border": "widget_border",
        "editorSuggestWidget.selectedBackground": "selection",
        "editorError.foreground": "red",
        "editorWarning.foreground": "orange",
        "editorInfo.foreground": "blue",
        "editorOverviewRuler.border": NONE,

        # Tabs
        "tab.activeBackground": "background",
        "tab.activeForeground": "text",
        "tab.inactiveBackground": "frame",
        "tab.inactiveForeground": "tab_inactive",
        "tab.border": NONE,
        "tab.activeBorderTop": NONE,

        # Side bar, activity bar, title and status bar
        "sideBar.background": "frame",
        "sideBar.foreground": "text",
        "sideBar.border": NONE,
        "sideBarSectionHeader.background": "frame",
        "sideBarTitle.foreground": "text",
        "activityBar.background": "frame",
        "activityBar.foreground": "text",
        "activityBar.inactiveForeground": "inactive",
        "activityBar.border": NONE,
        "activityBarBadge.background": "badge",
        "activityBarBadge.foreground": "background",
        "badge.background": "badge",
        "badge.foreground": "background",
        "titleBar.activeBackground": "frame",
        "titleBar.activeForeground": "text",
        "titleBar.inactiveBackground": "frame",
        "titleBar.inactiveForeground": "inactive",
        "titleBar.border": NONE,
        "statusBar.background": "frame",
        "statusBar.foreground": "text",
        "statusBar.border": NONE,
        "statusBar.noFolderBackground": "frame",
        "statusBar.debuggingBackground": "orange",
        "statusBar.debuggingForeground": "background",

        # The panel (terminal, problems)
        "panel.background": "background",
        "panel.border": NONE,
        "panelTitle.activeForeground": "text",
        "panelTitle.activeBorder": "orange",
        "panelTitle.inactiveForeground": "muted",

        # Lists and trees
        "list.activeSelectionBackground": "list_active",
        "list.activeSelectionForeground": "text",
        "list.inactiveSelectionBackground": "list_inactive",
        "list.hoverBackground": "list_hover",
        "list.focusOutline": "guide_active",
        "list.highlightForeground": "orange",

        # Text fields, buttons, scrollbars
        "input.background": "input",
        "input.border": "widget_border",
        "input.foreground": "text",
        "input.placeholderForeground": "placeholder",
        "dropdown.background": "input",
        "dropdown.border": "widget_border",
        "button.background": "button",
        "button.foreground": "background",
        "button.hoverBackground": "button_hover",
        "scrollbarSlider.background": a("scrollbar", 0x22 / 255),
        "scrollbarSlider.hoverBackground": a("scrollbar", 0x33 / 255),
        "scrollbarSlider.activeBackground": a("scrollbar", 0x44 / 255),
        "textLink.foreground": "link",
        "textLink.activeForeground": "link",

        # Git in the explorer
        "gitDecoration.modifiedResourceForeground": "orange",
        "gitDecoration.untrackedResourceForeground": "green",
        "gitDecoration.addedResourceForeground": "green",
        "gitDecoration.deletedResourceForeground": "red",
        "gitDecoration.ignoredResourceForeground": "inactive",

        # The terminal
        "terminal.background": "background",
        "terminal.foreground": "text",
        "terminalCursor.foreground": "text",
        "terminal.selectionBackground": "selection",
        **{f"terminal.ansi{n}": v for n, v in p["ansi"].items()},

        # No borders
        "editorGroupHeader.tabsBorder": NONE,
        "editorGroupHeader.border": NONE,
        "sideBarSectionHeader.border": NONE,
        "tab.activeBorder": NONE,
        "commandCenter.border": NONE,
        "commandCenter.inactiveBorder": NONE,
        "commandCenter.background": "command_center",
        "commandCenter.activeBackground": "command_center_active",
        **ui_extended(p),
    }


def ui_extended(p):
    """The rest of the workbench: everything that would otherwise get VS Code's own colours.

    Checked against every colour key VS Code registers, so that nothing falls back
    on VS Code's default blues, turquoises and cool greys.
    """
    shadow = pick(p, a("#000000", 0.45), a("#3c3836", 0.16))
    hover = a("text", pick(p, 0.10, 0.07))
    active = a("text", pick(p, 0.16, 0.11))
    drop = a("orange", 0.16)  # when something is dragged over an area
    added, removed = "green", "red"
    u = {}

    # ----- Base colours and text -----
    u.update({
        "icon.foreground": a("text", 0.85),
        "disabledForeground": "inactive",
        "errorForeground": "red",
        "strongForeground": "text",
        "selection.background": "selection",
        "textBlockQuote.background": "widget",
        "textBlockQuote.border": "muted",
        "textCodeBlock.background": "widget",
        "textPreformat.foreground": "blue",
        "textPreformat.background": "selection_dim",
        "textSeparator.foreground": "widget_border",
        "sash.hoverBorder": "orange",
        "toolbar.hoverBackground": hover,
        "toolbar.activeBackground": active,
        "widget.shadow": shadow,
        "scrollbar.shadow": shadow,
        "editorStickyScroll.shadow": shadow,
        "sideBarStickyScroll.shadow": shadow,
        "panelStickyScroll.shadow": shadow,
        "listFilterWidget.shadow": shadow,
        "inlineChat.shadow": shadow,
        "diffEditor.unchangedRegionShadow": shadow,
    })

    # ----- Activity bar (at the top), badges and profiles -----
    u.update({
        "activityBar.activeBorder": "orange",
        "activityBar.dropBorder": "orange",
        "activityBarTop.foreground": "text",
        "activityBarTop.inactiveForeground": "inactive",
        "activityBarTop.activeBorder": "orange",
        "activityBarTop.dropBorder": "orange",
        "activityErrorBadge.background": "red",
        "activityErrorBadge.foreground": "background",
        "activityWarningBadge.background": "orange",
        "activityWarningBadge.foreground": "background",
        "profileBadge.background": "muted",
        "profileBadge.foreground": "background",
    })

    # ----- Status bar -----
    u.update({
        "statusBarItem.hoverBackground": hover,
        "statusBarItem.compactHoverBackground": hover,
        "statusBarItem.activeBackground": active,
        "statusBarItem.prominentBackground": active,
        "statusBarItem.prominentHoverBackground": hover,
        "statusBarItem.errorBackground": "red",
        "statusBarItem.errorForeground": "background",
        "statusBarItem.errorHoverBackground": hover,
        "statusBarItem.warningBackground": "orange",
        "statusBarItem.warningForeground": "background",
        "statusBarItem.warningHoverBackground": hover,
        "statusBarItem.offlineBackground": "red",
        "statusBarItem.offlineForeground": "background",
        "statusBarItem.offlineHoverBackground": hover,
        "statusBarItem.remoteBackground": "frame",
        "statusBarItem.remoteForeground": "orange",
        "statusBarItem.remoteHoverBackground": hover,
        "statusBar.debuggingBorder": NONE,
        "statusBar.focusBorder": "orange",
        "statusBarItem.focusBorder": "orange",
    })

    # ----- Tabs -----
    u.update({
        "tab.hoverBackground": "list_hover",
        "tab.unfocusedHoverBackground": "list_hover",
        "tab.activeModifiedBorder": "orange",
        "tab.inactiveModifiedBorder": a("orange", 0.5),
        "tab.unfocusedActiveModifiedBorder": a("orange", 0.5),
        "tab.unfocusedInactiveModifiedBorder": a("orange", 0.25),
        "tab.lastPinnedBorder": "widget_border",
        "tab.dragAndDropBorder": "orange",
    })

    # ----- Editor -----
    u.update({
        "editorActiveLineNumber.foreground": "orange",
        "editor.hoverHighlightBackground": "selection_dim",
        "editor.rangeHighlightBackground": a("orange", 0.10),
        "editor.foldPlaceholderForeground": "muted",
        "editor.linkedEditingBackground": a("red", 0.15),
        "editor.snippetTabstopHighlightBackground": "selection_dim",
        "editor.snippetFinalTabstopHighlightBorder": "muted",
        "editor.inlineValuesBackground": a("orange", 0.15),
        "editor.inlineValuesForeground": "muted",
        "editor.stackFrameHighlightBackground": a("orange", 0.15),
        "editor.focusedStackFrameHighlightBackground": a("green", 0.15),
        "editor.compositionBorder": "text",
        "editor.placeholder.foreground": "placeholder",
        "editorCodeLens.foreground": "muted",
        "editorGhostText.foreground": "comment",
        "editorHint.foreground": "muted",
        "editorInlayHint.foreground": "muted",
        "editorInlayHint.background": a("muted", 0.12),
        "editorInlayHint.typeForeground": "muted",
        "editorInlayHint.parameterForeground": "muted",
        "editorLightBulb.foreground": "orange",
        "editorLightBulbAi.foreground": "orange",
        "editorLightBulbAutoFix.foreground": "green",
        "editorLink.activeForeground": "link",
        "editorStickyScrollHover.background": "list_hover",
        "editorGutter.foldingControlForeground": "muted",
        "editorGutter.addedBackground": added,
        "editorGutter.addedSecondaryBackground": a(added, 0.5),
        "editorGutter.modifiedBackground": "orange",
        "editorGutter.modifiedSecondaryBackground": a("orange", 0.5),
        "editorGutter.deletedBackground": removed,
        "editorGutter.deletedSecondaryBackground": a(removed, 0.5),
        "editorCommentsWidget.replyInputBackground": "input",
        "editorCommentsWidget.resolvedBorder": "muted",
        "editorCommentsWidget.unresolvedBorder": "orange",
        "editorCommentsWidget.rangeActiveBackground": a("orange", 0.12),
        "editorCommentsWidget.rangeBackground": a("orange", 0.06),
        "commentsView.resolvedIcon": "muted",
        "commentsView.unresolvedIcon": "orange",
        "editorUnicodeHighlight.border": "orange",
        "editorMarkerNavigation.background": "widget",
        "editorMarkerNavigationError.background": "red",
        "editorMarkerNavigationWarning.background": "orange",
        "editorMarkerNavigationInfo.background": "blue",
    })

    # ----- Overview ruler and minimap -----
    u.update({
        "editorOverviewRuler.addedForeground": a(added, 0.6),
        "editorOverviewRuler.modifiedForeground": a("orange", 0.6),
        "editorOverviewRuler.deletedForeground": a(removed, 0.6),
        "editorOverviewRuler.errorForeground": a("red", 0.8),
        "editorOverviewRuler.warningForeground": a("orange", 0.8),
        "editorOverviewRuler.infoForeground": a("blue", 0.8),
        "editorOverviewRuler.findMatchForeground": a("orange", 0.5),
        "editorOverviewRuler.rangeHighlightForeground": a("orange", 0.4),
        "editorOverviewRuler.selectionHighlightForeground": a("muted", 0.6),
        "editorOverviewRuler.wordHighlightForeground": a("muted", 0.6),
        "editorOverviewRuler.wordHighlightStrongForeground": a("muted", 0.8),
        "editorOverviewRuler.wordHighlightTextForeground": a("muted", 0.6),
        "editorOverviewRuler.bracketMatchForeground": "muted",
        "editorOverviewRuler.currentContentForeground": a("green", 0.5),
        "editorOverviewRuler.incomingContentForeground": a("plum", 0.5),
        "editorOverviewRuler.commonContentForeground": a("muted", 0.4),
        "editorOverviewRuler.inlineChatInserted": a(added, 0.12),
        "editorOverviewRuler.inlineChatRemoved": a(removed, 0.12),
        "editorMinimap.inlineChatInserted": a(added, 0.12),
        "minimap.errorHighlight": a("red", 0.7),
        "minimap.warningHighlight": a("orange", 0.7),
        "minimap.findMatchHighlight": a("orange", 0.6),
        "minimap.selectionHighlight": "selection",
        "minimapGutter.addedBackground": added,
        "minimapGutter.modifiedBackground": "orange",
        "minimapGutter.deletedBackground": removed,
    })

    # ----- Diff and inline suggestions (green = added, red = removed) -----
    u.update({
        "diffEditor.insertedTextBackground": a(added, 0.22),
        "diffEditor.insertedLineBackground": a(added, 0.12),
        "diffEditor.removedTextBackground": a("diff_removed", 0.22),
        "diffEditor.removedLineBackground": a("diff_removed", 0.12),
        "diffEditorGutter.insertedLineBackground": a(added, 0.25),
        "diffEditorGutter.removedLineBackground": a("diff_removed", 0.3),
        "diffEditorOverview.insertedForeground": a(added, 0.6),
        "diffEditorOverview.removedForeground": a(removed, 0.6),
        "diffEditor.diagonalFill": a("muted", 0.2),
        "diffEditor.unchangedCodeBackground": a("muted", 0.08),
        "diffEditor.unchangedRegionBackground": "frame",
        "diffEditor.unchangedRegionForeground": "muted",
        "diffEditor.move.border": a("muted", 0.6),
        "diffEditor.moveActive.border": "orange",
        "diffEditor.border": NONE,
        "multiDiffEditor.headerBackground": "frame",
        "multiDiffEditor.background": "background",
        "multiDiffEditor.border": NONE,
        "inlineChatDiff.inserted": a(added, 0.12),
        "inlineChatDiff.removed": a("diff_removed", 0.12),
        "inlineEdit.modifiedBackground": a(added, 0.06),
        "inlineEdit.modifiedBorder": a(added, 0.25),
        "inlineEdit.modifiedChangedLineBackground": a(added, 0.14),
        "inlineEdit.modifiedChangedTextBackground": a(added, 0.22),
        "inlineEdit.originalBackground": a("diff_removed", 0.06),
        "inlineEdit.originalBorder": a("diff_removed", 0.25),
        "inlineEdit.originalChangedLineBackground": a("diff_removed", 0.14),
        "inlineEdit.originalChangedTextBackground": a("diff_removed", 0.22),
        "inlineEdit.tabWillAcceptModifiedBorder": a(added, 0.25),
        "inlineEdit.tabWillAcceptOriginalBorder": a("diff_removed", 0.25),
        "inlineEdit.gutterIndicator.background": a("muted", 0.12),
    })

    # ----- Merge conflicts (ours green, incoming plum) -----
    u.update({
        "merge.currentHeaderBackground": a("green", 0.45),
        "merge.currentContentBackground": a("green", 0.18),
        "merge.incomingHeaderBackground": a("plum", 0.45),
        "merge.incomingContentBackground": a("plum", 0.18),
        "merge.commonHeaderBackground": a("muted", 0.4),
        "merge.commonContentBackground": a("muted", 0.16),
        "merge.border": NONE,
        "mergeEditor.change.background": a(added, 0.18),
        "mergeEditor.change.word.background": a(added, 0.32),
        "mergeEditor.changeBase.background": a("diff_removed", 0.18),
        "mergeEditor.changeBase.word.background": a("diff_removed", 0.32),
        "mergeEditor.conflict.input1.background": a("green", 0.18),
        "mergeEditor.conflict.input2.background": a("plum", 0.18),
        "mergeEditor.conflict.unhandledFocused.border": "orange",
        "mergeEditor.conflict.unhandledUnfocused.border": a("orange", 0.5),
        "mergeEditor.conflict.handledFocused.border": a("green", 0.8),
        "mergeEditor.conflict.handledUnfocused.border": a("green", 0.4),
        "mergeEditor.conflict.unhandled.minimapOverViewRuler": "orange",
        "mergeEditor.conflict.handled.minimapOverViewRuler": "green",
        "mergeEditor.conflictingLines.background": a("orange", 0.25),
    })

    # ----- Peek view (Alt+F12, references) -----
    u.update({
        "peekView.border": "orange",
        "peekViewEditor.background": "frame",
        "peekViewEditorGutter.background": "frame",
        "peekViewEditorStickyScroll.background": "frame",
        "peekViewEditorStickyScrollGutter.background": "frame",
        "peekViewEditor.matchHighlightBackground": a("orange", 0.35),
        "peekViewResult.background": "widget",
        "peekViewResult.fileForeground": "text",
        "peekViewResult.lineForeground": "muted",
        "peekViewResult.selectionBackground": "selection",
        "peekViewResult.selectionForeground": "text",
        "peekViewResult.matchHighlightBackground": a("orange", 0.3),
        "peekViewTitle.background": "widget",
        "peekViewTitleLabel.foreground": "text",
        "peekViewTitleDescription.foreground": "muted",
    })

    # ----- Command palette, menus and keybinding labels -----
    u.update({
        "pickerGroup.foreground": "orange",
        "pickerGroup.border": "widget_border",
        "quickInputTitle.background": a("text", 0.06),
        "menu.foreground": "text",
        "menu.background": "widget",
        "menu.selectionBackground": "list_active",
        "menu.selectionForeground": "text",
        "menu.separatorBackground": "widget_border",
        "menu.border": "widget_border",
        "menubar.selectionBackground": hover,
        "keybindingLabel.foreground": "text",
        "keybindingLabel.background": a("muted", 0.18),
        "keybindingLabel.border": a("muted", 0.3),
        "keybindingLabel.bottomBorder": a("muted", 0.45),
    })

    # ----- Form controls -----
    u.update({
        "dropdown.foreground": "text",
        "dropdown.listBackground": "input",
        "checkbox.foreground": "text",
        "checkbox.background": "input",
        "checkbox.border": "widget_border",
        "checkbox.selectBorder": "muted",
        "inputOption.activeBorder": "orange",
        "inputOption.activeBackground": a("orange", 0.2),
        "inputOption.activeForeground": "text",
        "inputOption.hoverBackground": hover,
        "radio.activeBorder": "orange",
        "radio.activeBackground": a("orange", 0.2),
        "radio.activeForeground": "text",
        "radio.inactiveBorder": "widget_border",
        "radio.inactiveHoverBackground": hover,
        "inputValidation.errorBackground": "widget",
        "inputValidation.errorBorder": "red",
        "inputValidation.warningBackground": "widget",
        "inputValidation.warningBorder": "orange",
        "inputValidation.infoBackground": "widget",
        "inputValidation.infoBorder": "blue",
        "button.secondaryBackground": "list_active",
        "button.secondaryForeground": "text",
        "button.secondaryHoverBackground": "selection",
        "button.border": NONE,
        "button.separator": a("background", 0.4),
        "progressBar.background": "orange",
    })

    # ----- Lists, trees and drag and drop -----
    u.update({
        "list.errorForeground": "red",
        "list.warningForeground": "orange",
        "list.invalidItemForeground": "orange",
        "list.deemphasizedForeground": "inactive",
        "list.dropBackground": drop,
        "list.dropBetweenBackground": "orange",
        "listFilterWidget.noMatchesOutline": "red",
        "listFilterWidget.outline": NONE,
        "tree.indentGuidesStroke": "guide_active",
        "tree.inactiveIndentGuidesStroke": "guide",
        "tree.tableColumnsBorder": "widget_border",
        "tree.tableOddRowsBackground": a("text", 0.03),
        "sideBar.dropBackground": drop,
        "editorGroup.dropBackground": drop,
        "panelSection.dropBackground": drop,
        "terminal.dropBackground": drop,
        "panelSectionHeader.background": "frame",
        "panelSection.border": NONE,
        "panelInput.border": "widget_border",
        "simpleFindWidget.sashBorder": "widget_border",
    })

    # ----- Settings, welcome page, extensions -----
    u.update({
        "settings.headerForeground": "text",
        "settings.settingsHeaderHoverForeground": a("text", 0.7),
        "settings.modifiedItemIndicator": "orange",
        "settings.checkboxForeground": "text",
        "settings.dropdownForeground": "text",
        "settings.headerBorder": "widget_border",
        "settings.sashBorder": "widget_border",
        "welcomePage.tileBackground": "widget",
        "welcomePage.tileHoverBackground": "list_hover",
        "welcomePage.tileBorder": a("text", 0.1),
        "welcomePage.progress.foreground": "orange",
        "walkthrough.stepTitle.foreground": "text",
        "walkThrough.embeddedEditorBackground": "frame",
        "extensionIcon.starForeground": "orange",
        "extensionIcon.preReleaseForeground": "green",
        "extensionIcon.sponsorForeground": "plum",
        "extensionIcon.verifiedForeground": "green",
        "extensionIcon.privateForeground": a("text", 0.4),
        "mcpIcon.starForeground": "orange",
        "debugToolBar.background": "widget",
        "debugToolBar.border": "widget_border",
    })

    # ----- Debugging -----
    u.update({
        "debugIcon.breakpointForeground": "red",
        "debugIcon.breakpointDisabledForeground": "inactive",
        "debugIcon.breakpointUnverifiedForeground": "muted",
        "debugIcon.breakpointCurrentStackframeForeground": "orange",
        "debugIcon.breakpointStackframeForeground": "green",
        "debugIcon.startForeground": "green",
        "debugIcon.continueForeground": "green",
        "debugIcon.restartForeground": "green",
        "debugIcon.pauseForeground": "orange",
        "debugIcon.stopForeground": "red",
        "debugIcon.disconnectForeground": "red",
        "debugIcon.stepOverForeground": "plum",
        "debugIcon.stepIntoForeground": "plum",
        "debugIcon.stepOutForeground": "plum",
        "debugIcon.stepBackForeground": "plum",
        "debugConsole.errorForeground": "red",
        "debugConsole.warningForeground": "orange",
        "debugConsole.infoForeground": "blue",
        "debugConsole.sourceForeground": "muted",
        "debugConsoleInputIcon.foreground": "orange",
        "debugTokenExpression.name": "plum",
        "debugTokenExpression.type": "plum",
        "debugTokenExpression.value": "muted",
        "debugTokenExpression.string": "blue",
        "debugTokenExpression.number": "orange",
        "debugTokenExpression.boolean": "orange",
        "debugTokenExpression.error": "red",
        "debugView.stateLabelBackground": a("muted", 0.3),
        "debugView.stateLabelForeground": "text",
        "debugView.exceptionLabelBackground": "red",
        "debugView.exceptionLabelForeground": "background",
        "debugView.valueChangedHighlight": "orange",
        "debugExceptionWidget.background": "widget",
        "debugExceptionWidget.border": "red",
    })

    # ----- Testing -----
    u.update({
        "testing.iconPassed": "green",
        "testing.iconFailed": "red",
        "testing.iconErrored": "red",
        "testing.iconQueued": "orange",
        "testing.iconUnset": "muted",
        "testing.iconSkipped": "inactive",
        "testing.runAction": "green",
        "testing.peekBorder": "red",
        "testing.peekHeaderBackground": a("red", 0.1),
        "testing.message.error.lineBackground": a("red", 0.1),
        "testing.message.error.badgeBackground": "red",
        "testing.message.error.badgeForeground": "background",
        "testing.message.error.badgeBorder": "red",
        "testing.message.info.decorationForeground": "muted",
        "testing.coveredBackground": a("green", 0.12),
        "testing.coveredGutterBackground": a("green", 0.5),
        "testing.uncoveredBackground": a("red", 0.12),
        "testing.uncoveredGutterBackground": a("red", 0.5),
        "testing.coverCountBadgeBackground": "muted",
        "testing.coverCountBadgeForeground": "background",
    })

    # ----- Jupyter notebooks -----
    u.update({
        "notebook.cellBorderColor": "widget_border",
        "notebook.focusedCellBorder": "orange",
        "notebook.inactiveFocusedCellBorder": a("orange", 0.4),
        "notebook.focusedEditorBorder": a("orange", 0.5),
        "notebook.selectedCellBorder": "widget_border",
        "notebook.cellToolbarSeparator": "widget_border",
        "notebook.cellStatusBarItemHoverBackground": hover,
        "notebook.symbolHighlightBackground": a("orange", 0.08),
        "notebook.cellInsertionIndicator": "orange",
        "notebookStatusSuccessIcon.foreground": "green",
        "notebookStatusErrorIcon.foreground": "red",
        "notebookStatusRunningIcon.foreground": "orange",
        "notebookEditorOverviewRuler.runningCellForeground": "green",
        "notebookScrollbarSlider.background": a("scrollbar", 0x22 / 255),
        "notebookScrollbarSlider.hoverBackground": a("scrollbar", 0x33 / 255),
        "notebookScrollbarSlider.activeBackground": a("scrollbar", 0x44 / 255),
        "interactive.activeCodeBorder": "orange",
        "interactive.inactiveCodeBorder": "widget_border",
    })

    # ----- Terminal -----
    u.update({
        "terminalCursor.background": "background",
        "terminal.hoverHighlightBackground": a("orange", 0.12),
        "terminal.initialHintForeground": "comment",
        "terminalCommandDecoration.defaultBackground": a("muted", 0.5),
        "terminalCommandDecoration.successBackground": "green",
        "terminalCommandDecoration.errorBackground": "red",
        "terminalOverviewRuler.cursorForeground": "muted",
        "terminalOverviewRuler.findMatchForeground": a("orange", 0.5),
        "terminalStickyScrollHover.background": "list_hover",
        "terminalSymbolIcon.aliasForeground": "plum",
        "terminalSymbolIcon.argumentForeground": "text",
        "terminalSymbolIcon.flagForeground": "orange",
        "terminalSymbolIcon.methodForeground": "green",
        "terminalSymbolIcon.optionForeground": "orange",
        "terminalSymbolIcon.optionValueForeground": "blue",
    })

    # ----- Symbol icons (outline, suggestions) in the same colours as the code -----
    for name, color in {
        "class": "plum", "interface": "plum", "struct": "plum", "enumerator": "plum", "typeParameter": "plum",
        "constructor": "green", "function": "green", "method": "green",
        "constant": "orange", "boolean": "orange", "number": "orange", "null": "orange",
        "enumeratorMember": "orange", "event": "orange", "unit": "orange", "color": "orange",
        "string": "blue", "key": "plum", "keyword": "rust", "operator": "text",
        "variable": "text", "field": "text", "property": "text", "object": "text", "array": "text",
        "module": "text", "namespace": "text", "package": "text", "file": "text", "folder": "text",
        "reference": "text", "snippet": "muted", "text": "muted",
    }.items():
        u[f"symbolIcon.{name}Foreground"] = color

    # ----- Git -----
    u.update({
        "gitDecoration.renamedResourceForeground": "green",
        "gitDecoration.stageModifiedResourceForeground": "orange",
        "gitDecoration.stageDeletedResourceForeground": "red",
        "gitDecoration.conflictingResourceForeground": "plum",
        "gitDecoration.submoduleResourceForeground": "plum",
        "scmGraph.foreground1": "orange",
        "scmGraph.foreground2": "red",
        "scmGraph.foreground3": "green",
        "scmGraph.foreground4": "plum",
        "scmGraph.foreground5": "blue",
        "scmGraph.historyItemRefColor": "orange",
        "scmGraph.historyItemRemoteRefColor": "plum",
        "scmGraph.historyItemBaseRefColor": "green",
        "scmGraph.historyItemHoverAdditionsForeground": "green",
        "scmGraph.historyItemHoverDeletionsForeground": "red",
    })

    # ----- Charts, Markdown alerts and chat -----
    u.update({
        "charts.foreground": "text",
        "charts.lines": "muted",
        "charts.red": "red",
        "charts.orange": "orange",
        "charts.yellow": "orange",
        "charts.green": "green",
        "charts.blue": "blue",
        "charts.purple": "plum",
        "chart.line": "orange",
        "chart.axis": a("muted", 0.4),
        "chart.guide": a("muted", 0.2),
        "agentsWindowGraphic.orange": "orange",
        "markdownAlert.note.foreground": "blue",
        "markdownAlert.tip.foreground": "green",
        "markdownAlert.important.foreground": "plum",
        "markdownAlert.warning.foreground": "orange",
        "markdownAlert.caution.foreground": "red",
        "chat.requestBorder": a("text", 0.1),
        "chat.requestCodeBorder": a("orange", 0.5),
        "chat.slashCommandBackground": a("plum", 0.2),
        "chat.slashCommandForeground": "plum",
        "chat.avatarBackground": "frame",
        "chat.avatarForeground": "text",
        "chat.editedFileForeground": "orange",
        "chat.linesAddedForeground": "green",
        "chat.linesRemovedForeground": "red",
        "chat.checkpointSeparator": "widget_border",
        "chat.mcpCompatibilityWarningForeground": "orange",
        "chat.thinkingShimmer": "text",
        "chat.workingProgressStableIconForeground": "orange",
        "chat.workingProgressInsidersIconForeground": "orange",
        "chat.sessionStateIndicator.needsInputBorder": "orange",
        "chat.sessionStateIndicator.unvisitedBorder": "green",
        "chat.fusionBadgeGradientStart": "orange",
        "chat.fusionBadgeGradientEnd": "red",
        "chat.inputWorkingBorderColor1": "orange",
        "chat.inputWorkingBorderColor2": "red",
        "chat.inputWorkingBorderColor3": "green",
    })
    return u


# ---------- the code (TextMate) ----------

# The environment types in the LaTeX grammar. Used to tell \\begin apart from commands
# such as \\color{...}, which the grammar gives the same scope inside braces.
# VS Code ranks rules by the length of their scope names, so the full names are needed.
ENVIRONMENTS = ["general", "math", "list", "tabular", "frame", "latex.tikz"]


def tokens(p):
    """Rules for colouring code: (name, scopes, colour, style).

    Colour None leaves the colour unchanged, style None leaves the style unchanged,
    and "" means neither bold nor italic. When several rules match, the most
    specific one wins, whatever the order.
    """
    return [
        # ===== All languages =====
        ("Default text", ["source", "variable", "variable.parameter", "meta.function-call.arguments", "keyword.operator", "entity.name.namespace", "entity.name.module", "entity.name.label", "variable.other.readwrite", "variable.other.property", "variable.other.object"], "text", None),
        ("Operators (not bold)", ["keyword.operator", "keyword.operator.assignment", "keyword.operator.arithmetic", "keyword.operator.comparison", "keyword.operator.bitwise", "keyword.operator.pipe", "keyword.operator.redirect", "keyword.operator.expansion"], "text", ""),
        ("Comments", ["comment", "punctuation.definition.comment", "string.quoted.docstring.multi.python", "string.quoted.docstring", "string.quoted.docstring punctuation.definition.string"], "comment", "italic"),
        ("1 Rust: keywords", ["keyword", "storage.type", "storage.modifier", "keyword.other", "keyword.operator.new", "keyword.control.import", "keyword.control.import.python", "storage.type.function.lambda.python", "storage.type.function.async.python"], "rust", ""),
        ("1 Rust, bold: control and logical keywords", ["keyword.control", "keyword.control.flow", "keyword.control.flow.python", "keyword.control.conditional", "keyword.control.loop", "keyword.control.return", "keyword.control.trycatch", "keyword.control.exception", "keyword.operator.logical", "keyword.operator.logical.python", "keyword.operator.word", "keyword.operator.expression", "keyword.operator.instanceof", "keyword.operator.typeof", "storage.type.function.python", "storage.type.class.python"], "rust", "bold"),
        ("2 Orange: numbers and constants", ["constant.numeric", "constant.language", "constant.other", "support.constant", "variable.other.constant", "variable.other.enummember", "constant.other.color", "keyword.other.unit"], "orange", None),
        ("Python: upper-case names are ordinary variables (M, G, LIMIT)", ["constant.other.caps", "constant.other.caps.python", "variable.other.constant"], "text", ""),
        ("2 Orange: number prefixes and suffixes (0x, 1j)", ["storage.type.number", "storage.type.imaginary.number", "storage.type.number.python", "storage.type.imaginary.number.python"], "orange", ""),
        ("3 Blue: strings", ["string", "punctuation.definition.string", "string.quoted", "string.interpolated", "string.template", "string.regexp", "string.other"], "blue", None),
        ("3 Blue: string prefixes (f, r, b)", ["storage.type.string", "storage.type.string.python"], "blue", ""),
        ("4 Green: functions", ["entity.name.function", "support.function", "support.function.builtin", "meta.function-call.generic", "support.function.magic", "variable.function", "entity.name.function.member", "entity.name.command"], "green", None),
        ("5 Plum: classes, types, decorators, self", ["entity.name.type", "entity.name.type.class", "entity.name.class", "entity.other.inherited-class", "support.type", "support.class", "entity.name.function.decorator", "meta.function.decorator", "punctuation.definition.decorator", "variable.language.special.self", "variable.parameter.function.language.special.self", "variable.language.special.cls", "variable.parameter.function.language.special.cls", "variable.language.this", "variable.language.self", "support.variable.magic", "constant.character.escape", "constant.character.format.placeholder", "meta.fstring.python constant.character.format.placeholder", "entity.name.type.parameter", "storage.type.annotation", "support.type.primitive"], "plum", None),
        ("5 Plum: format specifiers in f-strings (:.2f, !r)", ["storage.type.format", "storage.type.format.python"], "plum", ""),
        ("5 Plum: special characters in regular expressions", ["string.regexp keyword.operator", "string.regexp keyword.control", "string.regexp support.other", "string.regexp constant.other.set", "string.regexp constant.other.character-class", "string.regexp constant.character.character-class", "string.regexp punctuation.character.set", "string.regexp punctuation.parenthesis", "string.regexp punctuation.definition.group", "string.regexp punctuation.definition.character-class", "string.regexp keyword.operator.quantifier", "string.regexp keyword.operator.disjunction", "string.regexp support.other.escape.special", "string.regexp support.other.match"], "plum", ""),
        ("Invalid", ["invalid", "invalid.illegal"], "red", None),
        ("Deprecated", ["invalid.deprecated"], "red", "strikethrough"),

        # ===== Markdown =====
        ("Markdown: headings (bold text)", ["markup.heading", "entity.name.section", "markup.heading.setext"], "text", "bold"),
        ("Markdown: # before headings (red)", ["punctuation.definition.heading.markdown"], "red", "bold"),
        ("Markdown bold", ["markup.bold"], None, "bold"),
        ("Markdown italic", ["markup.italic"], None, "italic"),
        ("Markdown strikethrough", ["markup.strikethrough"], None, "strikethrough"),
        ("Markdown underline", ["markup.underline"], None, "underline"),
        ("Markdown: inline code (blue)", ["markup.inline.raw", "markup.inline.raw.string.markdown", "markup.raw", "markup.raw.block.markdown"], "blue", None),
        ("Markdown: code blocks follow their own language", ["markup.fenced_code.block.markdown", "meta.embedded.block"], "text", None),
        ("Markdown: ``` and language name (grey)", ["punctuation.definition.markdown", "fenced_code.block.language", "fenced_code.block.language.markdown", "fenced_code.block.language.attributes.markdown", "punctuation.definition.raw.markdown"], "muted", ""),
        ("Markdown: links (red, as in the PDF)", ["markup.underline.link", "string.other.link", "meta.link.inline.markdown", "meta.image.inline.markdown", "meta.link.reference.markdown", "constant.other.reference.link.markdown"], "red", ""),
        ("Markdown: brackets around links (grey)", ["punctuation.definition.link.title.begin.markdown", "punctuation.definition.link.title.end.markdown", "punctuation.definition.link.description.begin.markdown", "punctuation.definition.link.description.end.markdown", "punctuation.definition.metadata.markdown"], "muted", ""),
        ("Markdown: list markers (rust)", ["punctuation.definition.list.begin.markdown", "beginning.punctuation.definition.list.markdown"], "rust", None),
        ("Markdown: quotes (grey, italic)", ["markup.quote"], "muted", "italic"),
        ("Markdown: rules, table lines and emphasis markers (grey)", ["meta.separator.markdown", "punctuation.definition.table.markdown", "punctuation.separator.table.markdown", "punctuation.definition.strikethrough.markdown", "punctuation.definition.bold.markdown", "punctuation.definition.italic.markdown"], "muted", None),
        ("Markdown: mathematics (blue, commands neutral)", ["meta.embedded.math.markdown", "markup.math.inline.markdown", "markup.math.block.markdown", "meta.function.math.tex"], "blue", None),
        ("Markdown: mathematics, commands such as \\frac (neutral)", ["entity.name.function.math.tex", "punctuation.definition.function.math.tex", "storage.type.function.math.tex"], "text", ""),
        ("Markdown: mathematics, operators (neutral)", ["punctuation.math.operator.latex", "punctuation.line.separator.math.tex", "line.separator.math.tex"], "text", None),
        ("Markdown: mathematics, $ and brackets (grey)", ["punctuation.definition.math.begin.markdown", "punctuation.definition.math.end.markdown", "punctuation.math.begin.bracket.curly", "punctuation.math.end.bracket.curly", "punctuation.math.begin.bracket.round", "punctuation.math.end.bracket.round", "punctuation.definition.arguments.begin.math.tex", "punctuation.definition.arguments.end.math.tex"], "muted", None),

        # ===== LaTeX =====
        ("LaTeX: structure (rust)", ["keyword.control.preamble.latex", "keyword.control.include.latex", "storage.type.function.latex", "keyword.other.item.latex", "storage.type.function.tex", "keyword.control.tex", "keyword.control.catcode.tex"], "rust", ""),
        ("LaTeX: \\begin and \\end (rust, bold)", ["support.function.be.latex"], "rust", "bold"),
        ("LaTeX: sectioning commands (red, bold)", ["support.function.section.latex"], "red", "bold"),
        ("LaTeX: line breaks and table cells (neutral)", ["keyword.control.newline.tex", "keyword.control.equation.newline.latex", "keyword.control.table.cell.latex", "keyword.control.table.newline.latex", "keyword.control.equation.align.latex", "keyword.control.layout.latex"], "text", ""),
        ("LaTeX: section titles", ["entity.name.section.latex"], "text", "bold"),
        ("LaTeX: mathematics, variables (blue)", ["support.class.math.block.tex", "support.class.math.block.environment.latex", "meta.math.block.tex", "meta.math.block.latex"], "blue", None),
        ("LaTeX: Greek letters and symbols (plum)", ["constant.character.math.tex"], "plum", None),
        ("LaTeX: numbers (orange)", ["constant.numeric.math.tex"], "orange", None),
        ("LaTeX: plain text inside maths (\\text{})", ["meta.text.normal.tex"], "text", None),
        ("LaTeX: environment names (green, bold)", ["variable.parameter.function.latex"], "green", "bold"),
        ("LaTeX: names of new commands (green)", ["meta.parameter.newcommand.latex support.function.general.latex", "entity.name.function.latex", "entity.name.function.tex"], "green", ""),
        ("LaTeX: other commands (neutral)", ["support.function.general.latex", "support.function.general.tex", "support.function.emph.latex", "support.function.textbf.latex", "support.function.textit.latex", "support.function.texttt.latex", "support.function.url.latex", "support.function.footnote.latex", "support.function.marginpar.latex", "support.function.verb.latex", "keyword.control.ref.latex", "keyword.control.label.latex", "keyword.control.cite.latex", "constant.other.general.math.tex", "constant.other.math.tex", "support.function.textcolor.latex", "support.function.textsubscript.latex", "support.function.textsuperscript.latex", "support.function.textsc.latex", "support.function.textsf.latex", "support.function.textrm.latex", "support.function.underline.latex"], "text", ""),
        ("LaTeX: commands in braces and in \\newcommand that are not environments (neutral)", ["meta.group.braces.latex support.function.be.latex", "meta.parameter.newcommand.latex support.function.be.latex", "meta.group.braces.latex variable.parameter.function.latex", "meta.parameter.newcommand.latex variable.parameter.function.latex"], "text", ""),
        ("LaTeX: \\begin and \\end inside braces (rust, bold)", [f"{f} meta.function.environment.{m}.latex support.function.be.latex".replace(".latex.tikz.latex", ".latex.tikz") for f in ("meta.group.braces.latex", "meta.parameter.newcommand.latex") for m in ENVIRONMENTS], "rust", "bold"),
        ("LaTeX: environment names inside braces (green, bold)", [f"{f} meta.function.environment.{m}.latex variable.parameter.function.latex".replace(".latex.tikz.latex", ".latex.tikz") for f in ("meta.group.braces.latex", "meta.parameter.newcommand.latex") for m in ENVIRONMENTS], "green", "bold"),
        ("LaTeX: labels and keys (neutral)", ["variable.parameter.definition.label.latex", "constant.other.reference.label.latex", "constant.other.reference.citation.latex", "support.class.latex", "constant.other.citation.latex"], "text", ""),
        ("LaTeX: operators (neutral)", ["punctuation.math.operator.tex"], "text", None),
        ("LaTeX: bold text", ["markup.bold.textbf.latex"], "text", "bold"),
        ("LaTeX: italic text", ["markup.italic.emph.latex", "markup.italic.textit.latex"], "text", "italic"),
        ("LaTeX: braces, brackets and $ (grey)", [
            "punctuation.definition.arguments.begin.latex", "punctuation.definition.arguments.end.latex",
            "punctuation.definition.arguments.begin.tex", "punctuation.definition.arguments.end.tex",
            "punctuation.definition.arguments.optional.begin.latex", "punctuation.definition.arguments.optional.end.latex",
            "punctuation.group.begin.latex", "punctuation.group.end.latex", "punctuation.group.begin.tex", "punctuation.group.end.tex",
            "punctuation.definition.brackets.tex",
            "punctuation.definition.begin.latex", "punctuation.definition.end.latex",
            "punctuation.math.begin.bracket.curly.tex", "punctuation.math.end.bracket.curly.tex",
            "punctuation.math.begin.bracket.round.tex", "punctuation.math.end.bracket.round.tex",
            "punctuation.math.bracket.pair.tex", "punctuation.math.bracket.pair.big.tex",
            "punctuation.definition.emph.begin.latex", "punctuation.definition.emph.end.latex",
            "punctuation.definition.textbf.begin.latex", "punctuation.definition.textbf.end.latex",
            "punctuation.definition.textit.begin.latex", "punctuation.definition.textit.end.latex",
            "punctuation.definition.texttt.begin.latex", "punctuation.definition.texttt.end.latex",
            "punctuation.definition.footnote.begin.latex", "punctuation.definition.footnote.end.latex",
            "punctuation.definition.marginpar.begin.latex", "punctuation.definition.marginpar.end.latex",
            "punctuation.definition.string.begin.tex", "punctuation.definition.string.end.tex",
            "punctuation.definition.string.begin.latex", "punctuation.definition.string.end.latex",
            "punctuation.section.embedded.begin.math.tex", "punctuation.section.embedded.end.math.tex",
            "punctuation.definition.verb.latex",
        ], "muted", ""),
        ("LaTeX: comments", ["comment.line.percentage.tex", "comment.line.percentage.latex", "punctuation.definition.comment.tex", "punctuation.definition.comment.latex", "comment.block.preprocessor.tex", "comment.line.percentage.directive.texshop.tex"], "comment", "italic"),
        ("LaTeX: references and links (red, as in the PDF)", ["keyword.control.ref.latex", "keyword.control.cite.latex", "constant.other.reference.label.latex", "constant.other.reference.citation.latex", "support.function.url.latex", "markup.underline.link.latex", "keyword.control.ref.latex punctuation.definition.keyword.latex", "keyword.control.cite.latex punctuation.definition.keyword.latex", "support.function.url.latex punctuation.definition.function.latex"], "red", ""),
        ("LaTeX: siunitx and mhchem, command names (neutral)", ["support.function.siunitx.latex", "support.function.mhchem.latex"], "text", ""),
        ("LaTeX: siunitx units (text colour, also in maths)", ["meta.unit.siunitx.latex"], "text", ""),
        ("LaTeX: chemical formulas in \\ce (blue, like maths)", ["meta.chemistry.mhchem.latex"], "blue", ""),
        ("LaTeX: file paths (blue, like strings)", ["string.unquoted.path.latex", "meta.include.latex"], "blue", ""),
        ("LaTeX: package options (text colour, not green and bold)", ["meta.parameter.optional.latex variable.parameter.function.latex"], "text", ""),
        ("LaTeX: drawing commands in tikzpicture (green)", ["meta.function.environment.latex.tikz support.function.general.latex", "meta.function.environment.latex.tikz support.function.general.tex"], "green", ""),

        # ===== BibTeX =====
        ("BibTeX: entry type (@book)", ["keyword.other.entry-type.bibtex", "punctuation.definition.keyword.bibtex"], "rust", "bold"),
        ("BibTeX: the key used in \\cite (neutral, bold)", ["entity.name.type.entry-key.bibtex"], "text", "bold"),
        ("BibTeX: field names (plum)", ["support.function.key.bibtex", "string.unquoted.key.bibtex"], "plum", ""),
        ("BibTeX: values (neutral)", ["meta.key-assignment.bibtex"], "text", None),
        ("BibTeX: braces around values (grey)", ["meta.key-assignment.bibtex punctuation.definition.string.begin.bibtex", "meta.key-assignment.bibtex punctuation.definition.string.end.bibtex", "punctuation.section.entry.begin.bibtex", "punctuation.section.entry.end.bibtex", "punctuation.definition.group.begin.bibtex", "punctuation.definition.group.end.bibtex"], "muted", None),

        # ===== Data and configuration (JSON, YAML, TOML, INI) =====
        ("General: keys and attributes (plum)", ["support.type.property-name", "meta.object-literal.key", "entity.other.attribute-name", "meta.mapping.key string", "support.type.property-name.toml", "keyword.other.definition.ini", "entity.name.section.group-title.ini"], "plum", ""),
        ("General: HTML and XML tags, and CSS type selectors (rust, structure)", ["entity.name.tag"], "rust", ""),
        ("General: < and > around tags (grey, like brackets)", ["punctuation.definition.tag"], "muted", ""),
        ("YAML: keys (plum, although the grammar calls them tags)", ["entity.name.tag.yaml"], "plum", ""),
        ("General: built-in types (int, double, char) are types (plum)", ["storage.type.built-in", "storage.type.built-in.primitive", "storage.type.primitive", "support.type.primitive", "support.type.builtin"], "plum", ""),
        ("General: super and other language variables (plum)", ["variable.language.super", "variable.language.makefile", "constant.character.entity", "punctuation.definition.entity.html"], "plum", ""),
        ("Markdown: front matter delimiters (grey)", ["punctuation.definition.begin.frontmatter", "punctuation.definition.end.frontmatter"], "muted", ""),
        ("YAML: anchors and aliases (plum)", ["variable.other.anchor", "variable.other.alias", "punctuation.definition.anchor", "punctuation.definition.alias"], "plum", ""),
        ("JSON and YAML: structural punctuation (grey)", ["punctuation.support.type.property-name", "punctuation.definition.dictionary", "punctuation.definition.array", "punctuation.definition.mapping", "punctuation.definition.sequence"], "muted", None),

        # ===== Diff and git =====
        ("Diff: added (green)", ["markup.inserted", "punctuation.definition.inserted", "meta.diff.header.to-file", "punctuation.definition.to-file.diff"], "green", None),
        ("Diff: removed (red)", ["markup.deleted", "punctuation.definition.deleted", "meta.diff.header.from-file", "punctuation.definition.from-file.diff"], "red", None),
        ("Diff: changed (orange)", ["markup.changed", "punctuation.definition.changed"], "orange", None),
        ("Diff: line numbers and hunk headers (plum)", ["meta.diff.range", "meta.toc-list.line-number.diff", "punctuation.definition.range.diff"], "plum", None),
        ("Diff: git header (bold)", ["meta.diff.header.git", "meta.diff.header.command", "meta.diff.index.git", "meta.diff.index"], "muted", "bold"),
        ("Git commit: subject line", ["meta.scope.subject.git-commit"], "text", "bold"),
        ("Git commit: files in the comment", ["comment markup.inserted.git-commit", "comment markup.deleted.git-commit", "comment markup.changed.git-commit"], None, "italic"),

        # ===== Shell =====
        ("Shell: variables ($HOME)", ["variable.other.normal.shell", "variable.other.positional.shell", "variable.parameter.positional.shell", "variable.other.special.shell", "punctuation.definition.variable.shell"], "plum", ""),
        ("Shell: shebang", ["meta.shebang", "comment.line.shebang"], "comment", "italic"),

        # ===== Logs (Output panel) =====
        ("Log: error (red)", ["token.error-token", "log.error"], "red", None),
        ("Log: warning (orange)", ["token.warn-token", "log.warning"], "orange", None),
        ("Log: info (green)", ["token.info-token", "log.info"], "green", None),
        ("Log: debug (grey)", ["token.debug-token", "log.debug"], "comment", None),
    ]


def semantic_rules(p):
    """Semantic highlighting (Pylance and other language servers): token type -> palette name and style."""
    return {
        "class": "plum",
        "class.builtin": "plum",
        "type": "plum",
        "typeParameter": "plum",
        "enum": "plum",
        "interface": "plum",
        "struct": "plum",
        "decorator": "plum",
        "selfParameter": "plum",
        "clsParameter": "plum",
        "function": "green",
        "function.builtin": "green",
        "method": "green",
        "macro": "green",
        "namespace": "text",
        "module": "text",
        "variable": "text",
        # Pylance treats every upper-case name as a constant, including M, G and F in physics code.
        # They get the text colour like other variables; orange is for numbers, True, False and None.
        "variable.readonly": "text",
        "variable.readonly.builtin": "text",
        "enumMember": "orange",
        "parameter": "text",
        "property": "text",
        "property.readonly": "text",
        "keyword": "rust",
        "number": "orange",
        "string": "blue",
        "regexp": "blue",
        "operator": "text",
        "comment": ("comment", "italic"),
        "*.deprecated": {"strikethrough": True},
    }


# ---------- building ----------

def make_theme(name, p):
    colors = {k: resolve(p, v) for k, v in ui(p).items()}
    token_colors = []
    for rule_name, scopes, color, style in tokens(p):
        settings = {}
        if color is not None:
            settings["foreground"] = resolve(p, color)
        if style is not None:
            settings["fontStyle"] = style
        token_colors.append({"name": rule_name, "scope": scopes, "settings": settings})
    semantic = {}
    for k, v in semantic_rules(p).items():
        if isinstance(v, dict):
            semantic[k] = v
        elif isinstance(v, tuple):
            semantic[k] = {"foreground": resolve(p, v[0]), v[1]: True}
        else:
            semantic[k] = resolve(p, v)
    return {
        "$schema": "vscode://schemas/color-theme",
        "name": name,
        "type": p["type"],
        "semanticHighlighting": True,
        "colors": colors,
        "tokenColors": token_colors,
        "semanticTokenColors": semantic,
    }


def make_iterm(p):
    i = p["iterm"]
    out = {}

    def color(v):
        h, alpha = (v if isinstance(v, tuple) else (v, 1.0))
        r, g, b = hex_to_rgb(h)
        return {"Alpha Component": float(alpha), "Blue Component": b / 255, "Color Space": "sRGB",
                "Green Component": g / 255, "Red Component": r / 255}

    for n, v in enumerate(i["ansi"]):
        out[f"Ansi {n} Color"] = color(v)
    for k, v in i.items():
        if k != "ansi":
            out[k] = color(v)
    return dict(sorted(out.items()))


def check(name, p):
    print(f"\n{name}: contrast against the editor background {p['background']} (4.5 recommended for normal text, 3 for bold)")
    for role in ["text", "red", "rust", "orange", "green", "blue", "plum", "muted", "comment", "line_number", "inactive"]:
        k = round(contrast(p[role], p["background"]), 1)
        note = "" if k >= 4.5 else ("  (bold or large text only)" if k >= 3 else "  (low)")
        print(f"  {role:12s} {p[role]}  {k:4.1f}" + note)


def make_svg():
    """docs/palette.svg: the templates, Høstlys and Høstkveld, one row each."""
    templates = ["#781414", "#b85c00", "#4a6b12", "#1e608c", "#6e3278"]
    rows = [("LuaLaTeX templates", "#ffffff", "#282828", templates, [None] * 5),
            ("Høstlys", HOSTLYS["background"], HOSTLYS["text"], [HOSTLYS[n] for n in COLORS], COLORS),
            ("Høstkveld", HOSTKVELD["background"], HOSTKVELD["text"], [HOSTKVELD[n] for n in COLORS], COLORS)]
    b, h, gap, x0 = 96, 96, 12, 222
    width = x0 + 6 * (b + gap) + 8
    y, parts = 12, []
    for title, bg, fg, colors, roles in rows:
        height = h + 64
        parts.append(f'<rect x="8" y="{y}" width="{width - 16}" height="{height}" rx="14" fill="{bg}" stroke="#d8d2bf"/>')
        parts.append(f'<text x="26" y="{y + height / 2 + 6}" font-family="Helvetica,Arial,sans-serif" font-size="17" font-weight="600" fill="{fg}">{title}</text>')
        if len(colors) == 5:  # the templates have no rust; its slot stays empty
            slots = [x0] + [x0 + (i + 2) * (b + gap) for i in range(4)]
        else:
            slots = [x0 + i * (b + gap) for i in range(6)]
        for x, c, r in zip(slots, colors, roles):
            parts.append(f'<rect x="{x}" y="{y + 14}" width="{b}" height="{h}" rx="10" fill="{c}"/>')
            label = f"{r} " if r else ""
            parts.append(f'<text x="{x + b / 2}" y="{y + h + 34}" text-anchor="middle" font-family="Menlo,monospace" font-size="11" fill="{fg}" opacity="0.75">{label}{c.upper()}</text>')
        y += height + 14
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{y}" viewBox="0 0 {width} {y}">' + "".join(parts) + "</svg>\n"
    (DOCS / "palette.svg").write_text(svg, encoding="utf-8")


def main():
    for d in (THEMES, ITERM, DOCS):
        d.mkdir(parents=True, exist_ok=True)
    for name, file, p in [("Høstlys", "hostlys", HOSTLYS), ("Høstkveld", "hostkveld", HOSTKVELD)]:
        theme = make_theme(name, p)
        (THEMES / f"{file}-color-theme.json").write_text(json.dumps(theme, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        with open(ITERM / f"{name}.itermcolors", "wb") as f:
            plistlib.dump(make_iterm(p), f)
        print(f"OK: {name} ({len(theme['colors'])} workbench colours, {len(theme['tokenColors'])} code rules)")
        if "--check" in sys.argv:
            check(name, p)
    make_svg()


if __name__ == "__main__":
    main()
