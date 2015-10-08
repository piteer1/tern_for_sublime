'''
Module contains all listeners
'''

import sublime_plugin

import os

from .manager import Manager
from .utils import project_dirname

def is_js_file(filename):
    '''
    Checks if given file is a JavaScript file
    '''
    return filename is not None and os.path.splitext(filename)[1] == '.js'

class ViewModifiedListener(sublime_plugin.EventListener):
    '''
    Listens for any view modification
    '''

    def on_modified_async(self, view):
        '''
        Queries a server for completions
        '''
        manager = Manager.instance()
        if not is_js_file(view.file_name()):
            return
        client = manager.client(project_dirname(view.window()))
        client.request(view, {"type": "completions", "types": True})