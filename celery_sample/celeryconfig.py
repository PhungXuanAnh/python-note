import os
import re

current_dir = os.path.dirname(__file__)

task_default_queue = 'default'

task_create_missing_queues = True

# task routing
# https://docs.celeryproject.org/en/stable/userguide/routing.html
task_routes = ([
    ('task_routed_sample.feed.tasks.*', {'queue': 'feed'}),
    ('task_routed_sample.web.tasks.*', {'queue': 'web'}),
    (re.compile(r'task_routed_sample\.(video|image)\.tasks\..*'), {'queue': 'media'}),
],)


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
# or: https://ncrocfer.github.io/posts/celery-utiliser-filesystem/
OUT_DIR = os.path.join(os.getcwd(), ".celery/out")
RESULT_DIR = os.path.join(os.getcwd(), ".celery/result")
PROCESESSED_DIR = os.path.join(os.getcwd(), ".celery/processed")

# Create folders if they don't exist
for dir in [OUT_DIR, RESULT_DIR, PROCESESSED_DIR]:
    if not os.path.exists(dir):
        os.makedirs(dir)

broker_url = 'filesystem://'

# ====================================================== task setup ======================================
# task_time_limit = 150
# task_soft_time_limit = 140

imports = (
    'celery_tasks',
    # 'celery_signals',

    'task_routed_sample.feed.tasks',
    'task_routed_sample.image.tasks',
    'task_routed_sample.video.tasks',
    'task_routed_sample.web.tasks',

    'task_priority.tasks',
    'task_base_class_sample.tasks'
)
# task_publish_retry = True
task_publish_retry_policy = {
    'max_retries': 30,
}
# Reference: https://docs.celeryproject.org/en/latest/userguide/tasks.html#custom-states
task_track_started = True

# task_serializer = 'json'
# result_serializer = 'json'
# accept_content = ['json']

# ====================================================== broker setup ======================================
# https://docs.celeryproject.org/en/stable/userguide/configuration.html#std:setting-broker_transport_options
broker_transport_options = {
        'data_folder_in': OUT_DIR,
        'data_folder_out': OUT_DIR,
        'data_folder_processed': PROCESESSED_DIR
}
result_backend = "file://" + RESULT_DIR
# result_backend = 'db+sqlite:///celery-task-results.sqlite'

# broker_connection_retry = True          # retry connect to broker if lost connection
# broker_connection_max_retries = None    # retry forever

# timezone = 'Europe/Polish'
# enable_utc = True

# worker_disable_rate_limits = True
# result_expires = 30 * 60

# ==================== LOGGING ===========================================
# LOGGING_SLACK_API_KEY = ""
# LOGGING_SLACK_CHANNEL = "#general"

LOG_DIR = os.path.join(os.getcwd(), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


# StackDriver setup
def setup_google_logging():
    ENVIRONMENT = "dev"
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser("~/Dropbox/cantec/dev-cantec-driver-google-credentials.json")

    from google.cloud import logging as google_logging
    client = google_logging.Client()
    # Connects the logger to the root logging handler; by default
    # this captures all logs at INFO level and higher
    client.setup_logging()
    return client
    
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
        'rotating_file.DEBUG': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': LOG_DIR + '/celery.DEBUG.log',
            'maxBytes': 1024 * 1024,  # 100 * 1024 * 1024,  # 100Mb
            'backupCount': 3,
        },
        'rotating_file.ERROR': {
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
        # 'gcp_log': {
        #     'level': 'DEBUG',
        #     'class': 'google.cloud.logging.handlers.CloudLoggingHandler',
        #     'client': setup_google_logging(),
        #     'name': "test_celery_live",
        #     'formatter': 'verbose',
        # },
    },
    'loggers': {
        'celery': {
            'handlers': [
                'console', 
                'rotating_file.DEBUG', 
                'rotating_file.ERROR', 
                # 'gcp_log'
                ],
            'propagate': False,
            'level': 'INFO',
        },
        'root': {
            'handlers': [
                'console', 
                'rotating_file.DEBUG', 
                'rotating_file.ERROR',
                # 'gcp_log'
                ],
            'propagate': False,
            'level': 'INFO',
        }
    }
}
