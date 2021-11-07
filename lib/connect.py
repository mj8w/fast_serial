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

from PyQt5.QtCore import QThread
from PyQt5.Qt import QTextCursor
from lib.serial_port import SerialPort
from lib.set import baud_rate

from lib.project import logset
debug, info, warn, err = logset('app')

class ConnectButton():
    """ Part of MainWindow -  deal with button connecting/disconnecting to the serial port"""

    def setup_connectButton(self):
        """ Init connect button for use """
        self.ui.connectButton.clicked.connect(self.on_connect_clicked)
        self.ui.connectButton.setCheckable(True)
        self.ui.connectButton.setStyleSheet("background-color : lightgrey")

    def on_connect_clicked(self):
        if self.ui.connectButton.isChecked():
            self.on_connect()
        else:
            self.on_disconnect()

    def on_connect(self):
        """ When button is clicked and the result is the button is "ON" """

        # try to open the serial port
        self.serial = SerialPort()
        baud = self.ui.baudCBox.currentText()
        comport = self.ui.portCBox.currentText()
        if not self.serial.open(comport, baud):
            self.add_to_serial_output("NOT ABLE TO OPEN PORT")
            self.ui.connectButton.setChecked(False)
            self.serial = None
            return

        # set up the com activity (terminal) window for receiving characters
        self.ui.comActivityEdit.selectionChanged.connect(self.on_activity_selected)
        self.ui.comActivityEdit.setReadOnly(True)
        cursor = self.ui.comActivityEdit.textCursor()
        cursor.clearSelection()
        cursor.movePosition(QTextCursor.End)
        self.ui.comActivityEdit.setTextCursor(cursor)
        self.ui.comActivityEdit.setStyleSheet("border: 1px solid gray; background-color: white;")

        # disable comport and baudrate dropdowns
        self.ui.baudCBox.setEnabled(False)
        self.ui.portCBox.setEnabled(False)

        # set up the communication to the serial port
        self.thread = QThread()
        self.serial.moveToThread(self.thread)

        # connect signals
        self.serial.connect_to_thread(self.thread)
        self.serial.read_text.connect(self.add_to_serial_output)
        self.serial.closed.connect(self.on_comport_off)

        self.thread.start()

        self.ui.connectButton.setStyleSheet("background-color : lightblue")

        info(f"Port Opened")

    def on_disconnect(self):
        """ When button is clicked and the result is the button is "OFF" """

        self.ui.comActivityEdit.selectionChanged.disconnect()
        self.ui.connectButton.setEnabled(False) # temporarily until thread has completed
        self.ui.connectButton.setStyleSheet("background-color : lightgrey")
        self.ui.comActivityEdit.setReadOnly(False)
        self.serial.read_text.disconnect()
        self.serial.close()

        # re-enable comport and baudrate dropdowns
        self.ui.baudCBox.setEnabled(True)
        self.ui.portCBox.setEnabled(True)

        # because this can be called by external code, explicitly make the button unchecked
        self.ui.connectButton.setChecked(False)
