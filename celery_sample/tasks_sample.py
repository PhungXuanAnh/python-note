from celery import maybe_signature
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


@app.task(max_retries=500)
def fail_task(task_id, number=0):
    try:
        LOG.info('=============================== {}, task id: {}'.format(number, task_id))
        raise Exception("")
    except:
        print("###############")
        fail_task.retry(args=[task_id, number], countdown=3)

@app.task
def forever_task(arg):
    while True:
        time.sleep(1)
        LOG.info('=============================== {}'.format(arg))


@app.task
def countdown_task(number):
    for i in range(0, number):
        LOG.info('=============================== {}'.format(i))


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
        print('oooooooooooooooooooooooooooooooooooooooooooooo on_failure {0!r} failed: {1!r}'.format(task_id, exc))
        return None

    def run(self, arg):
        if arg == 6:
            raise Exception('------------------------------------------raise exception')

        print('------------------------------- arg = {}'.format(arg))
        for i in range(0, arg):
            time.sleep(1)
            print('------------------------- {}: This is class based Task {}'.format(i, arg))
        return arg


my_task = app.register_task(MyTask())


@app.task(name='super_task.error_callback')
def error_callback(*args, **kwargs):
    print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
    print('error_callback')
    print(args)
    print(kwargs)
    return 'error'


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


@app.task(bind=True)
def unlock_chord(self, group, callback, interval=1, max_retries=None):
    if group.ready():
        return maybe_signature(callback).delay(group.join())
    raise self.retry(countdown=interval, max_retries=max_retries)

@app.task(bind=True, max_retries=None)
def wait_for(self, task_id_or_ids):
    """
        Reference here: https://stackoverflow.com/a/47226259
    """
    try:
        ready = app.AsyncResult(task_id_or_ids).ready()
    except AttributeError:
        ready = all(app.AsyncResult(task_id).ready()
                    for task_id in task_id_or_ids)

    if not ready:
        self.retry(countdown=2**self.request.retries)

    print("=========================== previous task done: {}".format(task_id_or_ids))
    return "wait_for task is finished"