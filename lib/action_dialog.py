from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

from ui.ui_action_dialog import Ui_Dialog
from lib.project import logset
debug, info, warn, err = logset('app')

class ActionDialog(QDialog):

    action = ""
    name = ""

    def __init__(self, parent):
        super(ActionDialog, self).__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

    def button_clicked(self, s):
        info(f"{s} clicked")
