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
import os
from os import sep

app = f"pyuic5.exe"

files = [
    "application",
    "setup",
    "action_dialog",
    "filter_dialog",
    "run_dialog"
    ]

def main():

    for file in files:
        print(f"{app} {file}.ui > ui_{file}.py")
        os.system(f"{app} {file}.ui > ui_{file}.py")

if __name__ == '__main__':
    main()
