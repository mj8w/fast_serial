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

import subprocess

def git_describe():
    out = subprocess.Popen(['git', 'describe'], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    stdout, _stderr = out.communicate()
    return str(stdout)

def git_describe_dirty():
    out = subprocess.Popen(['git', 'describe', '--dirty'], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
    stdout, _stderr = out.communicate()
    return str(stdout)

def git_short_version():
    long = git_describe()

    # if the clone was shallow then no tags will be present, so describe will fail
    if long.find("cannot") != -1:
        return "--"

    dirty = git_describe_dirty().find('dirty') != -1

    gitid = long.find('g')
    if gitid == -1:
        short = long[2:-3]
    else:
        short = long[2:(gitid - 1)]

    if dirty:
        short = short + '_d'
    return short

if __name__ == "__main__":
    print(f"{git_describe()}")
    print(f"{git_short_version()}")
