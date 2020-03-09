from logging.config import dictConfig
import logging
import os
import json


with open('/home/xuananh/Dropbox/Work/Other/slack-token-api-key.json', "r") as in_file:
    SLACK_API_KEY = json.load(in_file)['phungxuananh']


LOGGING_SLACK_API_KEY = SLACK_API_KEY
LOGGING_SLACK_CHANNEL = "#general"
LOG_DIR = 'logs'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'app.DEBUG': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/app.log',
            'maxBytes': 1 * 1024,  # 1Kb       #100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
        },
        'app.ERROR': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/app.ERROR.log',
            'maxBytes': 1 * 1024,  # 1Kb       #100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
        },
        'slack.ERROR': {
            'level': 'ERROR',
            'api_key': LOGGING_SLACK_API_KEY,
            'class': 'slacker_log_handler.SlackerLogHandler',
            'channel': LOGGING_SLACK_CHANNEL
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console', 'app.DEBUG', 'app.ERROR', 'slack.ERROR'],
            'propagate': False,
            'level': 'INFO',
        },
    }
}

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

dictConfig(LOGGING)

# list all logger
print('--------------------------------------------------------')
print(logging.Logger.manager.loggerDict)
print('--------------------------------------------------------')

logger_app = logging.getLogger('app')
logger_thirdparty_app_request = logging.getLogger('app')
logger_thirdparty_app_statistic = logging.getLogger('app')

logger_app.error('aaaaaaaaaaaaaaaaaaa')
logger_thirdparty_app_request.error('bbbbbbbbbbbbbbbbb')
logger_thirdparty_app_statistic.error('cccccccccccccccccccccccc')

logger_app.info('aaaaaaaaaaaaaaaaaaa')
logger_thirdparty_app_request.info('bbbbbbbbbbbbbbbbb')
logger_thirdparty_app_statistic.info('cccccccccccccccccccccccc')
