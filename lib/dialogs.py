"""
Copyright 2021 Micheal Wilson
Fast_serial project founded by Micheal Wilson
"""

from PyQt5.QtWidgets import QDialog

from ui.ui_action_dialog import Ui_Dialog as actionDialog
from ui.ui_filter_dialog import Ui_FilterDialog as filterDialog
from lib.project import logset
debug, info, warn, err = logset('app')

class ActionDialog(QDialog):

    action = ""
    name = ""

    def __init__(self, parent, name = "", action = ""):
        super(ActionDialog, self).__init__(parent)

        ActionDialog.name = name
        ActionDialog.action = action

        self.ui = actionDialog()
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

class FilterDialog(QDialog):

    filter = ""
    name = ""

    def __init__(self, parent, name = "", the_filter = ""):
        super(FilterDialog, self).__init__(parent)

        FilterDialog.name = name
        FilterDialog.filter = the_filter

        self.ui = filterDialog()
        self.ui.setupUi(self)

        # wire dialog OK/cancel buttons to default handlers
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.ui.nameEdit.setText(name)
        self.ui.filterEdit.setText(the_filter)

        self.ui.nameEdit.textChanged.connect(self.on_name_changed)
        self.ui.filterEdit.textChanged.connect(self.on_filter_changed)

    def on_name_changed(self):
        FilterDialog.name = self.ui.nameEdit.text()

    def on_filter_changed(self):
        FilterDialog.filter = self.ui.filterEdit.toPlainText()
