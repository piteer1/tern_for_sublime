'''
Contains client class for communication with
tern server
'''

import json

import urllib.request

import sublime

from .utils import localhost

class Client(object):
    '''
    A ternjs client
    '''

    def __init__(self, port, root_path):
        self.port = port
        self.root_path = root_path

    def request(self, view, query):
        '''
        Make a request to a server with given query
        '''
        text = view.substr(sublime.Region(0, view.size()))
        selection = view.sel()
        end = max(selection[0].a, selection[0].b)
        query['end'] = end
        query['file'] = '#0'
        # -> #<number> where number is the number of file in files array for which the completition is queried
        document = {'query': query, 'files': [{
            "type": "full",
            "name": view.file_name()[len(self.root_path) + 1:],
            # "offset": 0,
            "text": text
        }]}

        print('sending', document)
        serialized = json.dumps(document).encode('utf-8')

        req = urllib.request.Request(
            'http://' + localhost + ":" + str(self.port),
            data=serialized,
            headers={'content-type': 'application/json'}
        )
        response = urllib.request.urlopen(req)

        output = json.loads(str(response.read().decode('utf-8')))
        print('ternjs output', output)
        return output
