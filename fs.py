# -*- coding: utf-8 -*-
import threading
import re
from time import sleep

class Fs():


    """
    """


    content_replaces = ["\u2029", "&nbsp;"]
    cont_repls = {"\u2029": "\r\n", "&nbsp;": " "}
    raw_content_replaces = ["\r\n", " "]
    raw_cont_repls = {"\r\n": "\u2029", " ": "&nbsp;"}

    def return_completed(self, kind):
        self.completedProcess.emit(kind)

    def return_contents(self, contents):
        self.openedFile.emit(contents)

    def _clean_filename(self, filename):
        clean = filename.replace("file:///", "")
        return clean

    def _clean_content(self, contents):
        for repl in self.content_replaces:
            if repl in contents:
                contents = contents.replace(repl, self.cont_repls[repl])
        return contents

    def _clean_raw_content(self, raw):
        for repl in self.raw_content_replaces:
            if repl in raw:
                raw = raw.replace(repl, self.raw_cont_repls[repl])
        return raw

    def _save_file(self, file_name, contents):
        filename =  self._clean_filename(file_name)
        cleaned = self._clean_content(contents)
        data = bytes(cleaned, 'utf-8')
        with open(filename, 'wb') as f:
            f.write(data)
        self.return_completed("save")

    def _read_file(self, file):

        filename = self._clean_filename(file)
        with open(filename, 'rb') as f:
            data = f.read()
        cleaned = self._clean_raw_content(str(data, 'utf-8'))
        self.return_contents(cleaned)

