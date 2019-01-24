import os

# ==================== RABBITMQ ===========================================
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', '127.0.0.1')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', 5672)
PUBLIC_EVENT_QUEUE = os.getenv('PUBLIC_EVENT_QUEUE', 'public_event')
WORKER_QUEUE = os.getenv('WORKER_QUEUE', 'worker')
RABBITMQ_URL = 'amqp://guest@' + RABBITMQ_HOST + ':' + str(RABBITMQ_PORT) + '//'

# ==================== REDIS ===========================================
REDIS_HOST = os.getenv('REDIS_URL', '127.0.0.1')
REDIS_PORT = os.getenv('REDIS_URL', 6379)
REDIS_URL = "redis://{host}:{port}".format(host=REDIS_HOST, port=REDIS_PORT)

# ==================== CELERY ===========================================
broker_url = RABBITMQ_URL
# result_backend = RABBITMQ_URL
result_backend = 'rpc://'
# broker_url = REDIS_URL
# result_backend = REDIS_URL

imports = ('tasks_sample')

# task_serializer = 'json'

# result_serializer = 'json'
# accept_content = ['json']

# timezone = 'Europe/Polish'
# enable_utc = True

# worker_disable_rate_limits = True
# result_expires = 30 * 60
