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

import re
from PyQt5.QtCore import QObject, QThread, pyqtSignal

from PyQt5.QtWidgets import QListWidgetItem
from lib.set import add_user_setting, actions
from lib.expect import Expect

from ui.run_action import RunActionDialog
from lib.dialogs import ActionDialog
try:
    import scripts  # @UnresolvedImport
except ModuleNotFoundError:
    scripts = None

from serial.serialutil import SerialException

from lib.project import logset
debug, info, warn, err = logset('app')

class ActionUi():
    """ Part of the MainWindow """

    def init_action_elements(self):

        for element in actions:
            name, action = element
            item = QListWidgetItem(name)
            item.action = action
            self.ui.actionList.addItem(item)

        self.ui.actionList.itemDoubleClicked.connect(self.on_actions_dclicked_item)
        self.ui.actionList.itemClicked.connect(self.on_actions_clicked_item)
        self.ui.addActionButton.clicked.connect(self.on_actions_add)
        self.ui.editActionButton.clicked.connect(self.on_actions_edit)
        self.ui.removeActionButton.clicked.connect(self.on_actions_remove)

        self.ui.upActionButton.clicked.connect(self.on_actions_list_up)
        self.ui.downActionButton.clicked.connect(self.on_actions_list_down)

        self.ui.editActionButton.setEnabled(False)
        self.ui.removeActionButton.setEnabled(False)
        self.ui.upActionButton.setEnabled(False)
        self.ui.downActionButton.setEnabled(False)

    def on_actions_list_up(self):
        row = self.ui.actionList.currentRow()
        currentItem = self.ui.actionList.takeItem(row)
        new_row = row - 1
        self.ui.actionList.insertItem(new_row, currentItem)
        self.ui.actionList.setCurrentRow(new_row);
        self.ui.upActionButton.setEnabled(new_row != 0)
        self.ui.downActionButton.setEnabled(True)
        self.save_actions()

    def on_actions_list_down(self):
        row = self.ui.actionList.currentRow()
        currentItem = self.ui.actionList.takeItem(row)
        new_row = row + 1
        self.ui.actionList.insertItem(new_row, currentItem)
        self.ui.actionList.setCurrentRow(new_row);
        maxr = self.ui.actionList.count() - 1
        self.ui.downActionButton.setEnabled(new_row != maxr)
        self.ui.upActionButton.setEnabled(True)
        self.save_actions()

    def on_actions_dclicked_item(self, item):
        info(f"dclicked {item.text()}, {item.action}")
        if not self.ui.connectButton.isChecked():
            return
        # create a context - everything needed to run an action
        context = RunContext(self, item)
        context.perform_action()

    def on_actions_clicked_item(self, item):
        info(f"clicked {item.text()}, {item.action}")
        self.ui.editActionButton.setEnabled(True)  # enable once a row is selected
        self.ui.removeActionButton.setEnabled(True)

        row = self.ui.actionList.currentRow()
        maxr = self.ui.actionList.count() - 1
        self.ui.upActionButton.setEnabled(row != 0)
        self.ui.downActionButton.setEnabled(row != maxr)

    def on_actions_add(self):
        info(f"clicked Add Button")

        cr = "<cr>" if self.ui.crCheckBox.isChecked() else ""
        lf = "<lf>" if self.ui.lfCheckBox.isChecked() else ""

        dialog = ActionDialog(self, "", cr + lf)
        success = dialog.exec()
        if not success:
            return

        if ActionDialog.name == "" or ActionDialog.action == "":
            return

        item = QListWidgetItem(ActionDialog.name)
        item.action = ActionDialog.action
        self.ui.actionList.addItem(item)
        self.save_actions()

    def save_actions(self):
        actions = []
        for i in range(self.ui.actionList.count()):
            item = self.ui.actionList.item(i)
            name = item.text()
            action = item.action
            actions.append((name, action))
        add_user_setting('actions', actions)

    def on_actions_edit(self):
        item = self.ui.actionList.currentItem()
        dialog = ActionDialog(self, item.text(), item.action)
        info(f"edit {ActionDialog.name}")

        success = dialog.exec()
        if not success:
            return

        if ActionDialog.name == "" or ActionDialog.action == "":
            return

        item.setText(ActionDialog.name)
        item.action = ActionDialog.action

        self.save_actions()

    def on_actions_remove(self):
        item = self.ui.actionList.currentItem()
        actions.remove((item.text(), item.action))
        row = self.ui.actionList.currentRow()
        self.ui.actionList.takeItem(row)
        self.save_actions()

class RunContext():
    """ Object contains everything that an action script can use to interact with the rest of
        the program
    """

    def __init__(self, parent, list_widget_item):
        self.serial = parent.serial
        self.terminal = parent.com_traffic
        self.script = None
        self.parent = parent

        replacement = {"<cr>":"\r", "<lf>":"\n"}

        self.action = list_widget_item.action
        for r in replacement:
            self.action = re.sub(r, replacement[r], self.action, re.IGNORECASE)

        # check for "run script" directive
        mrun = re.match("<run\s*\((.*)\)>", self.action, re.IGNORECASE)
        if mrun:
            if scripts == None:
                self.terminal.append_blue_text(f"Scripts.py not found to {mrun.group(0)}\n")
                return
            self.script = mrun.group(1)
        self.name = list_widget_item.text()

    def perform_action(self):
        ''' Perform the action in the action list item '''
        if self.script != None:
            self.run_action_in_background()
            return

        # basic operation writes text to the UART
        try:
            self.serial.write(self.action)
        except SerialException:
            self.terminal.write(f"\r\n<<< SERIAL PORT ERROR (closed) >>>")
            self.parent.on_disconnect()
            return
        self.terminal.write(self.action)

    def write_to_serial(self, text):
        try:
            self.serial.write(text)
        except SerialException:
            self.terminal.write(f"\r\n<<< SERIAL PORT ERROR (closed) >>>")
            self.parent.on_disconnect()
            return
        self.terminal.write(text)

    def run_action_in_background(self):

        self.dialog = RunActionDialog(self.parent, self.name)
        self.dialog.start()
        
        def update_progress(percent):
            self.dialog.percent_complete = percent
        
        # set up the script's thread
        self.thread = QThread()
        self.worker = RunScript(read_signal = self.serial.read_text, script = self.script)
        self.worker.moveToThread(self.thread)

        # connect signals
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(update_progress)
        self.worker.comment.connect(self.terminal.append_blue_text)
        self.worker.write_serial.connect(self.write_to_serial)
        self.thread.start()

        # this will block until the dialog closes
        self.dialog.exec()

class RunScript(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    write_serial = pyqtSignal(str)
    comment = pyqtSignal(str)
    
    def __init__(self, script, read_signal):
        super(RunScript, self).__init__()
        self.script = script
        self.input = Expect(read_signal)

    def write(self, text):
        self.write_serial.emit(text)

    def run(self):
        """ Thread which runs the action script. """
        getattr(scripts, self.script)(self)
        self.finished.emit()