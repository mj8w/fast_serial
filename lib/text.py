"""
Copyright 2021 Micheal Wilson
Fast_serial project founded by Micheal Wilson
"""

import re
from PyQt5.QtGui import QColor

from lib.project import logset
debug, info, warn, err = logset('app')

class RichText():

    def __init__(self, textEdit):
        self.textEdit = textEdit

        self.redColor = QColor(255, 0, 0)
        self.blueColor = QColor(0, 0, 255)
        self.blackColor = QColor(0, 0, 0)
        self.crlf = re.compile("(\r\n|\n\r|\r|\n)")

    def append_black_text(self, text):
        self.textEdit.setTextColor(self.blackColor)
        self.textEdit.insertPlainText(text)

    def append_red_text(self, text):
        self.textEdit.setTextColor(self.redColor)
        self.textEdit.insertPlainText(text)

    def append_blue_text(self, text):
        self.textEdit.setTextColor(self.blueColor)
        self.textEdit.insertPlainText(text)

    def insert_input_text(self, text):

        results = self.crlf.split(text)

        color = 0
        for s in results:
            if color % 2:
                if s == "\n":
                    s = "<LF>\n"
                if s == "\r":
                    s = "<CR>\n"
                if s == "\r\n":
                    s = "<CR><LF>\n"
                if s == "\n\r":
                    s = "<LF><CR>\n"
                self.append_red_text(s)
            else:
                self.append_black_text(s)
            color += 1

    def insert_output_text(self, text):

        results = self.crlf.split(text)

        color = 0
        for s in results:
            if color % 2:
                if s == "\n\r":
                    s = "<LF><CR>\n"
                if s == "\r\n":
                    s = "<CR><LF>\n"
                if s == "\n":
                    s = "<LF>\n"
                if s == "\r":
                    s = "<CR>\n"
                self.append_red_text(s)
            else:
                self.append_blue_text(s)
            color += 1
