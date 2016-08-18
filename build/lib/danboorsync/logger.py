#
# License: MIT (doc/LICENSE)
# Author: Todd Gaunt
#
# File: imgfetch/fourchan.py
# This file contains the logging functions for writing to stdout stderr etc...

from sys import stderr

PROGRAM_NAME = "imgfetch: "

def error(level, msg):
    global PROGRAM_NAME
    if level < 0:
        errmsg=PROGRAM_NAME + "error: internal error"
    if level >= 0:
        errmsg=PROGRAM_NAME + "error: " + msg

    print(errmsg, file=stderr)
    if level >= 1 or level < 0:
        quit()

def warning(level, msg):
    global PROGRAM_NAME
    if level < 0:
        error(-1, "")
    if level >= 0:
        warnmsg=PROGRAM_NAME + "warning: " + msg

    print(warnmsg)

def output(level, msg):
    global PROGRAM_NAME
    if level < 0:
        error(-1,"")
    if level == 0:
        return
    elif level >= 1:
        outmsg = PROGRAM_NAME + msg

    print(outmsg)

# End of File
