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
def hellow_world(context):
    """ Print Hello World! to monitor """

    for x in range(10):
        if not context.dialog.running:
            return
        context.dialog.percent_complete = x * 10
        context.terminal.append_blue_text("Hello World\n")
        context.write("\r\n")
        time.sleep(1)

def expect_DEBUG_msgs(context):

    for x in range(10):
        if not context.dialog.running:
            return
        context.dialog.percent_complete = x * 10

        context.expect("DEBUG")
