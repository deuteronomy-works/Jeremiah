# -*- coding: utf-8 -*-
import re
from vocabulary.py_user_defined import UserDefined
from vocabulary.types.base import base_types, base_types_dict, base_functions,\
base_func_dict
from vocabulary.types.user_defined import user_func_dict
from vocabulary.types.referenced import ref_prop_name

class Pyvoc():


    def __init__(self, conts):
        self.content = conts
        self.base_types = base_types
        self.base_types_dict = base_types_dict
        self.operand_types = ['+', '-', '=', '/', '*']
        self.replace_processes = ['base']
        self.lines = []
        self.r_lines_len = 0
        self.curr_type = None
        self.curr_class = None
        self.curr_func = None
        self.curr_par_indent = 0
        self.curr_type_name = ''
        self.curr_index = 0
        self.variables = {}

    def start(self):

        # Find user defined
        user_def = UserDefined(self.content)
        self.content = user_def.start()
        self.variables = user_def.variables
        print('variables: ', self.variables)
        self._sanitise_quotes()

        self.main_parser(self.content)

        self.content = self.rebuild_content()

        return self.content

    def finder(self, name, c_type=None, c_class=None, c_func=None, p_indent=0):
        # If it is by itself in the file
        if not c_type and not c_class and not c_func and not p_indent:

            if name in self.variables['__main_parent__'][1]:
                return name

            elif name in self.variables['___imports']:
                return name

            else:
                return None

        elif c_class:
            # If func name is set
            if c_func:
                print('func name set')
                if name in self.variables[c_class][0][c_func]:
                    print('found: ')
                    return name
                elif name in self.variables['___imports']:
                    return name
                elif name in self.variables['__main_parent__'][1]:
                    return name
            # if func name is not set
            else:
                print('func name unset')
                if name in self.variables[c_class][0]['__init__']:
                    print('found')
                    return name
                elif name in self.variables['___imports']:
                    return name
                elif name in self.variables['__main_parent__'][1]:
                    return name

        # if it is in a function in the file
        elif c_type == 'def':
            if name in self.variables['__main_parent__'][0][c_func]:
                return name
            elif name in self.varibles['__main_parent__'][1]:
                pass
            elif name in self.variables['___imports']:
                pass

        else:
            print('name: ', name)
        return

    def main_parser(self, content):

        lines = content.split('\r\n')
        self.r_lines_len = len(lines)

        no = -1
        for line in lines:
            no += 1
            self._parse_props(line)
            line = self._start_replace_processes(line)
            # mark prop names
            line = self._mark_prop_names(line)
            # mark function names
            line = self._mark_func_names(line)
            # Underline unfound
            line = self._mark_unfound(line, no)

            self.lines.append(line)

    def rebuild_content(self):

        string = ''
        for line in self.lines:
            string += line + '\r\n'

        return string

    def _mark_func_names(self, line):

        if 'def</span> ' in line:
            name = line.split('def</span> ')[1].split('(')[0]
            html = user_func_dict['bar'].format(name)
            line = line.replace(name+'(', html)

        return line

    def _mark_prop_names(self, line):
        sp_splits = line.split(' ')
        main_splits = [b for b in sp_splits if b != '']
        print(main_splits)
        
        if len(main_splits) == 1 and '(' not in main_splits[0]:
            found = self.finder(main_splits[0], c_type=self.curr_type, c_class=self.curr_class, c_func=self.curr_func)
            if found:
                print('found dear: ', found)
        return line

    def _parse_props(self, line):

        sp_splits = line.split(' ')
        main_splits = [b for b in sp_splits if b != '']

        # find class
        if 'class ' in line:
            self.curr_type = 'class'
            splits = line.split('class ')
            a_split = splits[0]

            # if all are spaces then its an indent
            if a_split == ' '*len(a_split):
                indent = len(a_split)

            b_split = splits[1]
            if '(' in b_split:
                name = b_split.split('(')[0]
            else:
                name = b_split.split(':')[0].replace(' ', '')

            self.curr_class, self.curr_par_indent = name, indent

        # find def
        if 'def' in main_splits:
            self.curr_type = 'def'
            splits = line.split('def ')
            a_split = splits[0]

            # if all are spaces then its an indent
            if a_split == ' '*len(a_split):
                indent = len(a_split)

            b_split = splits[1]
            if '(' in b_split:
                name = b_split.split('(')[0]
            else:
                name = b_split(':')[0].replace(' ', '')

            self.curr_func, self.curr_par_indent = name, indent

        # it is the only thing on the line
        if len(main_splits) == 1:
            if '(' in main_splits[0]:
                pass
            else:
                pass

    def _start_replace_processes(self, line):

        # Replaces
        for var in self.replace_processes:
            line = self._replace(var, line)
        return line

    def _mark_unfound(self, line, no):

        word_splits = []
        # Find if line contains just spaces
        founds = re.findall("[A-Za-z0-9`~!@#$%^&*\(\)\[\]-{}_=+/?<,.|>]*", line)
        found = str(founds).replace(', ', '').replace("'", "")
        if found == '[]':
            # Empty
            if (no+1) < self.r_lines_len:
                line = '\u2029'
            else:
                line = ''
        else:
            line += '\u2029'
        splits = line.split(" ")
        word_splits.extend(splits)
        word_splits_s = word_splits

        no = -1
        content = ""

        # Start with the Marking of the unfound
        for word in word_splits:
            no += 1
            if word.startswith('<span>'):
                pass
            elif word == "\u2029":
                word_splits_s[no] = '\u2029'
            elif word == "":
                # A space unless its the last entry
                if (no + 1) == len(word_splits_s):
                    # If it is the last entry probably its not a space
                    word_splits_s.pop()
                else:
                    word_splits_s[no] = "&nbsp;"
            else:
                stat = '<span style="color: red">' + word + '</span>'
                word_splits_s[no] = stat

        # recompose back into a line
        for each in word_splits_s:
            if each == '\u2029':
                # a space then a break
                content += '\u2029'

            elif each == '&nbsp;':
                content += '&nbsp;'

            elif each.endswith('\u2029</span>'):
                content += each

            elif each.endswith('\u2029'):
                # a break of line after a modification
                content += each
            else:
                # this should only perhaps for the middle
                content += each + "&nbsp;"

        return content
        self.content = content

    def _replace(self, var, line):

        if var == 'base':
            main_var = self.base_types
            main_dict = self.base_types_dict
            main_func = base_functions
            main_func_dict = base_func_dict

        # variable replacement
        line = self._replace_space_var(main_var, main_dict, line)

        # function replacement
        for y in main_func:
            if y in line:
                line = line.replace(y, main_func_dict[y])

        return line

    def _replace_space_var(self, var, var_dict, line):
        splits = line.split(' ')

        for x in var:
            if x in splits:
                ind = splits.index(x)
                splits[ind] = var_dict[x]

        # Add all to string
        string = ""
        for a in splits:
            string += a + " "

        # And back to contents
        line = string[:-1]
        return line

    def _sanitise_quotes(self):
        lines = self.content.split('\r\n')
        cwq = ""

        for line in lines:
            if '"' in line:
                cwq = '"'
            elif "'" in line:
                cwq = "'"
            else: continue

            pat = cwq + '.*?' + cwq
            matches = re.findall(pat, line)
            if matches:
                for match in matches:
                    fixed = match.replace(" ", "&nbsp;")
                    self.content = self.content.replace(match, fixed)


