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

import traceback
from serial import Serial, SerialException
from PyQt5.QtCore import QObject, pyqtSignal

from lib.project import logset
debug, info, warn, err = logset('serial')

class SerialPort(QObject):
    closed = pyqtSignal()
    read_text = pyqtSignal(str)

    def __init__(self):
        super(SerialPort, self).__init__()
        self.serial = None
        self.running = False
        self.buffer = ""

    def open(self, comport, baud_rate):
        try:
            self.serial = Serial(comport, baud_rate, timeout=0.015)
            return True
        except SerialException:
            return False

    def connect_to_thread(self, thread):
        thread.started.connect(self.run)
        self.closed.connect(thread.quit)
        self.closed.connect(self.deleteLater)
        thread.finished.connect(thread.deleteLater)

    def run(self):
        self.reader()

    def close(self):
        self.running = False
        if self.serial is None:
            return
        try:
            self.serial.close()
        except SerialException:
            pass

    def write(self, output):
        try:
            self.serial.write(output.encode())
            self.serial.flush()
        except SerialException:
            pass

    def reader(self):
        """Read serial port task."""
        self.running = True
        try:
            while(self.running):
                try:
                    btext = self.serial.read(100)
                except (SerialException, TypeError):  # this can happen on serial close
                    continue

                if len(btext) == 0:
                    continue

                self.buffer += btext.decode("UTF-8")

                i = 0
                while 1:
                    try:
                        ch = self.buffer[i]
                    except IndexError:
                        break
                    if ch == '\r' or ch == '\n':  # reached end-of-line
                        try:
                            ch2 = self.buffer[i + 1]
                        except IndexError:
                            break
                        info(f"{self.buffer[:i]}")
                        if ch2 == '\r' or ch2 == '\n' and ch != ch2:  # end-of-line is 2 characters terminator
                            line = self.buffer[:i + 2]
                            self.buffer = self.buffer[i + 2:]
                        else:
                            line = self.buffer[:i + 1]
                            self.buffer = self.buffer[i + 1:]
                        self.read_text.emit(f"{line}")
                        i = 0
                    else:
                        i += 1
        except:
            traceback.print_exc()
        self.closed.emit()

    def log(self, text):
        info(f"{text}")

