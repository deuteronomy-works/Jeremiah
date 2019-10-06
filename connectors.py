# -*- coding: utf-8 -*-
import threading
import re
from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class Connector(QObject):


    """
    """


    def __init__(self):
        QObject.__init__(self)
        self.count = [[]]
        self.curr_word = ""
        self.end_new_word = False
        self.lines = []

    send_base_html = pyqtSignal(str, arguments=["startUp"])
    space_return = pyqtSignal(str, arguments=["return_space"])
    enter_return = pyqtSignal(str, arguments=["return_enter"])
    char_return = pyqtSignal(str, arguments=["return_char"])
    sendCoOrd = pyqtSignal(list, arguments=["returnCoOrd"])
    wakeUp = pyqtSignal(str, arguments=["_pressed_mouse"])

    @pyqtSlot()
    def startUp(self):
        with open('base_styles.html', mode='r', encoding='ascii') as base_html:
            data = base_html.read()
        self.send_base_html.emit(data)

    def counter(self, text, breaks):
        c_thread = threading.Thread(target=self._counter,
                                    args=[text, breaks])
        c_thread.daemon = True
        c_thread.start()

    def _counter(self, text, breaks):
        if "\u2029" in text:
            splits = text.split("\u2029")
        else:
            splits = [text]
        self.count = [[]]
        line_no = 0
        char_no = 0
        for line in splits:
            line_no += 1
            self.count.append([])
            for char in line:
                char_no += 1
                self.count[line_no].append(char_no)
            else:
                char_no += 1
                self.count[line_no].append(char_no)

    def returnCoOrd(self, co_ord):
        self.sendCoOrd.emit(co_ord)

    def co_ord(self, cur_pos):
        c_thread = threading.Thread(target=self._co_ord,
                                    args=[cur_pos])
        c_thread.daemon = True
        c_thread.start()

    def _co_ord(self, cur_pos):
        # change cursor position
        cur_pos += 1
        ln_no = 0
        for line in self.count:
            # print(line)
            if cur_pos in line:
                col = line.index(cur_pos) + 1
                self.returnCoOrd([ln_no, col])
                ln_no += 1
                break
            else:
                pass
            ln_no += 1

    def _handle_text(self, text, breaks):
        self.counter(text, breaks)

    def _break_lots(self, text):
        pass

    @pyqtSlot(str, str, int)
    def send_text(self, full_text, line, cur_pos):
        pass

    def _send_text(self, full_text, line, cur_pos):
        pass

    @pyqtSlot(str, str, str, int, list)
    def pressed_space(self, full_text, char, line, cur_pos, breaks):
        f_thread = threading.Thread(target=self._pressed_space, args=[full_text,
                                                                      char,
                                                                 line,
                                                                 cur_pos,
                                                                 breaks])
        f_thread.daemon = True
        f_thread.start()

    def _pressed_space(self, full_text, char, line, cur_pos, breaks):
        self._handle_text(full_text, breaks)
        self.co_ord(cur_pos)

    def return_space(self, val):
        self.space_return.emit(val)

    @pyqtSlot(str, str, str, int, list)
    def pressed_enter(self, full_text, char, line, cur_pos, breaks):
        f_thread = threading.Thread(target=self._pressed_enter, args=[full_text,
                                                                      char,
                                                                 line,
                                                                 cur_pos,
                                                                 breaks])
        f_thread.daemon = True
        f_thread.start()

    def _pressed_enter(self, full_text, char, line, cur_pos, breaks):
        self._handle_text(full_text, breaks)

    def return_enter(self, val):
        self.enter_return.emit(val)

    @pyqtSlot(int)
    def pressed_mouse(self, cur_pos):
        m_thread = threading.Thread(target=self._pressed_mouse,
                                    args=[cur_pos])
        m_thread.daemon = True
        m_thread.start()

    def _pressed_mouse(self, cur_pos):
        sleep(0.2)
        self.wakeUp.emit("")

    @pyqtSlot(int)
    def wake_me_up(self, cur_pos):
        m_thread = threading.Thread(target=self._wake_me_up,
                                    args=[cur_pos])
        m_thread.daemon = True
        m_thread.start()

    def _wake_me_up(self, cur_pos):
        self.co_ord(cur_pos)


    @pyqtSlot(str, str, str, int, list)
    def pressed_char(self, full_text, char, line, cur_pos, breaks):
        f_thread = threading.Thread(target=self._pressed_char, args=[full_text,
                                                                     char,
                                                                 line,
                                                                 cur_pos,
                                                                 breaks])
        f_thread.daemon = True
        f_thread.start()

    def _pressed_char(self, text, char, line, cur_pos, breaks):
        self.counter(text, breaks)
        self.co_ord(cur_pos)
        # self._check_spelling(char)
        # self._handle_text(full_text)

    def return_char(self, val):
        self.char_return.emit(val)

    def _check_spelling(self, word):
        pass
