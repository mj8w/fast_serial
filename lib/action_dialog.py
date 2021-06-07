from PyQt5.QtWidgets import QDialog

from ui.ui_action_dialog import Ui_Dialog
from lib.project import logset
debug, info, warn, err = logset('app')

class ActionDialog(QDialog):

    action = ""
    name = ""

    def __init__(self, parent, name = "", action = ""):
        super(ActionDialog, self).__init__(parent)

        ActionDialog.name = name
        ActionDialog.action = action

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

