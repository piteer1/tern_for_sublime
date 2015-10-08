# Sublime Text plugin for Tern

import os

from .tern.commands import *
from .tern.listeners import *
from .tern.manager import Manager

import sublime, sublime_plugin


def plugin_loaded():
    print('Tern sublime plugin loaded')
    manager = Manager.instance()
