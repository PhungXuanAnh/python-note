from logging.config import dictConfig
import logging
import os
import json

LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

with open('/media/xuananh/data/Dropbox/Work/Other/slack-token-api-key.json',"r") as in_file:
    SLACK_API_KEY=json.load(in_file)['phungxuananh']

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
        'app-file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/app.log',
            'maxBytes': 1 * 1024,  #1Kb       #100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
        },
        'app-error-file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/app.ERROR.log',
            'maxBytes': 1 * 1024,  #1Kb       #100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
        },
        'thirdparty-app-request-file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/thirdparty-app.request.log',
            'maxBytes': 1 * 1024,  #1Kb       #100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
        },
        'thirdparty-app-statistic-file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/thirdparty-app.statistic.log',
            'maxBytes': 1 * 1024,  #1Kb       #100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
        },
        'slack-error': {
            'level': 'ERROR',
            'api_key': SLACK_API_KEY,
            'class': 'slacker_log_handler.SlackerLogHandler',
            'channel': '#general'
        },
        'slack-info': {
            'level': 'INFO',
            'api_key': SLACK_API_KEY,
            'class': 'slacker_log_handler.SlackerLogHandler',
            'channel': '#general'
        },
    },
    'loggers': {
        'app': {
            'handlers': ['app-file', 'console', 'app-error-file', 'slack-error'],
            'propagate': False,
            'level': 'INFO',
        },
        'thirdparty-app.request': {
            'handlers': ['thirdparty-app-request-file', 'console', 'slack-error'],
            'propagate': False,
            'level': 'INFO',
        },
        'thirdparty-app.statistic': {
            'handlers': ['thirdparty-app-statistic-file', 'console', 'slack-error'],
            'propagate': False,
            'level': 'INFO',
        },
    }
}

dictConfig(LOGGING)

# list all logger
print('--------------------------------------------------------')
print(logging.Logger.manager.loggerDict)
print('--------------------------------------------------------')

logger_app = logging.getLogger('app')
logger_thirdparty_app_request = logging.getLogger('thirdparty-app.request')
logger_thirdparty_app_statistic = logging.getLogger('thirdparty-app.statistic')

logger_app.error('aaaaaaaaaaaaaaaaaaa')
logger_thirdparty_app_request.error('bbbbbbbbbbbbbbbbb')
logger_thirdparty_app_statistic.error('cccccccccccccccccccccccc')

logger_app.info('aaaaaaaaaaaaaaaaaaa')
logger_thirdparty_app_request.info('bbbbbbbbbbbbbbbbb')
logger_thirdparty_app_statistic.info('cccccccccccccccccccccccc')