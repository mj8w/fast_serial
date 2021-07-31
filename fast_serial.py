"""
Copyright 2021 Micheal Wilson
Fast_serial project founded by Micheal Wilson
"""

import sys
import re
from serial.tools import list_ports

from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, QRect, QEvent, Qt
from PyQt5.Qt import QFontDatabase, QTextCursor

from ui.ui_application import Ui_MainWindow
from lib.set import add_user_setting, window_size, actions, baud_rates, splitter_pos, baud_rate, com_port
from lib.serial_port import SerialPort
from lib.action_dialog import ActionDialog
from lib.text import RichText
from lib.history import History
try:
    import scripts # @UnresolvedImport
except ModuleNotFoundError:
    scripts = None

from lib.project import logset
debug, info, warn, err = logset('app')

# from lib.git_version import git_short_version

from PyQt5 import QtCore
import traceback

if QtCore.QT_VERSION >= 0x50501:

    def excepthook(type_, value, traceback_):
        traceback.print_exception(type_, value, traceback_)
        QtCore.qFatal('')

sys.excepthook = excepthook

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setGeometry(QRect(*window_size))
        self.show()

        self.ui.connectButton.clicked.connect(self.on_connect_clicked)
        self.ui.connectButton.setCheckable(True)
        self.ui.connectButton.setStyleSheet("background-color : lightgrey")
        self.on_comport_off()

        self.scrollbar = self.ui.comActivityEdit.verticalScrollBar()
        self.scrollbar.sliderReleased.connect(self.on_scroll)
        self.autoscroll = False
        self.serial = None

        for action in actions:
            item = QListWidgetItem(action)
            item.action = actions[action]
            self.ui.actionList.addItem(item)

        self.ui.actionList.itemDoubleClicked.connect(self.on_dclicked_item)
        self.ui.actionList.itemClicked.connect(self.on_clicked_item)
        self.ui.addButton.clicked.connect(self.on_add)
        self.ui.editButton.clicked.connect(self.on_edit)
        self.ui.removeButton.clicked.connect(self.on_remove)

        self.ui.upButton.clicked.connect(self.on_list_up)
        self.ui.downButton.clicked.connect(self.on_list_down)

        QFontDatabase.addApplicationFont("ui\\resources\\source-code-pro\\SourceCodePro-Regular.ttf")
        self.ui.comActivityEdit.setFont(QFont("Source Code Pro", 9))
        self.ui.comActivityEdit.setReadOnly(True)
        self.ui.comActivityEdit.selectionChanged.connect(self.on_activity_selected)

        self.com_traffic = RichText(self.ui.comActivityEdit)

        self.ui.baudCBox.addItems(baud_rates)
        self.ui.baudCBox.setCurrentText(baud_rate)
        self.on_refresh()
        self.ui.portCBox.setCurrentText(com_port)

        self.ui.splitter.splitterMoved.connect(self.on_splitter_moved)
        self.ui.splitter.moveSplitter(splitter_pos[1], 1)
        self.ui.splitter.setHandleWidth(1)

        self.ui.baudCBox.currentTextChanged.connect(self.on_baud_changed)
        self.ui.portCBox.currentTextChanged.connect(self.on_port_changed)

        self.ui.clearButton.clicked.connect(self.on_clear_clicked)

        self.ui.editButton.setEnabled(False)
        self.ui.removeButton.setEnabled(False)
        self.ui.upButton.setEnabled(False)
        self.ui.downButton.setEnabled(False)

        self.history = History()
        self.ui.sendLineEdit.returnPressed.connect(self.on_send)
        self.ui.sendLineEdit.installEventFilter(self)   # this causes eventFilter() to be called on key presses

    def on_list_up(self):
        row = self.ui.actionList.currentRow()
        currentItem = self.ui.actionList.takeItem(row)
        new_row = row - 1
        self.ui.actionList.insertItem(new_row, currentItem)
        self.ui.actionList.setCurrentRow(new_row);
        self.ui.upButton.setEnabled(new_row != 0)
        self.ui.downButton.setEnabled(True)

    def on_list_down(self):
        row = self.ui.actionList.currentRow()
        currentItem = self.ui.actionList.takeItem(row)
        new_row = row + 1
        self.ui.actionList.insertItem(new_row, currentItem)
        self.ui.actionList.setCurrentRow(new_row);
        maxr = self.ui.actionList.count() - 1
        self.ui.downButton.setEnabled(new_row != maxr)
        self.ui.upButton.setEnabled(True)

    def on_activity_selected(self):
        self.ui.comActivityEdit.selectionChanged.disconnect()
        cursor = self.ui.comActivityEdit.textCursor()
        cursor.clearSelection()
        cursor.movePosition(QTextCursor.End)
        self.ui.comActivityEdit.setTextCursor(cursor)
        self.ui.comActivityEdit.selectionChanged.connect(self.on_activity_selected)

    def on_send(self):
        text = self.ui.sendLineEdit.text()
        self.history.add(text)
        if self.serial != None:
            self.serial.write(text + "\r\n")
            self.com_traffic.write(text + "\r\n")
        self.ui.sendLineEdit.setText("")

    def eventFilter(self, source, event):
        """ Detect up/down arrow in the send widget """
        if event.type() != QEvent.KeyPress:
            return super(MainWindow, self).eventFilter(source, event)

        if source is self.ui.sendLineEdit:
            if event.key() == Qt.Key_Up:
                text = self.history.up()
                if text != "":
                    self.ui.sendLineEdit.setText(text)
            elif event.key() == Qt.Key_Down:
                text = self.history.down()
                if text != "":
                    self.ui.sendLineEdit.setText(text)
        return super(MainWindow, self).eventFilter(source, event)

    def on_clear_clicked(self):
        self.ui.comActivityEdit.clear()

    def on_baud_changed(self, text):
        add_user_setting("baud_rate", text)

    def on_port_changed(self, text):
        add_user_setting("com_port", text)

    def on_splitter_moved(self, pos, index):

        positions = [0, 0]
        positions[index] = pos
        add_user_setting('splitter_pos', positions)

    def on_refresh(self):
        available_ports = list_ports.comports()
        for port in available_ports:
            if "Bluetooth" in port.description:
                continue
            info(f"{port.name}, {port.description}, {port.hwid}")
            self.ui.portCBox.addItem(port.name, None)

    def on_dclicked_item(self, item):
        info(f"dclicked {item.text()}, {item.action}")

        if not self.ui.connectButton.isChecked():
            return

        ''' Translate the action script into text to send '''
        replacement = {"<cr>":"\r", "<lf>":"\n", "<CR>":"\r", "<LF>":"\n"}
        action = item.action
        for r in replacement:
            action = action.replace(r, replacement[r])

        # check for "run script" directive
        mrun = re.match("<run\s*\((.*)\)>", action)
        if mrun:
            if scripts == None:
                self.com_traffic.append_blue_text(f"Scripts.py not found to {mrun.group(0)}\n")
                return
            script = mrun.group(1)
            getattr(scripts, script)(self.serial, self.com_traffic)
            return

        self.serial.write(action)
        self.com_traffic.write(action)

    def on_clicked_item(self, item):
        info(f"clicked {item.text()}, {item.action}")
        self.ui.editButton.setEnabled(True) # enable once a row is selected
        self.ui.removeButton.setEnabled(True)

        row = self.ui.actionList.currentRow()
        maxr = self.ui.actionList.count() - 1
        self.ui.upButton.setEnabled(row != 0)
        self.ui.downButton.setEnabled(row != maxr)

    def on_add(self):
        info(f"clicked Add Button")

        dialog = ActionDialog(self)
        ActionDialog.name = ""
        ActionDialog.action = ""
        success = dialog.exec()
        if not success:
            return

        if ActionDialog.name == "" or ActionDialog.action == "":
            return

        item = QListWidgetItem(ActionDialog.name)
        item.action = ActionDialog.action
        self.ui.actionList.addItem(item)

        actions.update({ActionDialog.name:ActionDialog.action})
        add_user_setting('actions', actions)

    def on_edit(self):
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

        actions.update({ActionDialog.name:ActionDialog.action})
        add_user_setting('actions', actions)

    def on_remove(self):
        item = self.ui.actionList.currentItem()
        actions.pop(item.text())
        add_user_setting('actions', actions)

        row = self.ui.actionList.currentRow()
        self.ui.actionList.takeItem(row)

    def on_connect_clicked(self):
        if self.ui.connectButton.isChecked():
            self.ui.comActivityEdit.selectionChanged.connect(self.on_activity_selected)
            self.ui.comActivityEdit.setReadOnly(True)
            cursor = self.ui.comActivityEdit.textCursor()
            cursor.clearSelection()
            cursor.movePosition(QTextCursor.End)
            self.ui.comActivityEdit.setTextCursor(cursor)
            baud = self.ui.baudCBox.currentText()
            comport = self.ui.portCBox.currentText()
            info(f"baud {baud}")
            info(f"comport {comport}")
            # try to open the serial port

            self.thread = QThread()
            self.serial = SerialPort()
            if not self.serial.open(comport, baud_rate):
                self.add_to_serial_output("NOT ABLE TO OPEN PORT")
                return

            self.serial.moveToThread(self.thread)

            # connect signals
            self.serial.connect_to_thread(self.thread)
            self.serial.read_text.connect(self.add_to_serial_output)
            self.serial.closed.connect(self.on_comport_off)

            self.thread.start()

            self.ui.connectButton.setStyleSheet("background-color : lightblue")

            info(f"Port Opened")
            self.ui.comActivityEdit.setStyleSheet("border: 1px solid gray; background-color: white;")

        else:
            self.ui.comActivityEdit.selectionChanged.disconnect()
            self.ui.connectButton.setEnabled(False) # temporarily until thread has completed
            self.ui.connectButton.setStyleSheet("background-color : lightgrey")
            self.ui.comActivityEdit.setReadOnly(False)
            self.serial.read_text.disconnect()
            self.serial.close()

    def add_to_serial_output(self, output):
        self.com_traffic.insert_input_text(output)

        # auto scroll to end
        if self.autoscroll:
            self.scrollbar.setValue(self.scrollbar.maximum())

    def on_scroll(self):
        current = self.scrollbar.value()
        if current >= self.scrollbar.maximum() - 5: # add in a little fudge for fast moving data
            self.autoscroll = True
        else:
            self.autoscroll = False

    def on_comport_off(self):
        info(f"comport is OFF")
        self.ui.connectButton.setEnabled(True)
        self.ui.comActivityEdit.setStyleSheet("border: 1px solid white; background-color: beige;")

    def closeEvent(self, event):
        geometry = self.geometry().getRect()
        info(f"save geometry as {geometry}")
        add_user_setting('window_size', geometry)

        if self.serial != None:
            self.serial.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())
