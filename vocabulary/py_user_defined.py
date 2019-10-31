# -*- coding: utf-8 -*-

class UserDefined():

    def __init__(self, content):
        self.indent = 4
        self.content = content
        self.classes_parent = {}
        self.functions_parent = {'__file__': []}
        self.functions = []

    def start(self):
        self._findall()
        print(self.functions_parent)
        return self.content

    def _findall(self):

        lines = self.content.split('\r\n')
        no = -1
        for line in lines:
            no += 1
            if 'class ' in line:
                self._parse_classes(line)
            elif 'def ' in line:
                name, values = self._parse_function(line)

    def _parse_classes(self, line):
        splits = line.split('class ')
        spaces = splits[0]
        remain = splits[1]
        if '(' in remain:
            name = remain.split('(')[0]
        elif ' :' in remain:
            name = remain.split(' :')[0]
        else:
            name = remain.split(':')[0]

        indent = len(spaces)
        if indent in self.classes_parent:
            self.classes_parent[indent].append(name)
        else:
            self.classes_parent[indent] = [name]

    def _parse_function(self, line):
        splits = line.split('def ')
        
        indent = len(splits[0])

        remain = splits[1].split('(')
        name = remain[0]
        value_str = remain[1].split(')')[0]

        if ' ' in value_str:
            values = value_str.split(', ')
        else:
            values = value_str.split(',')

        if indent == 0:
            self.functions_parent['__file__'].append(name)
            self.functions.append(name)
        else:
            ind = indent - self.indent
            if ind in self.classes_parent:
                class_name = self.classes_parent[ind][-1]
                if class_name in self.functions_parent:
                    self.functions_parent[class_name].append(name)
                    self.functions.append(name)
                else:
                    self.functions_parent[class_name] = [name]
                    self.functions.append(name)
        return name, values
