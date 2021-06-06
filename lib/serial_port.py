from threading import Thread
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
        info(f"Start SerialPort()")
        self.reader_thread = None
        self.serial = None

    def open(self, comport, baud_rate):
        info(f"SerialPort.open()")
        try:
            self.serial = Serial(comport, baud_rate, timeout = 0.015)

            self.reader_thread = Thread(target = self.reader)
            self.reader_thread.start()
            return True
        except SerialException:
            return False

    def close(self):
        if self.serial is None:
            return
        try:
            self.serial.close()
        except SerialException:
            pass
        self.running = False

    def write(self, output):
        self.serial.write(output.encode())

    def reader(self):
        """Read serial port task."""
        info(f"SerialPort.run()")
        self.running = True
        buffer = "" # buffer for logging the resulting text line by line
        try:
            while(self.running):
                try:
                    btext = self.serial.read(100)
                except (SerialException): # this can happen on serial close
                    continue

                if len(btext):
                    text = btext.decode()
                    buffer += text
                    pos = buffer.find("\n")
                    if pos > -1:
                        printable = buffer[:pos]
                        printable = printable.strip()
                        info(f"{printable}")
                        self.read_text.emit(f"{printable}\n")
                        buffer = buffer[pos + 1:]

        except:
            traceback.print_exc()
        info(f"Exiting SerialPort")
        self.closed.emit()
