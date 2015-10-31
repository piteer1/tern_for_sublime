'''
Module contains all listeners
'''

import sublime_plugin, sublime

import os
import collections
import hashlib

from .manager import Manager
from .utils import project_dirname
from .renderer import query_format

CACHE_LIMIT = 5

#stores completions per view
completions = {}


def is_js_file(view):
    '''
    Checks if given file is a JavaScript file based on syntax and file extension

    @param view: A sublime view
    '''

    syntax = os.path.splitext(os.path.basename(view.settings().get('syntax')))[0]
    filename = view.file_name()
    js_ext = filename is not None and os.path.splitext(filename)[1] == '.js'

    return syntax == 'JavaScript' or js_ext

def show_auto_complete(view, on_query_info,
                       disable_auto_insert=True, api_completions_only=True,
                       next_completion_if_showing=False, auto_complete_commit_on_tab=True):
    # Show autocompletions:
    def _show_auto_complete():
        view.run_command('auto_complete', {
            'disable_auto_insert': disable_auto_insert,
            'api_completions_only': api_completions_only,
            'next_completion_if_showing': next_completion_if_showing,
            'auto_complete_commit_on_tab': auto_complete_commit_on_tab,
        })
    completions[view.id()] = on_query_info
    sublime.set_timeout(_show_auto_complete, 0)

class ViewModifiedListener(sublime_plugin.EventListener):

    def on_modified_async(self, view):
        '''
        Queries TernJS server. Quering is done here, because of
        syncronous on_query_completions. This function calls async
        the on_query_completions method at the end
        '''
        manager = Manager.instance()
        if not is_js_file(view):
            return
        client = manager.client(project_dirname(view.window()))
        if client is None:
            return
        current_completions = client.completions(view, {"type": "completions", "types": True})

        completion = [query_format(completion) for completion in current_completions['completions']]

        show_auto_complete(view, completion)

    def on_query_completions(self, view, prefix, locations):
        '''
        Returns completions if available. This function is NOT quering
        the TernJS server because it's syncronous. This would lags while
        editing files in bigger projects!
        '''

        print ('asking for completions', view.id())
        print('has completions', view.id() in completions, completions)
        if view.id() in completions:
            completion = completions[view.id()]
            del completions[view.id()]
            return completion
