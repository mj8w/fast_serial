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

    def __init__(self, textEdit):
        self.textEdit = textEdit

        self.redColor = QColor(255, 0, 0)
        self.blueColor = QColor(0, 0, 255)
        self.blackColor = QColor(0, 0, 0)
        self.crlf = re.compile("(\r\n|\n\r|\r|\n)")
        self.mark_crlf = False
        self.mark_ctrl = False

    def append_black_text(self, text):
        self.textEdit.setTextColor(self.blackColor)
        self.textEdit.insertPlainText(text)

    def append_red_text(self, text):
        self.textEdit.setTextColor(self.redColor)
        self.textEdit.insertPlainText(text)

    def append_blue_text(self, text):
        self.textEdit.setTextColor(self.blueColor)
        self.textEdit.insertPlainText(text)

    def show_crlf(self, show = True):
        self.mark_crlf = show
        
    def show_ctrl(self, show = True):
        self.mark_ctrl = show

    def insert_input_text(self, text):

        if not self.mark_crlf and not self.mark_ctrl:
            self.append_black_text(text)
            return

        for char in text:
            
            if (char == "\n" or char == "\r"):
                if self.mark_crlf:
                    self.append_red_text(f"<{controlnames[ord(char)]}>")
                if char == "\n":
                    self.textEdit.insertPlainText(char)
            elif ord(char) < 32:
                if self.mark_ctrl:
                    self.append_red_text(f"<{controlnames[ord(char)]}>")
            elif ord(char) > 127:
                if self.mark_ctrl:
                    self.append_red_text(f"<{ord(char):02X}>")
            else:
                self.append_black_text(char)

    def write(self, text):
        for char in text:
            if (char == "\n" or char == "\r"):
                if self.mark_crlf:
                    self.append_red_text(f"<{controlnames[ord(char)]}>")
                if char == "\n":
                    self.textEdit.insertPlainText(char)
            elif ord(char) < 32:
                if self.mark_ctrl:
                    self.append_red_text(f"<{controlnames[ord(char)]}>")
            elif ord(char) > 127:
                if self.mark_ctrl:
                    self.append_red_text(f"<{ord(char):02X}>")
            else:
                self.append_blue_text(char)
