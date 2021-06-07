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

        # wire dialog OK/cancel buttons to default handlers
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.ui.nameEdit.setText(name)
        self.ui.actionEdit.setText(action)

        self.ui.nameEdit.textChanged.connect(self.on_name_changed)
        self.ui.actionEdit.textChanged.connect(self.on_action_changed)

    def on_name_changed(self):
        ActionDialog.name = self.ui.nameEdit.text()

    def on_action_changed(self):
        ActionDialog.action = self.ui.actionEdit.toPlainText()
