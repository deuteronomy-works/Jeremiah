# -*- coding: utf-8 -*-
from vocabulary import py_voc

class Vocabulary():


    def __init__(self, conts):
        self.contents = conts

    def start(self):
        py_voca = py_voc.Pyvoc(self.contents)
        py_checked = py_voca.start()

        return py_checked
