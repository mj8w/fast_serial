"""
Copyright 2021 Micheal Wilson
Fast_serial project founded by Micheal Wilson
"""

import re

from lib.project import logset, base_dir
debug, info, warn, err = logset('app')

settings_file = "settings.py"
settings = "\\".join([base_dir, settings_file])

# get the default settings
values = {
    'window_size':[500, 700],
    'actions':[('help', 'help<cr><lf>')],
    'baud_rates':['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200'],
    'splitter_pos':[0, 258],
    'window_size':(167, 118, 1262, 367),
    'baud_rate':'115200',
    'com_port':'COM10',
    'send_history': [],
}

def rewrite_settings_file(new_values = {}):
    values.update(new_values)
    try:
        import settings
        defined = dir(settings)
    except:
        defined = []

    for key, value in values.items():
        if key not in defined:
            add_user_setting(key, value)

def add_user_setting(variable, value):
    lines = []
    try:
        with open(settings, 'r') as f:
            lines.extend(f.readlines())
    except:
        pass

    lines = [line for line in lines if not re.search(variable + "[\t ]*=.*", line)]
    lines.append(variable + " = " + repr(value) + '\n')
    with open(settings, 'w') as f:
        for line in lines:
            f.write(line)

try:
    from settings import baud_rates, splitter_pos, window_size, actions, baud_rate, com_port, send_history
except:
    rewrite_settings_file()
    baud_rates = ['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200']
    splitter_pos = [0, 258]
    window_size = (167, 118, 1262, 367)
    actions = [('help', 'help<cr><lf>')]
    baud_rate = '115200'
    com_port = 'COM3'
    send_history = []

_ = (window_size, splitter_pos, actions, baud_rates, baud_rate, com_port, send_history)

