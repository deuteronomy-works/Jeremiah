# -*- coding: utf-8 -*-
import re
from vocabulary.py_user_defined import UserDefined
from vocabulary.types.base import base_types, base_types_dict, base_functions,\
base_func_dict

class Pyvoc():


    def __init__(self, conts):
        self.content = conts
        self.base_types = base_types
        self.base_types_dict = base_types_dict
        self.operand_types = ['+', '-', '=', '/', '*']
        self.replace_processes = ['base']
        self.lines = []
        self.r_lines_len = 0
        self.curr_type = ''
        self.curr_type_name = ''
        self.curr_index = 0

    def start(self):

        # Find user defined
        user_def = UserDefined(self.content)
        self.content = user_def.start()
        self._sanitise_quotes()

        self.main_parser(self.content)

        self.content = self.rebuild_content()
        print('32: ', self.content)

        print(self.content)

        return self.content

    def main_parser(self, content):

        lines = content.split('\r\n')
        self.r_lines_len = len(lines)

        no = -1
        for line in lines:
            no += 1
            line = self._start_replace_processes(line)
            print('45: ', line)
            # Underline unfound
            line = self._mark_unfound(line, no)
            print('49: ', line)

            self.lines.append(line)

    def rebuild_content(self):

        string = ''
        print('56: ', self.lines)
        for line in self.lines:
            print('58: ', line)
            string += line + '\r\n'

        return string

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
                content += '\u2029'
            elif each == '&nbsp;':
                content += '&nbsp;'
            elif each.endswith('\u2029</span>'):
                content += each
            else:
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
        self._replace_space_var(main_var, main_dict, line)

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


