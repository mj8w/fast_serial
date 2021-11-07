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

import sys

from serial.tools import list_ports

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect, QEvent, Qt
from PyQt5.Qt import QFontDatabase, QTextCursor

from ui.ui_application import Ui_MainWindow
from lib.set import add_user_setting, window_size, baud_rates, splitter_pos, splitter2_pos, baud_rate, com_port
from lib.actions import ActionUi
from lib.filters import FilterUi
from lib.text import RichText
from lib.history import History
from lib.connect import ConnectButton

from lib.project import logset, base_dir
from serial.serialutil import SerialException
debug, info, warn, err = logset('app')

# from lib.git_version import git_short_version

from PyQt5 import QtCore
import traceback

if QtCore.QT_VERSION >= 0x50501:

    def excepthook(type_, value, traceback_):
        traceback.print_exception(type_, value, traceback_)
        QtCore.qFatal('')

sys.excepthook = excepthook

class MainWindow(QMainWindow, ActionUi, FilterUi, ConnectButton):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setGeometry(QRect(*window_size))
        self.show()

        self.setup_connectButton()
        self.on_comport_off()

        self.scrollbar = self.ui.comActivityEdit.verticalScrollBar()
        self.scrollbar.sliderReleased.connect(self.on_scroll)
        self.autoscroll = False
        self.serial = None

        QFontDatabase.addApplicationFont(f"{base_dir}\\ui\\resources\\source-code-pro\\SourceCodePro-Regular.ttf")
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

        self.ui.splitter_2.splitterMoved.connect(self.on_splitter2_moved)
        self.ui.splitter_2.moveSplitter(splitter2_pos[1], 1)
        self.ui.splitter_2.setHandleWidth(1)

        self.ui.baudCBox.currentTextChanged.connect(self.on_baud_changed)
        self.ui.portCBox.currentTextChanged.connect(self.on_port_changed)

        self.ui.clearButton.clicked.connect(self.on_clear_clicked)

        self.history = History()
        self.ui.sendLineEdit.returnPressed.connect(self.on_send)
        self.ui.sendLineEdit.installEventFilter(self)   # this causes eventFilter() to be called on key presses

        self.autoscroll = True

        # the action submenu activities are initialized here...
        self.init_action_elements()

        # the filter submenu activities are initialized here...
        self.init_filter_elements()

    def on_activity_selected(self):
        self.ui.comActivityEdit.selectionChanged.disconnect()
        cursor = self.ui.comActivityEdit.textCursor()
        cursor.clearSelection()
        cursor.movePosition(QTextCursor.End)
        self.ui.comActivityEdit.setTextCursor(cursor)
        self.ui.comActivityEdit.selectionChanged.connect(self.on_activity_selected)
        self.ui.sendLineEdit.setFocus()

    def on_send(self):
        """ Send out text from the send input line edit"""
        text = self.ui.sendLineEdit.text()
        cr = "\r" if self.ui.crCheckBox.isChecked() else ""
        lf = "\n" if self.ui.lfCheckBox.isChecked() else ""
        self.history.add(text)
        if self.serial != None:
            try:
                self.serial.write(f"{text}{cr}{lf}")
            except SerialException:
                self.com_traffic.write(f"{cr}{lf}<<< SERIAL PORT ERROR (closed) >>>")
                self.on_disconnect()
                return
            self.com_traffic.write(f"{text}{cr}{lf}")
            self.serial.log(f"{text}")
        self.ui.sendLineEdit.setText("")

    def eventFilter(self, source, event):
        """ Filters out keypress events. Detect up/down arrow in the send widget """
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

    def on_splitter2_moved(self, pos, index):
        positions = [0, 0]
        positions[index] = pos
        add_user_setting('splitter2_pos', positions)

    def on_refresh(self):
        available_ports = list_ports.comports()
        for port in available_ports:
            if "Bluetooth" in port.description:
                continue
            info(f"{port.name}, {port.description}, {port.hwid}")
            self.ui.portCBox.addItem(port.name, None)

    def add_to_serial_output(self, output):
        """ Apply filters and insert the resulting text to the terminal window """

        matched = self.active_filter.search(output)

        if matched != None:
            # found = matched.group(0)
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
