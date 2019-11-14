from celery.exceptions import SoftTimeLimitExceeded
from celery_app import app
import time
import gevent
from celery.schedules import crontab
from celery import group, chain, chord, Task
from celery.signals import setup_logging
from celeryconfig import LOGGING
import logging

LOG = logging.getLogger('celery')


@app.task(name='ADD-FUNCTION')
def add(x, y):
    LOG.info('xxxxxxxxxxxxxxxxxxxxxx: {}'.format(x))
    LOG.info('yyyyyyyyyyyyyyyyyyyyyy: {}'.format(y))
    return x + y


@app.task
def longtime_add(x, y):
    LOG.info('long time task begins')
    time.sleep(3)
    LOG.info('long time task finished')
    return x + y


@app.task
def print_hello():
    LOG.info('=============================== Hello')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls print_result('hello') every 2 seconds.
    sender.add_periodic_task(2.0, print_result.s(' ------- hello'), name='add every 10')

    # Calls print_result('world') every 3 seconds
    sender.add_periodic_task(3.0, print_result.s(' ------- world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        print_result.s('Happy Mondays!'),
    )


@app.task(queue='queue1')
def print_result(arg):
    LOG.info(' ========================== RESULTS: {}'.format(arg))


@app.task(queue='queue1')
def print_result_queue1(arg):
    LOG.info(' ======= : {}'.format(arg))


@app.task(queue='queue2')
def print_result_queue2(arg):
    LOG.info(' ======= : {}'.format(arg))


@app.task(queue='queue2')
def chord_task(arg):
    for i in range(0, 15):
        # time.sleep(1)
        gevent.sleep(1)
        LOG.info(' ---------------------- chord task {}-{}'.format(arg, i))
    return arg


chord_result = []
@app.task
def chord_callback(arg):
    chord_result.append(arg)
    LOG.info(' ======= chord task : {}'.format(arg))
    return chord_result


@setup_logging.connect
def config_loggers(*args, **kwags):
    from logging.config import dictConfig
    dictConfig(LOGGING)


# Task inheritance
# http://docs.celeryproject.org/en/stable/userguide/tasks.html#task-inheritance
class MyTask(Task):

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # print('{0!r} failed: {1!r}'.format(task_id, exc))
        print('ffffffffffffffffffffffffff')

    def run(self):
        for i in range(0, 10):
            time.sleep(1)
            print('------------------------- {}: This is class based Task'.format(i))


my_task = app.register_task(MyTask())


@app.task(base=MyTask)
def test_base_class():
    print('bbbbbbbbbbbbbbbbbbbbbbbase task')
    raise KeyError()


@app.task
def time_limited(arg):
    try:
        for i in range(0, arg):
            time.sleep(1)
            LOG.info('---------------------------------- {}'.format(i))
    except SoftTimeLimitExceeded as e:
        LOG.info('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        LOG.exception(e)
