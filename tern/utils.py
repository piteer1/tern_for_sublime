import platform
import os
import subprocess
import sys

import sublime, sublime_plugin

windows = platform.system() == "Windows"
python3 = sys.version_info[0] > 2
localhost = (windows and "127.0.0.1") or "localhost"

PLUGIN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_setting(key, default):
    '''
    fetch a certain setting from the package settings file and if it doesn't exist check the
    Preferences.sublime-settings file for backwards compatibility.
    '''
    old_settings = sublime.load_settings("Preferences.sublime-settings")
    new_settings = sublime.load_settings("Tern.sublime-settings")

    setting = new_settings.get(key, None)
    if setting is None:
        return old_settings.get(key, default)
    else:
        return new_settings.get(key, default)

def tern_command():
    command = get_setting("tern_command", None)
    if command is None:
        if not os.path.isdir(os.path.join(PLUGIN_DIR, "node_modules/tern")):
            if sublime.ok_cancel_dialog(
                    "It appears Tern has not been installed. Do you want tern_for_sublime to try and install it? "
                    "(Note that this will only work if you already have node.js and npm installed on your system.)"
                    "\n\nTo get rid of this dialog, either uninstall new_tern_for_sublime, or set the tern_command setting.",
                    "Yes, install."
                ):
                try:
                    path = os.environ.get('PATH', '') + ':/usr/local/bin/'

                    if hasattr(subprocess, "check_output"):
                        subprocess.check_output(["npm", "install"], cwd=PLUGIN_DIR, env=dict(os.environ, PATH=path))
                    else:
                        subprocess.check_call(["npm", "install"], cwd=PLUGIN_DIR, env=dict(os.environ, PATH=path))
                except subprocess.CalledProcessError as ex:
                    msg = "Installation failed. Try doing 'npm install' manually in " + PLUGIN_DIR + "."
                    if hasattr(ex, "output"):
                        msg += " Error message was:\n\n" + ex.output
                    sublime.error_message(msg)
                    return
        command = ["node", os.path.join(PLUGIN_DIR, "node_modules/.bin/tern")]
    return command
