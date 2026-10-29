// A button at the right of the status bar that switches between Høstlys and Høstkveld.
// It runs VS Code's own command, which toggles between
// workbench.preferredLightColorTheme and workbench.preferredDarkColorTheme.
const vscode = require('vscode');

function activate(context) {
  const button = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 1000);
  button.text = '$(color-mode)';
  button.tooltip = 'Switch between Høstlys and Høstkveld';
  button.command = 'workbench.action.toggleLightDarkThemes';
  button.show();
  context.subscriptions.push(button);
}

function deactivate() {}

module.exports = { activate, deactivate };
