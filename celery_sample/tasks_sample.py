from celery_app import app
import time
from celery.schedules import crontab
from celery.signals import setup_logging
from celeryconfig import LOGGING
import logging

LOG = logging.getLogger('celery')


@app.task
def longtime_add(x, y):
    LOG.info('long time task begins')
    # sleep 5 seconds
    time.sleep(5)
    LOG.info('long time task finished')
    return x + y


@app.task
def print_hello():
    LOG.info('=============================== Hello')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 2 seconds.
    sender.add_periodic_task(2.0, test.s(' ------- hello'), name='add every 10')

    # Calls test('world') every 3 seconds
    sender.add_periodic_task(3.0, test.s(' ------- world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )


@app.task
def test(arg):
    LOG.info(arg)


@setup_logging.connect
def config_loggers(*args, **kwags):
    from logging.config import dictConfig
    dictConfig(LOGGING)
