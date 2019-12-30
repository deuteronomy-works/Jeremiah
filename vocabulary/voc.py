# -*- coding: utf-8 -*-
from vocabulary import py_voc

class Vocabulary():


    def __init__(self, conts):
        self.contents = conts

    def start(self):
        print('conts: ', self.contents, '\n')
        py_voca = py_voc.Pyvoc(self.contents)
        py_checked = py_voca.start()
        
        print('\n\n********************')
        print(py_checked)
        print('\n\n********************')

        return py_checked
