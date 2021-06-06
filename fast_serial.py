import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QRect

from lib.project import logset
from PyQt5.Qt import QFontDatabase
debug, info, warn, err = logset('app')

from ui.ui_application import Ui_MainWindow

from lib.set import add_user_setting, window_size, actions, baud_rates, splitter_pos, baud_rate, com_port
from lib.serial_port import SerialPort
from lib.action_dialog import ActionDialog
from serial.tools import list_ports

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
        self.serial = SerialPort()

        for action in actions:
            # info(f"{action} {actions[action]}")
            item = QListWidgetItem(action)
            item.action = actions[action]
            self.ui.actionList.addItem(item)

        self.ui.actionList.itemDoubleClicked.connect(self.on_dclicked_item)
        self.ui.addButton.clicked.connect(self.on_add)
        self.ui.editButton.clicked.connect(self.on_edit)

        font_db = QFontDatabase()
        font_db.addApplicationFont("ui\\resource\\source-code-pro\\SourceCodePro-Regular.ttf")
        font = QFont("Source Code Pro", 9)
        self.ui.comActivityEdit.setCurrentFont(font)

        self.ui.baudCBox.addItems(baud_rates)
        self.ui.baudCBox.setCurrentText(baud_rate)
        self.on_refresh()
        self.ui.portCBox.setCurrentText(com_port)

        self.ui.splitter.splitterMoved.connect(self.on_splitter_moved)
        self.ui.splitter.moveSplitter(splitter_pos[1], 1)
        self.ui.splitter.setHandleWidth(1)

        self.ui.baudCBox.currentTextChanged.connect(self.on_baud_changed)
        self.ui.portCBox.currentTextChanged.connect(self.on_port_changed)

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

    def on_add(self):
        info(f"clicked Add Button")

        dialog = ActionDialog(self)
        dialog.exec()

        if dialog.name != "":
            item = QListWidgetItem(dialog.name)
            item.action = dialog.action
            self.ui.actionList.addItem(item)

    def on_dclicked_item(self, item):
        info(f"clicked {item.text()}, {item.action}")
        self.serial.write(item.action)
        self.ui.comActivityEdit.insertPlainText(item.action)

    def on_edit(self):
        item = self.ui.actionList.currentItem()
        info(f"edit {item.action}")

    def on_connect_clicked(self):
        if self.ui.connectButton.isChecked():
            baud = self.ui.baudCBox.currentText()
            comport = self.ui.portCBox.currentText()
            info(f"baud {baud}")
            info(f"comport {comport}")
            # try to open the serial port
            if self.serial.open(comport, baud) == False:
                return

            self.ui.connectButton.setStyleSheet("background-color : lightblue")

            info(f"Port Opened")
            self.ui.comActivityEdit.setStyleSheet("border: 1px solid gray; background-color: white;")

            # start collecting data in the background
            self.serial.read_text.connect(self.add_to_serial_output)
            self.serial.closed.connect(self.on_comport_off)
        else:
            self.ui.connectButton.setStyleSheet("background-color : lightgrey")
            self.serial.read_text.disconnect()
            self.serial.close()
            self.on_comport_off()

    def add_to_serial_output(self, output):

        self.ui.comActivityEdit.insertPlainText(output)

        # auto scroll to end
        if self.autoscroll:
            self.scrollbar.setValue(self.scrollbar.maximum())

    def on_scroll(self):
        current = self.scrollbar.value()
        if current >= self.scrollbar.maximum() - 3: # add in a little fudge for fast moving data
            self.autoscroll = True
        else:
            self.autoscroll = False

    def on_comport_off(self):
        info(f"comport is OFF")
        self.ui.comActivityEdit.setStyleSheet("border: 1px solid white; background-color: beige;")

    def closeEvent(self, event):
        geometry = self.geometry().getRect()
        info(f"save geometry as {geometry}")
        add_user_setting('window_size', geometry)

        self.serial.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())
