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

import sys
from os import sep
from os.path import abspath, dirname

this_dir = abspath(dirname(__file__))  # should be lib directory
base_dir = abspath(f"{this_dir}{sep}..")

import logging
from logging import config as logging_config

logfile = sep.join([this_dir, 'logging.ini'])

print(f"LOGFILE = {logfile}")

logging_config.fileConfig(logfile, disable_existing_loggers = False)

def logset(logname):
    ''' convenience sets up a logger object pre-configured with default functions
        attached to the logtype. That way you can set up all the log functions that
        will use the logtype in one line. Usually, you will use one log type name per file.
        You also need to set up the log type in logging.ini.
    Usage:
        from <project> import logset
        debug, info, warn, err = logset('<logtype name>')
    '''
    llog = logging.getLogger(logname)
    llog.propagate = False
    return (llog.debug, llog.info, llog.warning, llog.error)

sys.path.append(base_dir)

from platform import system
