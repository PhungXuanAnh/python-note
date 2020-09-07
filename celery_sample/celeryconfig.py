import os

current_dir = os.path.dirname(__file__)

# ==================== RABBITMQ ===========================================
"""
Create rabbitmq server with command:
docker rm -f test-rabbitmq
docker run -d --name test-rabbitmq \
               -p 15673:15672  \
               -p 5673:5672  \
               rabbitmq:3.8.0-management
"""
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', 5673)
PUBLIC_EVENT_QUEUE = os.getenv('PUBLIC_EVENT_QUEUE', 'public_event')
WORKER_QUEUE = os.getenv('WORKER_QUEUE', 'worker')
RABBITMQ_URL = 'amqp://guest@' + RABBITMQ_HOST + ':' + str(RABBITMQ_PORT) + '//'

# ==================== REDIS ===========================================
REDIS_HOST = os.getenv('REDIS_URL', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_URL', 7379)
REDIS_URL = "redis://{host}:{port}".format(host=REDIS_HOST, port=REDIS_PORT)

# ==================== CELERY ===========================================
# -------------------- using RABBITMQ as broker and backend result
# broker_url = RABBITMQ_URL
# result_backend = RABBITMQ_URL

# -------------------- using REDIS as broker and backend result
# broker_url = REDIS_URL
# result_backend = REDIS_URL + '/9'

# -------------------- using FILESYSTEM as broker and SQLITE as backend result
# reference: https://www.distributedpython.com/2018/07/03/simple-celery-setup/
broker_url = 'filesystem://'
broker_transport_options = {
        'data_folder_in': current_dir + '/broker/out',
        'data_folder_out': current_dir + '/broker/out',
        'data_folder_processed': current_dir + '/broker/processed'
}
result_backend = 'db+sqlite:///celery-task-results.sqlite'


# task_time_limit = 150
# task_soft_time_limit = 140

imports = ('tasks_sample')
# task_publish_retry = True
task_publish_retry_policy = {
    'max_retries': 30,
}
# broker_connection_retry = True          # retry connect to broker if lost connection
# broker_connection_max_retries = None    # retry forever

# task_serializer = 'json'

# result_serializer = 'json'
# accept_content = ['json']

# timezone = 'Europe/Polish'
# enable_utc = True

# worker_disable_rate_limits = True
# result_expires = 30 * 60

# ==================== LOGGING ===========================================
# LOGGING_SLACK_API_KEY = ""
# LOGGING_SLACK_CHANNEL = "#general"
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
        'celery.DEBUG': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/celery.DEBUG.log',
            'maxBytes': 1024 * 1024,  # 100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
        },
        'celery.ERROR': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/celery.ERROR.log',
            'maxBytes': 1024 * 1024,  # 100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
        },
        # 'slack.ERROR': {
        #     'level': 'ERROR',
        #     'api_key': LOGGING_SLACK_API_KEY,
        #     'class': 'slacker_log_handler.SlackerLogHandler',
        #     'channel': LOGGING_SLACK_CHANNEL
        # },
    },
    'loggers': {
        'celery': {
            'handlers': ['console', 'celery.DEBUG', 'celery.ERROR'],
            'propagate': False,
            'level': 'INFO',
        },
        'root': {
            'handlers': ['console', 'celery.DEBUG', 'celery.ERROR'],
            'propagate': False,
            'level': 'INFO',
        }
    }
}
