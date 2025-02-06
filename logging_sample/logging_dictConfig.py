'''
Format of logging
Attribute name      Format                    Description
args               You shouldn't need to format this yourself.The tuple of arguments merged into msg to produce message, or a dict whose values are used for the merge (when there is only one argument, and it is a dictionary).
asctime            %(asctime)s    Human-readable time when the LogRecord was created. By default this is of the form '2003-07-08 16:49:45,896' (the numbers after the comma are millisecond portion of the time).
created            %(created)f    Time when the LogRecord was created (as returned by time.time()).
exc_info           You shouldn't need to format this yourself.Exception tuple (sys.exc_info) or, if no exception has occurred, None.
filename           %(filename)s    Filename portion of pathname.
funcName           %(funcName)s    Name of function containing the logging call.
levelname          %(levelname)s    Text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
levelno            %(levelno)s    Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL).
lineno             %(lineno)d    Source line number where the logging call was issued (if available).
module             %(module)s    Module (name portion of filename).
msecs              %(msecs)d    Millisecond portion of the time when the LogRecord was created.
message            %(message)s    The logged message, computed as msg % args. This is set when Formatter.format() is invoked.
msg                You shouldn't need to format this yourself.The format string passed in the original logging call. Merged with args to produce message, or an arbitrary object (see Using arbitrary objects as messages).
name               %(name)s    Name of the logger used to log the call.
pathname           %(pathname)s    Full pathname of the source file where the logging call was issued (if available).
process            %(process)d    Process ID (if available).
processName        %(processName)s    Process name (if available).
relativeCreated    %(relativeCreated)d    Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded.
thread             %(thread)d    Thread ID (if available).
threadName         %(threadName)s    Thread name (if available).
'''

import json
import logging
import os
from logging.config import dictConfig

# with open('/home/xuananh/Dropbox/Work/Other/slack-token-api-key.json', "r") as in_file:
#     SLACK_API_KEY = json.load(in_file)['phungxuananh']

# LOGGING_SLACK_API_KEY = SLACK_API_KEY
# LOGGING_SLACK_CHANNEL = "#general"

class MyFilter(logging.Filter):
    def __init__(self, param=None):
        self.param = param

    def filter(self, record):
        if self.param is None:
            allow = True
        else:
            allow = self.param not in record.msg

        if allow:
            record.msg = "changed: " + record.msg + "\n---------------------------------"

        return allow


LOG_DIR = os.path.dirname(os.path.realpath(__file__)) + "/logs"
os.makedirs(LOG_DIR) if not os.path.exists(LOG_DIR) else None

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "add_my_custom_attribute": {
            "()": "logging_sample.formatter.custom_format.MyCustomFormatAttributes",
        },
        "myfilter": {
            "()": MyFilter,
            "param": "noshow",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] [%(custom_format)s] [%(pathname)s:%(lineno)d] [%(funcName)s] %(levelname)s: %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["add_my_custom_attribute", "myfilter"],
        },
        "app.DEBUG": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": LOG_DIR + "/app.log",
            "maxBytes": 1 * 1024,  # 1Kb       #100 * 1024 * 1024,  # 100Mb
            "backupCount": 3,
            "filters": ["add_my_custom_attribute"],
        },
        "app.ERROR": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": LOG_DIR + "/app.ERROR.log",
            "maxBytes": 1 * 1024,  # 1Kb       #100 * 1024 * 1024,  # 100Mb
            "backupCount": 3,
            "filters": ["add_my_custom_attribute"],
        },
        # 'slack.ERROR': {
        #     'level': 'ERROR',
        #     'api_key': LOGGING_SLACK_API_KEY,
        #     'class': 'slacker_log_handler.SlackerLogHandler',
        #     'channel': LOGGING_SLACK_CHANNEL
        # },
    },
    "loggers": {
        "console": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
        "all-handlers": {
            "handlers": ["console", "app.DEBUG", "app.ERROR"],
            "propagate": False,
            "level": "INFO",
        },
    },
}

dictConfig(LOGGING_CONFIG)
all_handlers_logger = logging.getLogger("all-handlers")
console_logger = logging.getLogger("console")

if __name__ == "__main__":

    # list all logger
    print("--------------------------------------------------------")
    print(logging.Logger.manager.loggerDict)
    print("--------------------------------------------------------")

    all_handlers_logger.error("aaaaaaaaaaaaaaaaaaa")
    all_handlers_logger.info("aaaaaaaaaaaaaaaaaaa")

    all_handlers_logger.error("hello")
    all_handlers_logger.error("hello - noshow")
