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
    'filters':[('all', '.+')],
    'baud_rates':['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200'],
    'splitter_pos':[128, 258],
    'splitter2_pos':[128, 258],
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
    from settings import actions, filters, send_history
except:
    rewrite_settings_file()
    actions = [('help', 'help<cr><lf>')]
    filters = [('all', '.+')]
    send_history = []

try:
    from settings import baud_rates, splitter_pos, splitter2_pos, window_size, baud_rate, com_port
except:
    rewrite_settings_file()
    baud_rates = ['1200', '2400', '4800', '9600', '19200', '38400', '57600', '115200']
    splitter_pos = [128, 258]
    splitter2_pos = [128, 258]
    window_size = (167, 118, 1262, 367)
    baud_rate = '115200'
    com_port = 'COM3'

_ = (window_size, splitter_pos, splitter2_pos, actions, filters, baud_rates, baud_rate, com_port, send_history)

