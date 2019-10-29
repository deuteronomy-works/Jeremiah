# -*- coding: utf-8 -*-
import re

class Pyvoc():


    def __init__(self, conts):
        self.content = conts
        self.base_types = ['for']
        self.base_types_dict = {'for': "<span>for</span>"}
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
                print('line: ', list(line))
                if (no+1) < lines_len:
                    line = '\u2029'
                else:
                    line = ''
            else:
                print('linee: ' + line)
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
                word_splits_s[no] = "&nbsp;"
            else:
                stat = '<span style="color: red">' + word + '</span>'
                word_splits_s[no] = stat

        for each in word_splits_s:
            if each == '\u2029':
                print('l: ' + content)
                content += '\u2029'
                print('d: ' + content)
            elif each == '&nbsp;':
                content += '&nbsp;'
            elif each.endswith('\u2029</span>'):
                print('ld: ' + content)
                content += each
                print('dl: ' + content)
            else:
                print('kk: ' + each)
                content += each + "&nbsp;"

        self.content = content

    def _replace(self, var):

        if var == 'base':
            main_var = self.base_types
            main_dict = self.base_types_dict

        for x in main_var:
            if x in self.content:
                self.content = self.content.replace(x, main_dict[x])
