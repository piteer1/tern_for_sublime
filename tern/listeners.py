'''
Module contains all listeners
'''

import sublime_plugin

import os

from .manager import Manager
from .utils import project_dirname
from .renderer import query_format

def is_js_file(view):
    '''
    Checks if given file is a JavaScript file based on syntax and file extension

    @param view: A sublime view
    '''

    syntax = os.path.splitext(os.path.basename(view.settings().get('syntax')))[0]
    filename = view.file_name()
    js_ext = filename is not None and os.path.splitext(filename)[1] == '.js'

    return syntax == 'JavaScript' or js_ext


class ViewModifiedListener(sublime_plugin.EventListener):
    '''
    Listens for any view modification
    '''

    def on_modified_async(self, view):
        '''
        @todo: would be better to get some data here and use it
        during query completions
        '''

    def on_query_completions(self, view, prefix, locations):
        '''
        Queries a server for completions
        '''
        manager = Manager.instance()
        if not is_js_file(view):
            return
        client = manager.client(project_dirname(view.window()))
        if client is None:
            return
        completions = client.completions(view, {"type": "completions", "types": True})

        output = [query_format(completion) for completion in completions['completions']]
        print('on query completions output', output)
        return output
