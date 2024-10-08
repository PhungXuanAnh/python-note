from celery import maybe_signature
from celery.exceptions import SoftTimeLimitExceeded
from celery_app import app
import time
import gevent
from celery.schedules import crontab
from celery import group, chain, chord, Task

import logging

LOG = logging.getLogger('celery')


@app.task(name='ADD-FUNCTION', bind=True)
def add(self, x, y):
    LOG.info('tttttttttttttttttttttt 1 : {}'.format(x))
    LOG.info('tttttttttttttttttttttt 2 : {}'.format(y))
    result = x + y
    return result


@app.task(bind=True)
def longtime_add(self, x=1, y=1, sleep_time=2):
    LOG.info('long time task begins')

    time.sleep(2)
    # Reference: https://docs.celeryproject.org/en/latest/userguide/tasks.html#custom-states
    self.update_state(state="PROGRESS --> this custom state.", meta={"key": "value"})
    time.sleep(sleep_time)

    LOG.info('long time task finished')
    return x + y


@app.task
def long_task(sleep_time):
    for i in range(0, sleep_time):
        LOG.info(" ttttttttttttttttttttttt long_task: {}:{}".format(sleep_time, i))
        time.sleep(i)
    return sleep_time


@app.task(max_retries=5)
def fail_task_retry(task_id, number=0):
    try:
        LOG.info('tttttttttttttttttttttt {}, task id: {}'.format(number, task_id))
        raise Exception("")
    except:
        print("tttttttttttttttttttttt EEEEEEEEEEEEEEEEEEEEEEEEException")
        number += 1
        fail_task_retry.retry(args=[task_id, number], countdown=5)


@app.task
def fail_task():
    LOG.info('tttttttttttttttttttttt')
    raise Exception("This is fail task")

@app.task
def forever_task(arg):
    while True:
        time.sleep(1)
        LOG.info(' tttttttttttttttttttttt {}'.format(arg))


@app.task
def countdown_task(number):
    for i in range(0, number):
        LOG.info(' tttttttttttttttttttttt {}'.format(i))


@app.task
def print_hello():
    LOG.info(' tttttttttttttttttttttt Hello')


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls print_result('hello') every 2 seconds.
    sender.add_periodic_task(2.0, print_result.s(' tttttttttttttttttttttt hello'), name='add every 10')

    # Calls print_result('world') every 3 seconds
    sender.add_periodic_task(3.0, print_result.s(' tttttttttttttttttttttt world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        print_result.s('Happy Mondays!'),
    )


@app.task(queue='queue1')
def print_result(arg):
    LOG.info(' tttttttttttttttttttttt RESULTS: {}'.format(arg))


@app.task(queue='queue1')
def print_result_queue1(arg):
    LOG.info(' tttttttttttttttttttttt : {}'.format(arg))


@app.task(queue='queue2')
def print_result_queue2(arg):
    LOG.info(' tttttttttttttttttttttt : {}'.format(arg))


@app.task(queue='queue2')
def chord_task(arg):
    for i in range(0, 15):
        # time.sleep(1)
        gevent.sleep(1)
        LOG.info(' tttttttttttttttttttttt chord task {}-{}'.format(arg, i))
    return arg


chord_result = []
@app.task
def chord_callback(arg):
    chord_result.append(arg)
    LOG.info(' ======= chord task : {}'.format(arg))
    return chord_result

@app.task(name='super_task.error_callback')
def error_callback(*args, **kwargs):
    print(' tttttttttttttttttttttt error_callback ')
    print(args)
    print(kwargs)
    return 'error'


@app.task
def time_limited(arg):
    try:
        for i in range(0, arg):
            time.sleep(1)
            LOG.info(' tttttttttttttttttttttt {}'.format(i))
    except SoftTimeLimitExceeded as e:
        LOG.info(' tttttttttttttttttttttt ')
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

    print(" tttttttttttttttttttttt previous task done: {}".format(task_id_or_ids))
    return "wait_for task is finished"