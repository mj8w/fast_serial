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

from lib.project import logset
debug, info, warn, err = logset('app')

import time
import re
from threading import Lock, Semaphore

class NotFound(Exception):

    def __init__(self, rcvd_data, re_compare):
        self.found = rcvd_data
        self.searching_for = re_compare

    def __str__(self):
        return f"Found '{self.found}' instead of '{self.searching_for}'"

class Aborting(Exception):
    ''' raise when the port closes or similar aborting all operations '''

class Expect():
    ''' For expecting data from a datastream '''

    def __init__(self, signal):
        self.block = Semaphore()  # allow blocking while waiting for data to arrive

        self.mutex = Lock()  # protects incoming data buffer
        self.incoming_data = ""  # incoming data buffer

        # we can un-block processing anytime, it just allows one extra loop of checks in the expect function.
        # better to unblock unnecessarily than to block accidentally.
        self.block.release()  # enable processing in the expect function
        self.abort = False
        signal.connect(self.process_input)

    def process_input(self, data):
        """ enter data that might be expected. """
        with self.mutex:
            self.incoming_data += data
        # release whenever we have data to process
        self.block.release()  # enable processing in the expect function

    def on_abort(self):
        ''' when script has to abort, cancel any open expects. '''
        info("ABORTING")
        self.abort = True
        self.block.release()  # enable processing in the expect function

    def start_timer(self):
        self.start_time = time.time()

    def elapsed(self):
        return time.time() - self.start_time

    def time_left(self, timeout):
        return timeout - self.elapsed()

    def data_len(self):
        with self.mutex:
            return len(self.incoming_data)

    def clear(self):
        """ clear the input buffer """
        with self.mutex:
            self.incoming_data = ""

    def expect(self, re_compare, timeout=1):
        """ block until expected compare matches some input or timeout occurs
            returns the found text.
        """
        self.start_timer()

        compare = re.compile(re_compare)
        while self.time_left(timeout) > 0:
            self.block.acquire(True, self.time_left(timeout))  # block until some data arrives
            if self.abort:
                raise Aborting
            with self.mutex:
                matched = compare.search(self.incoming_data)
            if matched:
                with self.mutex:
                    self.incoming_data = self.incoming_data[matched.end(0):]  # eat up the text that was found from the buffer
                if self.data_len():
                    self.block.release()  # release whenever we have data to process (for next call of expect())
                return matched.group(0)
        raise NotFound(self.incoming_data, re_compare)

    def wait(self, timeout=1):
        """ wait for the specified time to elapse, ignore the incoming text. Return the text that arrived during the wait. """
        self.start_timer()
        self.clear()

        # absorb the block.releases as data arrives
        while self.time_left(timeout) > 0:
            self.block.acquire(True, self.time_left(timeout))  # block until some data arrives
        with self.mutex:
            text = self.incoming_data
        self.clear()
        return text