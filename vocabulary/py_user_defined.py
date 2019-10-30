# -*- coding: utf-8 -*-

class UserDefined():

    def __init__(self, content):
        self.content = content

    def start(self):
        self._find_functions()
        return self.content

    def _find_functions(self):
        # read in file
        lines = self.content.split('\r\n')
        no = -1
        for line in lines:
            no += 1
            if 'def ' in line:
                name, values = self._parse_function(line)

    def _pares_function(self, line):
        splits = line.split('(')
        name = splits[0].split(' ')[1]
        value_str = splits[1].split(')')[0]
        if ' ' in value_str:
            values = value_str.split(', ')
        else:
            values = value_str.split(',')

        return name, values
