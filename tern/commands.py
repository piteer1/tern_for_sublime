# Sublime Text plugin for Tern

from __future__ import absolute_import

import sublime, sublime_plugin

import json, re, time, atexit

from .manager import Manager


# def is_js_file(view):
#   return view.score_selector(sel_end(view.sel()[0]), "source.js") > 0

class NewTernCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    print('command ran')


