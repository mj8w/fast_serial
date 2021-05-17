
from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.Qt import Qt

from lib.project import logset
debug, info, warn, err = logset('app')

from ui.ui_setup import Ui_SetupDialog
from serial.tools import list_ports

class SetupDialog(QDialog):

    baud = 9600
    comport = "COM3"
    started = False

    def __init__(self, parent):
        super(SetupDialog, self).__init__(parent)
        self.ui = Ui_SetupDialog()
        self.ui.setupUi(self)

        self.on_refresh()   # refresh the com ports list        
        rates = ['1200','2400','4800','9600','19200','38400','57600','115200']
        self.ui.baudCBox.addItems(rates)

        self.ui.startButton.clicked.connect(self.on_start)
        self.ui.comportRefreshButton.clicked.connect(self.on_refresh)        
        self.setAttribute(Qt.WA_DeleteOnClose)
        
    def on_refresh(self):
        available_ports = list_ports.comports()
        for port in available_ports:
            if "Bluetooth" in port.description:
                continue
            info(f"{port.name}, {port.description}, {port.hwid}")
            self.ui.comportCBox.addItem(port.name, None)
        
    def on_start(self):
        # save off the parameters used
        SetupDialog.baud = self.ui.baudCBox.currentText()
        SetupDialog.comport = self.ui.comportCBox.currentText()
        SetupDialog.started = True
        self.close()
        
        
class Message(QMessageBox):
    """ Message dialog shown when some tests are disabled. """

    def __init__(self, message):
        super(Message, self).__init__()

        self.setWindowTitle("Failed to open")
        self.setIcon(QMessageBox.Information)
        self.setStandardButtons(QMessageBox.Ok)
        message.replace(" ", "&nbsp;")
        self.setText(message)
        self.setTextFormat(Qt.RichText)
        self.setInformativeText("Press OK to continue")
        