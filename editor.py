# -*- coding: utf-8 -*-
import threading
import re
from time import sleep

class Editor():


    def return_space(self, val):
        self.space_return.emit(val)

    def returnCoOrd(self, co_ord):
        self.sendCoOrd.emit(co_ord)

    def return_char(self, val):
        self.char_return.emit(val)

    def return_enter(self, val):
        self.enter_return.emit(val)

    def return_backspace(self, pos):
        self.backspace_return.emit(pos)

    def return_backtab(self, pos):
        self.backtab_return.emit(pos)

    def _pressed_space(self, full_text, char, line, cur_pos, breaks):
        self._handle_text(full_text, breaks)
        self.co_ord(cur_pos)

    def _pressed_enter(self, full_text, cur_pos):

        # Calculate tabs
        query = self.values["new_line"] + self._tabs(full_text[-1])
        stat = query
        self.return_enter(stat)

    def _pressed_mouse(self, cur_pos):
        sleep(0.2)
        self.wakeUp.emit("")

    def _pressed_char(self, text, char, line, cur_pos, breaks):
        self.counter(text, breaks)
        self.co_ord(cur_pos)
        # self._check_spelling(char)
        # self._handle_text(full_text)

    def _pressed_tab(self, some_text, cur_pos, pure):
        if pure:
            # add tabs
            tabs = self._tabs(some_text[-1])
            self.return_enter(tabs)
        else:
            # delete tabs
            self._pressed_backtab(some_text, cur_pos)

    def _pressed_backspace(self, some_text, cur_pos):

        start = -1
        end = -1
        if some_text[-4:] == '\xa0' * 4:
            # tab delete
            if self.tab_width > 0:
                self.tab_width -= 1
                start = cur_pos - 4
                end = cur_pos - 1
            else:
                start = cur_pos - 4
                end = cur_pos - 1
        else:
            # normal delete
            start = cur_pos - 1
            end = cur_pos - 1
        self.return_backspace([start, end])

    def _pressed_backtab(self, some_text, cur_pos):
        if some_text[-4:] == '\xa0' * 4:
            # tab delete
            if self.tab_width > 0:
                self.tab_width -= 1
                start = cur_pos - 4
                end = cur_pos
            else:
                start = cur_pos - 4
                end = cur_pos
            self.return_backtab([start, end])

    def co_ord(self, cur_pos):
        c_thread = threading.Thread(target=self._co_ord,
                                    args=[cur_pos])
        c_thread.daemon = True
        c_thread.start()

    def counter(self, text, breaks):
        c_thread = threading.Thread(target=self._counter,
                                    args=[text, breaks])
        c_thread.daemon = True
        c_thread.start()

    def _break_lots(self, text):
        pass

    def _check_spelling(self, word):
        pass

    def _co_ord(self, cur_pos):
        # change cursor position
        cur_pos += 1
        ln_no = 0
        for line in self.count:
            if cur_pos in line:
                col = line.index(cur_pos) + 1
                self.returnCoOrd([ln_no, col])
                ln_no += 1
                break
            else:
                pass
            ln_no += 1

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

    def _editor_count(self, text, cur_pos):
        breaks = []
        self._handle_text(text, breaks)
        self.co_ord(cur_pos)

    def _handle_text(self, text, breaks):
        self.counter(text, breaks)

    def _send_text(self, full_text, line, cur_pos):
        pass

    def _tabs(self, last_char):
        if last_char in self.tab_worthy:
            self.tab_width += 1
        return self.values['tab'] * self.tab_width

    def _wake_enter_up(self, text, cur_pos, breaks):
        self._handle_text(text, breaks)
        self.co_ord(cur_pos)

    def _wake_me_up(self, cur_pos):
        self.co_ord(cur_pos)
