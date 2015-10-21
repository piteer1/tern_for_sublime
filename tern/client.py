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

    def completions(self, view, query):
        '''
        Make a request to a server with given query
        @TODO: change it so it will use internal request method with correct data formatted here
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

        output = self._request(document)

        print('client output', output)

        return output

    def _request(self, document):
        '''
        Does a request to ternjs server
        '''
        print('sending', document)
        serialized = json.dumps(document).encode('utf-8')

        req = urllib.request.Request(
            'http://' + localhost + ":" + str(self.port),
            data=serialized,
            headers={'content-type': 'application/json'}
        )
        response = urllib.request.urlopen(req)

        return json.loads(str(response.read().decode('utf-8')))
