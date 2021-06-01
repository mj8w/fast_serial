import sys
import traceback

from PyQt5.QtWidgets import QApplication, QMainWindow

from lib.project import logset
from PyQt5.Qt import QListWidgetItem, QLayout, QWidget
debug, info, warn, err = logset('app')

from ui.ui_application import Ui_MainWindow
from ui.ui_list_item import Ui_Form as list_item
from ui.setup_dialog import SetupDialog, Message
from lib.set import add_user_setting, window_size, actions
from lib.serial_port import SerialPort
# from lib.git_version import git_short_version

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

        # load the actions into the list widget
        for action in actions:
            self.addAddEntry(action)
        self.addAddEntry()

    def addAddEntry(self, action = None):
        item = QListWidgetItem()

        # Create widget
        widget = QWidget()
        widget.ui = list_item()
        widget.ui.setupUi(widget)
        widget.ui.horizontalLayout.setSizeConstraint(QLayout.SetFixedSize)
        item.setSizeHint(widget.sizeHint())

        if action is None:
            widget.ui.nameLabel.setText("...")
            widget.ui.actionLabel.setText("")
            widget.ui.editButton.setText("Add")
        else:
            widget.ui.nameLabel.setText(action)
            widget.ui.actionLabel.setText(actions[action])

        # Add widget to QListWidget funList
        self.ui.buttonsListBox.addItem(item)
        self.ui.buttonsListBox.setItemWidget(item, widget)

    def resizeEvent(self, event):
        if self.save_resizing:
            width = self.frameGeometry().width()
            height = self.frameGeometry().height()
            if self.win_width != width or self.win_height != height:
                debug(f"resize to {self.win_width} {self.win_height}")
                add_user_setting('window_size', (width, height))
        QMainWindow.resizeEvent(self, event)

    def setup_dialog(self):

        # TODO: turn off any active serial communications
        # self.serial.close()

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
        info(f"add {output}")
        self.ui.comActivityEdit.insertPlainText(output)

        # auto scroll to end
        if self.autoscroll:
            self.scrollbar.setValue(self.scrollbar.maximum())

    def on_scroll(self):
        current = self.scrollbar.value()
        if current >= self.scrollbar.maximum():
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
