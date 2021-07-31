# write your own script that can interface with the serial port and the terminal
# serial.write(text) to send text
# See the terminal commands possible in lib/text.py
def project(serial, terminal):
    """ Print Hello World! to monitor """
    terminal.append_blue_text("Hello World\n")
    serial.write("\r\n")
