# -*- coding: utf-8 -*-

class UserDefined():

    def __init__(self, content):
        self.indent = 4
        self.content = content
        self.classes_parent = {}
        self.curr_class = ''
        self.functions_parent = {'__main_parent__': []}
        self.functions = []
        self.var_parent = {'__main_parent__': []}
        self.variables = {'__main_parent__': [{}, []]}
        #self.variables = {'__main_parent__': [{}, {}]}
        self.curr_type = ""

    def start(self):
        self._findall()
        print(self.variables)
        return self.content

    def _findall(self):

        lines = self.content.split('\r\n')
        no = -1
        for line in lines:
            no += 1
            if 'class ' in line:
                self.curr_type = 'class'
                self._parse_classes(line)
            elif 'def ' in line:
                self.curr_type = 'def'
                name, values = self._parse_function(line)
            elif '=' in line:
                self._parse_prop(line)

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
        self.variables[name] = [{'__init__': []}]
        self.curr_class = name

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
            self.functions_parent['__main_parent__'].append(name)
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

    def _parse_prop(self, line):
        splits = line.split('=')
        splits.pop()
        values = [v.replace(' ', '') for v in splits]
        class_name = ''
        if self.curr_class != '':
            class_name = self.curr_class + '.'
        else:
            class_name = '__main_parent__.'

        # If even one space exist
        if line[0] != ' ':
            self.var_parent['__main_parent__'].extend(values)
            self.variables['__main_parent__'][1].extend(values)

        elif self.curr_type == 'class':
            func_name = self.functions[-1]
            #class_name = ''
            name = class_name + func_name

            if name in self.var_parent:
                self.var_parent[name].extend(values)
            else:
                self.var_parent[name] = values

            self.variables[class_name[:-1]] = [{func_name: values}]

        elif self.curr_type == 'def':
            func_name = self.functions[-1]
            #class_name = ''
            name = class_name + func_name

            # Add variables declared as self to the init function
            # of a class instead
            bk_values = values
            for value in bk_values:
                if value.startswith('self.'):
                    if class_name != '':
                        par_name = class_name + '__init__'
                        if par_name in self.var_parent:
                            self.var_parent[par_name].extend([value])
                        else:
                            self.var_parent[par_name] = [value]

                        if func_name in self.variables[class_name[:-1]][0]:
                            self.variables[class_name[:-1]][0][func_name].extend([value])
                        else:
                            self.variables[class_name[:-1]][0][func_name] = [value]

                        values.remove(value)

            if name in self.var_parent:
                self.var_parent[name].extend(values)
            else:
                self.var_parent[name] = values

            if func_name in self.variables[class_name[:-1]][0]:
                self.variables[class_name[:-1]][0][func_name].extend(values)
            else:
                self.variables[class_name[:-1]][0][func_name] = values

