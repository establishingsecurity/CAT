# This library follows the common advice on how to set up logging for libraries:
#
# https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
# https://docs.python-guide.org/writing/logging/#logging-in-a-library
#
# TLDR: it sets a NullHandler for the __name__ logger in the root __init__.py file. This
# prevents any logs from appearing anywhere. At the same time, it configures the logging
# module just enough so as to allow the library developers to make logging calls without
# running the risk of raising an exception due to a missing handler.
#
# In case you want this library to output logging messages again, do the following:
#
# from cat.log import enable_logging
# enable_logging()

import logging
import logging.config
import sys

# Enable logging if we're in an interactive session.
# See https://stackoverflow.com/questions/2356399/tell-if-python-is-in-interactive-mode
import __main__

# To configure the root logger of the library, its name must be known. Since the current
# name of the library might change in the future, parse __name__ instead of hard-coding:
LIB_ROOT_LOGGER_NAME = __name__.split(".")[0]

default_logging_config = {
    "version": 1,
    "formatters": {
        "simple": {"format": "%(levelname)s %(message)s"},
        "verbose": {
            "format": "%(asctime)22s %(levelname)8s %(process)6d %(threadName)11s %(message)s"
        },
    },
    "handlers": {
        "console-simple": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "console-verbose": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file-verbose": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": "cat.log",
            "maxBytes": 10485760,  # 10 MiB
            "backupCount": 3,
        },
    },
    "loggers": {
        LIB_ROOT_LOGGER_NAME: {
            "level": "DEBUG",
            "handlers": ["console-verbose", "file-verbose"],
        }
    },
}


def enable_logging(config=None, kitten=True):
    """Re-enables logging for this library"""

    if config is None:
        logging.config.dictConfig(default_logging_config)
    else:
        logging.config.dictConfig(config)

    logger = logging.getLogger(LIB_ROOT_LOGGER_NAME)

    if kitten:
        # fmt: off
        logger.critical("Do you see a kitten?")
        logger.error   ("""  |\__/,|   (`\\""")
        logger.warning ("""  |_ _  |.--.) )""")
        logger.info    ("""  ( T   )     / """)
        logger.debug   (""" (((^_(((/(((_/ """)
        # fmt: on


def disable_logging(config=None):
    """Re-disables logging for this library"""

    if config is None:
        # NOTE: if you have configured more loggers, silense them here:
        logging.getLogger(LIB_ROOT_LOGGER_NAME).handlers = [logging.NullHandler()]
    else:
        # In case you are muting loggers through a config:
        logging.config.dictConfig(config)


if (
    not hasattr(__main__, "__file__")
    or not hasattr(sys, "ps1")
    or not hasattr(sys, "ps2")
):
    enable_logging(kitten=False)
