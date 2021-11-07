"""
Copyright 2021 Micheal Wilson
Fast_serial project founded by Micheal Wilson

    This file is part of Fast_Serial.

    Fast_Serial is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    Fast_Serial is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Fast_Serial.  If not, see <https://www.gnu.org/licenses/>
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
