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

    def insert_input_text(self, text):

        self.textEdit.setTextColor(self.blackColor)

        results = self.crlf.split(text)

        color = 0
        for s in results:
            if color % 2:
                self.textEdit.setTextColor(self.redColor)
                if s == "\n":
                    s = "<LF>\n"
                if s == "\r":
                    s = "<CR>\n"
            else:
                self.textEdit.setTextColor(self.blackColor)
            color += 1

            self.textEdit.insertPlainText(s)

    def insert_output_text(self, text):

        self.textEdit.setTextColor(self.blueColor)
        results = self.crlf.split(text)

        color = 0
        for s in results:
            if color % 2:
                self.textEdit.setTextColor(self.redColor)
                if s == "\n\r":
                    s = "<LF><CR>\n"
                if s == "\r\n":
                    s = "<CR><LF>\n"
                if s == "\n":
                    s = "<LF>\n"
                if s == "\r":
                    s = "<CR>\n"
            else:
                self.textEdit.setTextColor(self.blueColor)
            color += 1

            self.textEdit.insertPlainText(s)
