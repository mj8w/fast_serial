import sys
from os.path import abspath, dirname

this_dir = abspath(dirname(__file__)) # should be lib directory
base_dir = abspath(f"{this_dir}\\..") 

import logging
from logging import config as logging_config

logfile = "\\".join([this_dir, 'logging.ini'])
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