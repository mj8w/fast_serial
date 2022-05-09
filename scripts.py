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

# write your own script that can interface with the serial port and the terminal
# serial.write(text) to send text

# all action scripts must be inside this file, but of course, you can
# import other functions and call them from here

from lib.expect import Expect
from lib.project import logset
debug, info, warn, err = logset('scripts')

# See the terminal commands possible in lib/text.py
def hello_world(serial, terminal, dialog):
    """ Print Hello World! to monitor """

    ex = Expect(serial.read_text) 

    # TODO: wrap in try-except and pass abort signal to except
    for x in range(10):
        if not dialog.running:
            return
        dialog.percent_complete = x * 10
        terminal.append_blue_text("run(hello_world): Sending Hello!\n")
        serial.write("Hello!\r\n")
        ex.expect("Invalid Command Request:", 300)
