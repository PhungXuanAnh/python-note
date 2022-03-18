from celery import Celery
from celery.schedules import crontab
from celery.backends import redis

# NOTE: best practice https://betterprogramming.pub/python-celery-best-practices-ae182730bb81

app = Celery('task_name_1')

app.config_from_object('celeryconfig')

app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'celery_tasks.print_hello',
        # 'schedule': crontab(hour=7, minute=30, day_of_week=1),    # every Monday morning at 7:30 a.m.
        # crontab(minute="*")     every minute of every day
        # crontab(hour=1, minute="*")     # every minute between 1am and 2am
        # crontab(hour="*", minute=1)         # every first minute of every hour
        'schedule': 3.0,       # every 3 seconds
        # 'args': (16, 16),
    },
}

app.conf.task_publish_retry_policy = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 0.2,
    'interval_max': 0.2,
}

app.conf.update(
    BROKER_CONNECTION_MAX_RETRIES=None
)
