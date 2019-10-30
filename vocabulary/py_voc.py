# -*- coding: utf-8 -*-
import re
from vocabulary.types.base import base_types, base_types_dict, base_functions,\
base_func_dict

class Pyvoc():


    def __init__(self, conts):
        self.content = conts
        self.base_types = base_types
        self.base_types_dict = base_types_dict
        self.replace_processes = ['base']

    def start(self):

        # Replaces
        for var in self.replace_processes:
            self._replace(var)

        # Underline unfound
        self._mark_unfound()

        return self.content

    def _mark_unfound(self):

        word_splits = []
        lines_splits = self.content.split('\r\n')
        lines_len = len(lines_splits)
        no = -1
        for line in lines_splits:
            no += 1
            # Find if line contains just spaces
            founds = re.findall("[A-Za-z0-9`~!@#$%^&*\(\)\[\]-{}_=+/?<,.|>]*", line)
            found = str(founds).replace(', ', '').replace("'", "")
            if found == '[]':
                # Empty
                if (no+1) < lines_len:
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

        for each in word_splits_s:
            if each == '\u2029':
                content += '\u2029'
            elif each == '&nbsp;':
                content += '&nbsp;'
            elif each.endswith('\u2029</span>'):
                content += each
            else:
                content += each + "&nbsp;"

        self.content = content

    def _replace(self, var):

        if var == 'base':
            main_var = self.base_types
            main_dict = self.base_types_dict
            main_func = base_functions
            main_func_dict = base_func_dict

        # variable replacement
        for x in main_var:
            if x in self.content:
                self.content = self.content.replace(x, main_dict[x])

        # function replacement
        for y in main_func:
            if y in self.content:
                self.content = self.content.replace(y, main_func_dict[y])
