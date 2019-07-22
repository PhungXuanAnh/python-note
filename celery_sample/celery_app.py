from celery import Celery
from celery.schedules import crontab


app = Celery('task_name_1')

app.config_from_object('celeryconfig')

app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'tasks_sample.print_hello',
        # 'schedule': crontab(hour=7, minute=30, day_of_week=1),    # every Monday morning at 7:30 a.m.
        # crontab(minute="*")     every minute of every day
        # crontab(hour=1, minute="*")     # every minute between 1am and 2am
        # crontab(hour="*", minute=1)         # every first minute of every hour
        'schedule': 3.0,       # every 3 seconds
        # 'args': (16, 16),
    },
}

