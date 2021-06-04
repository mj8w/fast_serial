
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from ui.ui_list_item import Ui_Form

from lib.project import logset
debug, info, warn, err = logset('app')

class ActionListItem(QWidget):
    ''' Item in the list of actions '''
    do_action = pyqtSignal(str)

    def __init__(self, parent = None):
        ''' Import a UI and initialize '''
        super(ActionListItem, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.editButton.clicked.connect(self.on_button)

    def setName(self, text):
        self.ui.nameLabel.setText(text)

    def setAction(self, text):
        self.ui.actionLabel.setText(text)

    def on_button(self):
        text = self.ui.actionLabel.text()
        self.do_action.emit(text)
