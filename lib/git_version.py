"""
Copyright 2021 Micheal Wilson
Fast_serial project founded by Micheal Wilson
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
