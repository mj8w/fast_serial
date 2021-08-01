"""
Copyright 2021 Micheal Wilson
Fast_serial project founded by Micheal Wilson
"""

# write your own script that can interface with the serial port and the terminal
# serial.write(text) to send text

# all action scripts must be inside this file, but of course, you can
# import other functions and call them from here

import time

# See the terminal commands possible in lib/text.py
def hellow_world(serial, terminal, dialog):
    """ Print Hello World! to monitor """

    for x in range(10):
        if not dialog.running:
            return
        dialog.percent_complete = x * 10
        terminal.append_blue_text("Hello World\n")
        serial.write("\r\n")
        time.sleep(1)
