#
# License: MIT (doc/LICENSE)
# Author: Todd Gaunt

from sys import stderr

class logger():
    """ logger

    description:
        logger class used for associated logger module functions

    fields:
        namespace: The namespace or given name the logger was created in.

        level: The level of verbosity the logger functions should use
    """

    def __init__(self, namespace="", level=1):
        self.namespace = namespace
        self.level = level

def error(lg, info):
    """ error

    description:
        Print to stderr with a uniform error format, then call quit()

    example:
        for the following example let __name__ = "__main__"

        >> lg = logger.logger(__name__, 1)
        >> logger.error(lg, "Here is some information")
        __main__: error: Here is some information
    """

    info = "{}: {}: {}".format(lg.namespace, "error", info)
    if (lg.level > 0):
        print(info)
    quit()

def warning(lg, info):
    """ warning

    description:
        Print to stdout with a uniform warning format

    example:
        for the following example let __name__ = "__main__"

        >> lg = logger.logger(__name__, 1)
        >> logger.warning(lg, "Here is a warning")
        __main__: warning: Here is a warning
    """

    info = "{}: {}: {}".format(lg.namespace, "warning", info)
    if (lg.level > 0):
        print(info)

def info(lg, info):
    """ info

    description:
        Print to stdout with a uniform information format

    example:
        for the following example let __name__ = "__main__"

        >> lg = logger.logger(__name__, 1)
        >> logger.info(lg, "Here is an error")
        __main__: info: Here is an error
    """

    info = "{}: {}: {}".format(lg.namespace, "info", info)
    if (lg.level > 0):
        print(info)

# End of File
