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

from lib.expect import Aborting, NotFound

from lib.project import logset
debug, info, warn, err = logset('scripts')

"""
 TO USE THIS FEATURE:
 - create a new action
 - after naming the action, set the action text to "<run(hello_world)>"
 - save the action
 - connect to a serial port, then double click the new action
"""

def hello_world(context):
    """ Print Hello World! to monitor x 10, as fast as possible
        and wait for "Invalid Request" each time
    """
    try:
        for x in range(10):
            context.progress(x * 10)
            context.comment("run(hello_world): Sending Hello!\n")
            context.write("Hello!\r\n")
            context.input.expect("Invalid Request", 3)
    except NotFound as nf:
        context.comment(f"found '{nf.found}'")
        context.comment(f"expected '{nf.searching_for}' - aborting")
        return
    except Aborting:
        info("Aborted")
        context.comment("ABORTED\n")
        return