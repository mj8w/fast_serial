"""
Copyright 2021 Micheal Wilson
Fast_serial project founded by Micheal Wilson
"""

import re
from PyQt5.QtGui import QColor
from lib.project import logset

debug, info, warn, err = logset('app')

# from curses.ascii, which won't import for some reason
controlnames = [
"NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL",
"BS", "HT", "LF", "VT", "FF", "CR", "SO", "SI",
"DLE", "DC1", "DC2", "DC3", "DC4", "NAK", "SYN", "ETB",
"CAN", "EM", "SUB", "ESC", "FS", "GS", "RS", "US",
"SP"
]

class RichText():

    def __init__(self, textEdit, mark_crlf = False):
        self.textEdit = textEdit

        self.redColor = QColor(255, 0, 0)
        self.blueColor = QColor(0, 0, 255)
        self.blackColor = QColor(0, 0, 0)
        self.crlf = re.compile("(\r\n|\n\r|\r|\n)")
        self.mark_crlf = mark_crlf

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

        if not self.mark_crlf:
            self.append_black_text(text)
            return

        for char in text:
            if ord(char) < 32:
                mark = f"<{controlnames[ord(char)]}>"
                self.append_red_text(mark)
                if char == "\n":
                    self.textEdit.insertPlainText(char)

            elif ord(char) > 127:
                mark = f"<{ord(char):02X}>"
                self.append_red_text(mark)
                if char == "\n":
                    self.textEdit.insertPlainText(char)
            else:
                self.append_black_text(char)

    def write(self, text):

        if not self.mark_crlf:
            self.append_blue_text(text)
            return

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
