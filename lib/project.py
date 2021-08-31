"""
Copyright 2021 Micheal Wilson
Fast_serial project founded by Micheal Wilson
"""

import sys
from os.path import abspath, dirname

import logging
from logging import config as logging_config

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    base_dir = abspath(dirname(sys._MEIPASS))
    logfile = f"{base_dir}\\logging.ini"
else:
    this_dir = abspath(dirname(__file__)) # should be lib directory
    base_dir = abspath(f"{this_dir}\\..")
    logfile = f"{base_dir}\\lib\\logging.ini"
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

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):

    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
            'bare': {
                'format': '%(message)s'
            },
            'simple': {
                'format': '%(name)s: %(message)s'
            },
            'more': {
                'format': '%(relativeCreated)08d:%(name)s: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
            },
            'stream': {
                'level': 'NOTSET',
                'formatter': 'simple',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',  # Default is stderr
            },
            'serial': {
                'level': 'INFO',
                'formatter': 'more',
                'class': 'logging.FileHandler',
                'args': ('serial.log', 'w'),
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['stream'],
                'level': 'INFO',
                'propagate': False
            },
            'app': {
                'handlers': ['stream'],
                'level': 'INFO',
                'propagate': True
            },
            'serial': {
                'handlers': ['serial'],
                'level': 'INFO',
                'propagate': True
            },
        }
    }

    logging_config.dictConfig(LOGGING_CONFIG)
