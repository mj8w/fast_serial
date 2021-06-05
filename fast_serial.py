import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QLayout

from lib.project import logset
debug, info, warn, err = logset('app')

from ui.ui_application import Ui_MainWindow
from ui.setup_dialog import SetupDialog, Message
from lib.set import add_user_setting, window_size, actions
from lib.serial_port import SerialPort
from lib.list_item import ActionListItem
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
        self.save_resizing = False
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.show()

        self.win_width, self.win_height = window_size
        self.resize(self.win_width, self.win_height)
        self.save_resizing = True

        self.ui.portButton.clicked.connect(self.setup_dialog)
        self.on_comport_off()

        self.scrollbar = self.ui.comActivityEdit.verticalScrollBar()
        self.scrollbar.sliderReleased.connect(self.on_scroll)
        self.autoscroll = False
        self.serial = SerialPort()

        for action in actions:
            # info(f"{action} {actions[action]}")
            action_item = ActionListItem(None, action, actions[action])
            item = QListWidgetItem()

            action_item.ui.horizontalLayout.setSizeConstraint(QLayout.SetFixedSize)
            action_item.setLayout(action_item.ui.horizontalLayout)
            item.setSizeHint(action_item.sizeHint())

            self.ui.actionList.addItem(item)
            self.ui.actionList.setItemWidget(item, action_item)

            action_item.edit.connect(self.on_edit)

        self.ui.actionList.itemDoubleClicked.connect(self.on_dclicked_item)
        self.ui.addButton.clicked.connect(self.on_add)

    def on_add(self):
        info(f"clicked Add Button")

    def on_dclicked_item(self, item):
        action_item = self.ui.actionList.itemWidget(item)
        info(f"clicked {action_item.ui.nameLabel.text()}, {action_item.ui.actionLabel.text()}")

    def on_edit(self, form):
        item = self.ui.actionList.currentItem()
        info(f"{form.nameLabel.text()}, {item}")

    def resizeEvent(self, event):
        if self.save_resizing:
            width = self.frameGeometry().width()
            height = self.frameGeometry().height()
            if self.win_width != width or self.win_height != height:
                debug(f"resize to {self.win_width} {self.win_height}")
                add_user_setting('window_size', (width, height))
        QMainWindow.resizeEvent(self, event)

    def setup_dialog(self):

        self.serial.close()

        # prepare the run dialog
        dialog = SetupDialog(self)
        SetupDialog.started = False
        dialog.exec()

        started = SetupDialog.started
        baud = SetupDialog.baud
        comport = SetupDialog.comport

        # try to open the serial port
        if self.serial.open(comport, baud) == False:
            Message("Unable to open the port.")
            return

        if not started:
            return

        info(f"Port Opened")
        self.ui.comActivityEdit.setStyleSheet("border: 1px solid gray; background-color: white;")

        # start collecting data in the background
        self.serial.read_text.connect(self.add_to_serial_output)
        self.serial.closed.connect(self.on_comport_off)

    def add_to_serial_output(self, output):
        info(f"{output.strip()}")
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())
