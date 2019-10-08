# -*- coding: utf-8 -*-
import threading
import re
from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from editor import Editor
from fs import Fs

class Connector(QObject, Editor, Fs):


    """
    """


    def __init__(self):
        QObject.__init__(self)
        self.count = [[]]
        self.tab_width = 0
        self.tab_worthy = ['{']
        self.values = {"new_line": "\u2029", 'tab': "&nbsp;&nbsp;&nbsp;&nbsp;"}
        self.curr_word = ""
        self.end_new_word = False
        self.lines = []

    send_base_html = pyqtSignal(str, arguments=["startUp"])
    space_return = pyqtSignal(str, arguments=["return_space"])
    enter_return = pyqtSignal(str, arguments=["return_enter"])
    char_return = pyqtSignal(str, arguments=["return_char"])
    backspace_return = pyqtSignal(list, arguments=["return_backspace"])
    backtab_return = pyqtSignal(list, arguments=["return_backtab"])
    sendCoOrd = pyqtSignal(list, arguments=["returnCoOrd"])
    wakeUp = pyqtSignal(str, arguments=["_pressed_mouse"])
    completedProcess = pyqtSignal(str, arguments=["return_completed"])

    @pyqtSlot(str, int)
    def pressed_enter(self, full_text, cur_pos):
        f_thread = threading.Thread(target=self._pressed_enter,
                                    args=[full_text,cur_pos])
        f_thread.daemon = True
        f_thread.start()

    @pyqtSlot(str, str, str, int, list)
    def pressed_space(self, full_text, char, line, cur_pos, breaks):
        f_thread = threading.Thread(target=self._pressed_space,
                                    args=[full_text, char, line,
                                          cur_pos, breaks])
        f_thread.daemon = True
        f_thread.start()

    @pyqtSlot(str, int)
    def pressed_backspace(self, some_text, cur_pos):
        print('pure backspace: ', cur_pos)
        p_thread = threading.Thread(target=self._pressed_backspace,
                                    args=[some_text, cur_pos])
        p_thread.daemon = True
        p_thread.start()

    @pyqtSlot(int)
    def pressed_mouse(self, cur_pos):
        m_thread = threading.Thread(target=self._pressed_mouse,
                                    args=[cur_pos])
        m_thread.daemon = True
        m_thread.start()

    @pyqtSlot(str, str, str, int, list)
    def pressed_char(self, full_text, char, line, cur_pos, breaks):
        f_thread = threading.Thread(target=self._pressed_char,
                                    args=[full_text, char, line,
                                          cur_pos, breaks])
        f_thread.daemon = True
        f_thread.start()

    @pyqtSlot(str, int, bool)
    def pressed_tab(self, some_text, cur_pos, pure):
        p_thread = threading.Thread(target=self._pressed_tab,
                                    args=[some_text, cur_pos, pure])
        p_thread.daemon = True
        p_thread.start()

    @pyqtSlot(str)
    def read_file(self, filename):
        f_thread = threading.Thread(target=self._read_file,
                                    args=[filename])
        f_thread.daemon = True
        f_thread.start()

    @pyqtSlot(str, str)
    def save_file(self, filename, full_text):
        f_thread = threading.Thread(target=self._save_file,
                                    args=[filename, full_text])
        f_thread.daemon = True
        f_thread.start()

    @pyqtSlot(str, str, int)
    def send_text(self, full_text, line, cur_pos):
        pass

    @pyqtSlot()
    def startUp(self):
        with open('base_styles.html', mode='r', encoding='ascii') as base_html:
            data = base_html.read()
        self.send_base_html.emit(data)

    @pyqtSlot(int)
    def wake_me_up(self, cur_pos):
        m_thread = threading.Thread(target=self._wake_me_up,
                                    args=[cur_pos])
        m_thread.daemon = True
        m_thread.start()

    @pyqtSlot(str, int, list)
    def wake_enter_up(self, text, cur_pos, breaks):
        m_thread = threading.Thread(target=self._wake_enter_up,
                                    args=[text, cur_pos, breaks])
        m_thread.daemon = True
        m_thread.start()

    


