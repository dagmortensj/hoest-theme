// A button at the right of the status bar that switches between Høstlys and Høstkveld.
// It is shown only while one of the two themes is active.
//
// If workbench.preferredLightColorTheme and workbench.preferredDarkColorTheme are set to
// Høstlys and Høstkveld, the button runs VS Code's own command for switching between them.
// Otherwise it sets workbench.colorTheme directly, so it works without those settings.
const vscode = require('vscode');

const LIGHT = 'Høstlys';
const DARK = 'Høstkveld';

function workbench() {
  return vscode.workspace.getConfiguration('workbench');
}

function activeTheme() {
  const kind = vscode.window.activeColorTheme.kind;
  const dark = kind === vscode.ColorThemeKind.Dark || kind === vscode.ColorThemeKind.HighContrast;
  if (vscode.workspace.getConfiguration('window').get('autoDetectColorScheme')) {
    return workbench().get(dark ? 'preferredDarkColorTheme' : 'preferredLightColorTheme');
  }
  return workbench().get('colorTheme');
}

function pairIsSet() {
  return workbench().get('preferredLightColorTheme') === LIGHT
    && workbench().get('preferredDarkColorTheme') === DARK;
}

async function toggle() {
  if (pairIsSet()) {
    await vscode.commands.executeCommand('workbench.action.toggleLightDarkThemes');
    return;
  }
  const next = activeTheme() === DARK ? LIGHT : DARK;
  await workbench().update('colorTheme', next, vscode.ConfigurationTarget.Global);
}

function activate(context) {
  const button = vscode.window.createStatusBarItem('hoest.toggle', vscode.StatusBarAlignment.Right, 1000);
  button.name = 'Høst: switch between light and dark';
  button.text = '$(color-mode)';
  button.tooltip = `Switch between ${LIGHT} and ${DARK}`;
  button.command = 'hoest.toggle';

  const refresh = () => {
    const theme = activeTheme();
    if (theme === LIGHT || theme === DARK) button.show();
    else button.hide();
  };

  context.subscriptions.push(
    button,
    vscode.commands.registerCommand('hoest.toggle', toggle),
    vscode.window.onDidChangeActiveColorTheme(refresh),
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration('workbench') || e.affectsConfiguration('window.autoDetectColorScheme')) refresh();
    }),
  );
  refresh();
}

function deactivate() {}

module.exports = { activate, deactivate };
