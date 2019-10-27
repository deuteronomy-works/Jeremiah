# -*- coding: utf-8 -*-

class Pyvoc():


    def __init__(self, conts):
        self.content = conts
        self.replace_processes = {self.base_types: self.base_types_dict}
        self.base_types = ['for']
        self.base_types_dict = {'for': "<span>for</span>"}

    def start(self):

        # Replaces
        for var in self.replace_processes:
            self._replace(var, self.replace_processes[var])

        # Underline unfound
        self._mark_unfound()


    def _replace(self, main_var, main_dict):

        for x in main_var:
            if x in self.content:
                self.content = self.content.replace(x, main_dict[x])
        print(self.content)
