# -*- coding: utf-8 -*-
import re
from vocabulary.misc.misc import escape_user_strings, put_back_user_strings, escape_user_comments, put_back_user_comments


class UserDefined():

    def __init__(self, content):
        self.indent = 4
        self.par_indent = 0
        self.content = content
        self.classes_parent = {} # Store indents of classes and their names
        self.curr_class = ''
        self.functions_parent = {'__main_parent__': []}
        self.functions = []
        self.var_parent = {'__main_parent__': []}
        self.variables = {'__main_parent__': [{}, []], '___imports': [{}, []]}
        #self.variables = {'__main_parent__': [{}, {}]}
        self.curr_type = ""

    def start(self):
        self._findall()
        return self.content

    def _findall(self):

        lines = self.content.split('\r\n')
        no = -1
        for line in lines:
            sngl, dobl, line = escape_user_strings(line)
            sgnl_com, dobl_com, line = escape_user_comments(line)
            no += 1
            if re.findall(r'\bimport\b', line):
                self._parse_imports(line)
            if re.findall(r'\bclass\b', line):
                self.curr_type = 'class'
                self._parse_classes(line)
            elif re.findall(r'\bdef\b', line):
                self.curr_type = 'def'
                name, values = self._parse_function(line)
            elif '=' in line:
                self._parse_prop(line)
            line = put_back_user_comments(sgnl_com, dobl_com, line)
            line = put_back_user_strings(sngl, dobl, line)

    def _parse_classes(self, line):
        print('class line: ', line)
        splits = line.split('class ')
        print('splits: ', splits)
        spaces = splits[0]
        remain = splits[1]
        if '(' in remain:
            name = remain.split('(')[0]
        elif ' :' in remain:
            name = remain.split(' :')[0]
        else:
            name = remain.split(':')[0]

        indent = len(spaces)
        # if this is outside the parent
        if indent <= self.par_indent:
            self.par_indent = indent
            # remove the nested items
            self.functions.append("")
            self.curr_type = 'class'

        # For classes nesting sake
        # {
        if indent in self.classes_parent:
            self.classes_parent[indent].append(name)
        else:
            self.classes_parent[indent] = [name]
        # }

        self.functions_parent[name] = ['__init__']
        self.variables.update({name: [{'__init__': []}]})
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
            self.variables['__main_parent__'][0].update({name: []})
            self.functions.append(name)
        else:
            ind = indent - self.indent
            if ind in self.classes_parent:
                class_name = self.classes_parent[ind][-1]
                if class_name in self.functions_parent:
                    self.functions_parent[class_name].append(name)
                    self.functions.append(name)
                    # Add the function name to the class dict
                    if name not in self.variables[class_name][0]:
                        self.variables[class_name][0].update({name: []})
                else:
                    self.functions_parent[class_name] = [name]
                    self.variables[class_name] = [{name: []}]
                    self.functions.append(name)

        return name, values

    def _parse_imports(self, line):

        splits = line.split('import ')
        remain = splits[1]
        if ', ' in remain:
            values = remain.split(', ')
        elif ',' in remain:
            values = remain.split(',')
        else:
            values = [remain]

        self.variables['___imports'][1].extend(values)

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

        else:

            if self.curr_type == 'class':
    
                func_name = self.functions[-1]
                # If there is no function yet defined in the class
                if func_name == '':
                    func_name = '__init__'
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
                self.variables[class_name[:-1]][0][func_name] = [values]

