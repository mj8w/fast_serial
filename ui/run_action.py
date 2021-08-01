"""
Copyright 2021 Micheal Wilson
Fast_serial project founded by Micheal Wilson
"""

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QTimer, Qt

from ui.ui_run_dialog import Ui_Dialog

class RunActionDialog(QDialog):

    def __init__(self, parent, name):
        super(RunActionDialog, self).__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.nameLabel.setText(name)

        self.ui.cancelButton.clicked.connect(self.on_cancel)
        self.setAttribute(Qt.WA_DeleteOnClose)

    def start(self):
        self.ui.progressBar.setMaximum(100)
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setValue(0)

        self.percent_complete = 0
        self.running = True

        # start a timer that updates the dialog
        self.update = QTimer(self)
        self.update.singleShot(250, self.update_progress)

    def update_progress(self):
        """ update the dialog """
        if self.percent_complete >= 100.0:
            self.close()
            return

        self.ui.progressBar.setValue(self.percent_complete)
        self.update.singleShot(250, self.update_progress) # mSec

    def on_cancel(self):
        self.running = False
        self.close()
