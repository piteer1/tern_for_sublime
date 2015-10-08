'''
Top level management functions
'''

import sublime
import os

from .utils import tern_command, project_dirname
from .server import Server
from .client import Client

class Manager(object):
    '''
    Class which manages ternjs

    For now it's a singleton, which should be rather refactored latef
    '''

    _instance = None

    @classmethod
    def instance(cls):
        '''
        Returns instance of a manager
        '''
        if cls._instance is None:
            cls._instance = Manager()

        return cls._instance

    '''
    Manages plugin
    '''
    def __init__(self):
        if self._instance is not None:
            raise RuntimeError("This class is a singleton, please use instance property")
        self.servers = []
        self.clients = []
        self.start_servers()

    def start_servers(self):
        '''
        Starts servers for currently opened projects
        '''
        command = tern_command()
        root_path = project_dirname(sublime.active_window())
        server = Server(root_path, command)
        self.servers.append(server)
        for server in self.servers:
            server.start()
            self.clients.append(Client(server.port, root_path))

    def client(self, root_path):
        return next(client for client in self.clients if client.root_path == root_path)


