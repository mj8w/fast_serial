
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.Qt import Qt

from lib.project import logset
debug, info, warn, err = logset('app')

from ui.ui_setup import Ui_SetupDialog
from serial.tools import list_ports

class Message(QMessageBox):
    """ Message dialog shown when some tests are disabled. """

    def __init__(self, message):
        super(Message, self).__init__()

        self.setWindowTitle("Failed to open")
        self.setIcon(QMessageBox.Information)
        self.setStandardButtons(QMessageBox.Ok)
        message.replace(" ", "&nbsp;")
        self.setText(message)
        self.setTextFormat(Qt.RichText)
        self.setInformativeText("Press OK to continue")
