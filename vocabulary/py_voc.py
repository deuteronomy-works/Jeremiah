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
        for line in lines_splits:
            # Find if line contains just spaces
            founds = re.findall("[A-Za-z0-9`~!@#$%^&*\(\)\[\]-{}_=+/?<,.|>]*", line)
            found = str(founds).replace(', ', '').replace("'", "")
            if found == '[]':
                # Empty
                line = '\u2029'
            else:
                line += '\u2029'
            print('l: ', line)
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
                print('line break')
            elif word == "":
                word_splits_s[no] = "&nbsp;"
                print('hey')
            else:
                print(list(word))
                stat = '<span style="color: red">' + word + '</span>'
                word_splits_s[no] = stat

        for each in word_splits_s:
            if each == '\u2029':
                print('ll')
                content += '\u2029'
            elif each == '&nbsp;':
                content += '&nbsp;'
            else:
                content += each + "&nbsp;"

        self.content = content
        print(self.content)

    def _replace(self, var):

        if var == 'base':
            main_var = self.base_types
            main_dict = self.base_types_dict

        for x in main_var:
            if x in self.content:
                self.content = self.content.replace(x, main_dict[x])
        print(self.content)
