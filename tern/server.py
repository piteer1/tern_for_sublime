
import subprocess
import platform
import os
import re

from .utils import windows, PLUGIN_DIR

class Server(object):
    '''
    A ternjs server
    '''

    def __init__(self, root_path, command):
        self.command = command
        self.arguments = ["--no-port-file", '--persistent', '--verbose']
        self.proc = None
        self.port = None
        self.root_path = root_path

    def start(self):
        '''
        Starts a new server for a project
        '''
        if not self.command:
            return None
        env = None
        if platform.system() == "Darwin":
            env = os.environ.copy()
            env["PATH"] += ":/usr/local/bin"
        proc = subprocess.Popen(
            self.command + self.arguments, cwd=PLUGIN_DIR, env=env,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, shell=windows
        )


        line = proc.stdout.readline().decode("utf-8")
        match = re.match("Listening on port (\\d+)", line)
        if match:
            self.proc = proc
            self.port = int(match.group(1))
        else:
            raise ServerSpawnError("Failed to start server" + (line and ":\n" + line))


    def kill(self):
        '''
        Kill server
        '''

        self.proc.stdin.close()
        self.proc.kill()
        self.proc = None

class ServerSpawnError(RuntimeError):
    '''
    A server spawn error
    '''
    pass
