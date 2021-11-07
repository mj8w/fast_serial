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
from lib.set import add_user_setting, send_history

from lib.project import logset
debug, info, warn, err = logset('app')

class History():
    """ manage the history of send widget entries"""

    def __init__(self):
        self.history = send_history
        self.pos = len(self.history) - 1

    def add(self, text):
        """ Add an entry to the history """
        if text == "":
            return

        if not len(self.history):
            self.history.append(text)
        elif text != self.history[-1]:
            self.history.append(text)

        limit = 50 # who will scroll up 50 entries?
        size = len(self.history)
        if size > limit: # limit the size to something usable
            self.history = self.history[size - limit:]

        self.pos = len(self.history)
        debug(f"add(): len {len(self.history)}, pos = {self.pos}")

        add_user_setting("send_history", self.history)

    def up(self):
        self.pos -= 1

        if len(self.history) == 0:
            return ""

        if self.pos < 0:
            self.pos = 0

        debug(f"up(): len {len(self.history)}, pos = {self.pos}")
        return self.history[self.pos]

    def down(self):
        self.pos += 1

        if len(self.history) == 0:
            return ""

        if self.pos >= len(self.history):
            self.pos = len(self.history) - 1

        debug(f"down(): len {len(self.history)}, pos = {self.pos}")
        return self.history[self.pos]

