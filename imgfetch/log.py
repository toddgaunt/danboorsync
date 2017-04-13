import sys

class logger():
    def __init__(self, name="", level=1):
        self.name = name
        self.level = level

    def info(self, info):
        info = "{}: {}: {}\n".format(self.name, "info", info)
        if (self.level > 0):
            sys.stdout.write(info)

    def error(self, info):
        info = "{}: {}: {}\n".format(self.name, "info", info)
        if (self.level >= 0):
            sys.stderr.write(info)

    def fatal(self, info):
        info = "{}: {}: {}\n".format(self.name, "error", info)
        if (self.level >= 0):
            sys.stderr.write(info)
        exit()
