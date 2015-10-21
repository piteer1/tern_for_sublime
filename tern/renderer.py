'''
Methods for formatting/rendering query completions
'''

import re

class Completion(object):
    '''
    Formats query completion
    '''
    function_params = re.compile(r"^fn\(([^)]*)\)")

    def __init__(self, completion):
        self.completion = completion

    def is_function(self):
        '''
        Checks if completion is a function

        :rtype: bool
        '''

        completion_type = self.completion.get('type', None)
        return completion_type is not None and completion_type.startswith('fn(')

    def format(self):
        '''
        Formats completion to match sublime query format
        '''
        if 'type' not in self.completion:
            # no type hints were found at all
            return self.completion['name']

        completion = self.completion['type']
        output = self.completion['name']

        if self.is_function():
            output += self._format_fuction(completion)

        return output

    def _format_fuction(self, completion):
        stripped_fn = re.match(self.function_params, completion).group(1)
        separator = ', '
        return "(%s)" % separator.join([
            "${%d:%s}" % (index + 1, value) for index, value in enumerate(stripped_fn.split(separator))
        ])

    def __repr__(self):
        return self.format()
    def __str__(self):
        return self.format()

def query_format(completion):
    '''
    Generates correct output format for sublime for a given completion
    '''
    formatter = Completion(completion)
    completion_type = completion['type'] if 'type' in completion else ''

    return (
        '{completion} {description}'.format(completion=completion['name'], description=completion_type),
        formatter.format()
    )
