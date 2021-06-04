import re

from lib.project import logset, base_dir
debug, info, warn, err = logset('app')

settings_file = "settings.py"
settings = "\\".join([base_dir, settings_file])

# get the default settings
values = {
    'window_size':[500, 700],
    'actions':{'help':'help\r\n', '?':'?\r\n'}
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
    from settings import window_size, actions
except:
    rewrite_settings_file()
    window_size = [500, 500]
    actions = {'help':'help\r\n', '?':'?\r\n'}
    
_ = (window_size, actions)

