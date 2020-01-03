# -*- coding: utf-8 -*-
import re
from vocabulary.py_user_defined import UserDefined
from vocabulary.types.base import base_types, base_types_dict, base_functions,\
base_func_dict
from vocabulary.types.user_defined import user_func_dict
from vocabulary.types.referenced import ref_prop_name
from vocabulary.misc.misc import add_splitter
from vocabulary.misc.misc_py import SplitParenthesis

class Pyvoc():


    def __init__(self, conts):
        self.content = conts
        self.base_types = base_types
        self.base_types_dict = base_types_dict
        self.operand_types = ['+', '-', '=', '/', '*']
        self.escape_parentesis = ['[', ']', '{', '}', '(', ')']
        self.space_char = "&nbsp;"
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
                if name in self.variables[c_class][0][c_func]:
                    return name
                # prop can be found inside the __init__
                elif name in self.variables[c_class][0]['__init__']:
                    return name
                # search the general imports
                elif name in self.variables['___imports']:
                    return name
                elif name in self.variables['__main_parent__'][1]:
                    return name
            # if func name is not set
            else:
                if name in self.variables[c_class][0]['__init__']:
                    return name
                elif name in self.variables['___imports']:
                    return name
                elif name in self.variables['__main_parent__'][1]:
                    return name

        # if it is in a function in the file
        elif c_type == 'def':
            if name in self.variables['__main_parent__'][0][c_func]:
                return name
            elif name in self.variables['__main_parent__'][1]:
                return name
            elif name in self.variables['___imports']:
                return name

        else:
            print('name: ', name)
        return

    def main_parser(self, content):

        lines = content.split('\r\n')
        self.r_lines_len = len(lines)

        no = -1
        for line in lines:
            no += 1
            # Replace the newline character with its unicode character
            if line == '':
                line = '\u2029'
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
            if type(line) == type(''):
                string += line + ''
        return string

    def _mark_func_names(self, line):

        if not line:
            return line

        if 'def</span> ' in line:
            name = line.split('def</span> ')[1].split('(')[0]
            html = user_func_dict['bar'].format(name)
            line = line.replace(name+'(', html)

        return line

    def _mark_prop_names(self, line):
        # mark property that are been referenced
        # narrow down to certain instances

        if not line:
            return line

        if 'class</span>' in line or 'def</span>' in line or ': ' in line:
            pass
        else:
            sp_splits = line.split('=')
            print('sp: ', sp_splits)

            # find those used in brackets
            new_splits = self._find_props_in_brac(sp_splits)
            a = new_splits[-1].split(' ')
            # remove empty space chars and commas
            b = [pick.replace(',', '') for pick in a if pick != '' and pick != ',']
            # remove strings props
            c = [pick for pick in b if "'" not in pick and '"' not in pick]
            d = [pick.replace('(', '').replace(')', '') for pick in c]
            e = [pick.replace('{', '').replace('}', '') for pick in d]
            f = [pick.replace('[', '').replace(']', '') for pick in e]
            g = [pick for pick in f if not pick.startswith('<span>')]
            h = [pick for pick in g if pick not in ['-', '+', '/', '*']]
            i = [pick for pick in h if pick not in ['(', ')', '[', ']', '{', '}']]
            main_splits = i
            print('main splits: ', main_splits)

            # IHandle all in a loop
            for prop in main_splits:
                found = self.finder(prop, c_type=self.curr_type, c_class=self.curr_class, c_func=self.curr_func)
                if found:
                    # mark
                    line = line.replace(found, ref_prop_name['baz'].format(found))

        return line

    def _find_props_in_brac(self, raw_list):

        """
        Gets the property names out of brackets
        and adds them to the property list
        """

        final_list = []
        data = raw_list[-1]

        if '(' in data and ')' in data:
            content = data.split('(')[-1].split(')')[0] # it contains 1+
            final_list.append(content)
        else:
            return raw_list

        return final_list

    def _parse_props(self, line):

        sp_splits = line.split(' ')
        main_splits = [b for b in sp_splits if b != '']

        # find class
        if 'class ' in line:
            self.curr_type = 'class'
            splits = line.split('class ')
            a_split = splits[0]

            indent = 0
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
        if not line:
            return line

        for var in self.replace_processes:
            line = self._replace(var, line)
        return line

    def _mark_unfound(self, line, no):

        if not line:
            return line
        left_ahead = ""
        if '=' in line and not '"="' in line or "'='" in line:
            junk_s = line.split('=')
            junky = junk_s[:-1]
            ww = ''
            for x in junky:
                ww += x + '='
            left_ahead = ww[:-1] + '='
            line = junk_s[-1]

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
        splits = add_splitter(splits, self.space_char)
        print('what is this: ', splits)
        sParen = SplitParenthesis(splits)
        splits = sParen.start()
        #splits = self._add_list_span_without_spaces(splits)
        print('now what is this: ', splits)
        word_splits.extend(splits)
        word_splits_s = word_splits

        no = -1
        content = ""

        # Start with the Marking of the unfound
        for word in word_splits:
            no += 1
            if word.startswith('<span>'):
                pass
            elif self._is_string(word):
                word_splits_s[no] = word
            elif word == "\u2029":
                word_splits_s[no] = '\u2029'
            elif word == self.space_char:
                # A space unless its the last entry
                word_splits_s[no] = self.space_char
            elif word == "":
                if (no + 1) == len(word_splits_s):
                    # If it is the last entry probably its not a space
                    word_splits_s.pop()
            elif word in self.escape_parentesis or word in self.operand_types:
                word_splits_s[no] = word
            else:
                stat = '<span style="color: red">' + word + '</span>'
                word_splits_s[no] = stat

        # recompose back into a line
        for each in word_splits_s:
            if each == '\u2029':
                # a space then a break
                content += '\u2029'

            elif each == '&nbsp;':
                content += self.space_char

            elif each.endswith('\u2029</span>'):
                content += each.replace('\u2029</span>', '</span>\u2029')

            elif each.endswith('\u2029'):
                # a break of line after a modification
                content += each
            else:
                # this should only perhaps for the middle
                content += each

        # Add left ahead back to line
        content = left_ahead + content
        self.content = content
        return content

    def _is_string(self, word):
        if word:
            if word[0] == "'" or word[0] == '"':
                return True

        return False

    def _add_list_span_without_spaces(self, old_list):
        lister = old_list
        for l in old_list:
            if '</span>' in l:
                lister.remove(l)
                j = l.split('</span>')
                print('non: ', j)
                nn = [n + '</span>' for n in j if n.startswith('<span')]
                print('n: ', nn)
                mm = [m for m in j if not m.startswith('<span')]
                print('mm: ', mm)
                nn.extend(mm)
                lister.extend(nn)
                

        print('here is lister: ', lister)
        return lister

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


