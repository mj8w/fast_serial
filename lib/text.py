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
        self.append_black_text(text)
        return

    def write(self, text):
        self.append_blue_text(text)
