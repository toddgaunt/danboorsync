#
# License: MIT (doc/LICENSE)
# Author: Todd Gaunt

from sys import stderr

PROGRAM_NAME = "imgfetch: "

def error(level, msg):
    global PROGRAM_NAME
    if level < 0:
        quit()
    if level >= 0:
        errmsg=PROGRAM_NAME + "error: " + msg

    print(errmsg, file=stderr)
    quit()

def warning(level, msg):
    global PROGRAM_NAME
    if level < 0:
        error(-1, "")
    elif level == 0:
        return
    elif level >= 1:
        nmsg=PROGRAM_NAME + "warning: " + msg

    print(nmsg)

def output(level, msg):
    global PROGRAM_NAME
    if level < 0:
        error(-1,"")
    elif level == 0:
        return
    elif level >= 1:
        nmsg = PROGRAM_NAME + msg

    print(nmsg)

# End of File
