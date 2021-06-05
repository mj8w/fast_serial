
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from ui.ui_list_item import Ui_Form

from lib.project import logset
debug, info, warn, err = logset('app')

class ActionListItem(QWidget):
    ''' Item in the list of actions '''
    edit = pyqtSignal(Ui_Form)

    def __init__(self, parent, name, action):
        ''' Import a UI and initialize '''
        super(ActionListItem, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.nameLabel.setText(name)
        self.ui.actionLabel.setText(action)
        self.ui.editButton.clicked.connect(self.on_edit)

    def setName(self, text):
        self.ui.nameLabel.setText(text)

    def setAction(self, text):
        self.ui.actionLabel.setText(text)

    def on_edit(self):
        info("edit.emit(self.ui)")
        self.edit.emit(self.ui)

