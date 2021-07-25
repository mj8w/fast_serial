"""
Copyright 2021 Micheal Wilson
Fast_serial project founded by Micheal Wilson
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

    def open(self, comport, baud_rate):
        info(f"SerialPort.open()")
        try:
            self.serial = Serial(comport, baud_rate, timeout = 0.015)
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
        self.serial.write(output.encode())
        self.serial.flush()

    def reader(self):
        """Read serial port task."""
        info(f"SerialPort.run()")
        self.running = True
        buffer = "" # buffer for logging the resulting text line by line
        try:
            while(self.running):
                try:
                    btext = self.serial.read(100)
                except (SerialException, TypeError): # this can happen on serial close
                    continue

                if len(btext) == 0:
                    continue

                text = btext.decode("ISO-8859-1")
                print(text.strip())
                self.read_text.emit(f"{text}")
                continue

        except:
            traceback.print_exc()
        info(f"Exiting SerialPort")
        self.closed.emit()
