from celery_app import app
import logging
import time
from celery import Task


LOG = logging.getLogger('celery')
class Task1(Task):
    def __init__(self):
        self._x = 1.0

class Task2(Task):
    def __init__(self):
        self._x = 2.0

@app.task(base=Task1, name='task_base_class_sample_1')
def add1(y):
    LOG.info(" tttttttttttttttttttttt task_base_class_sample_1")
    return add1._x + y

@app.task(base=Task2, name='task_base_class_sample_2')
def add2(y):
    LOG.info(" tttttttttttttttttttttt task_base_class_sample_2")
    return add2._x + y


# Task inheritance
# http://docs.celeryproject.org/en/stable/userguide/tasks.html#task-inheritance
class MyTask(Task):

    def __init__(self):
        self._x = 2.0

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('tttttttttttttttttttttt on_failure {0!r} failed: {1!r}'.format(task_id, exc))
        return None

    def run(self, arg):
        if arg == 6:
            raise Exception(' tttttttttttttttttttttt raise exception')

        print(' tttttttttttttttttttttt arg = {}'.format(arg))
        for i in range(0, arg):
            time.sleep(1)
            print(' tttttttttttttttttttttt {}: This is class based Task {}'.format(i, arg))
        return arg


my_task = app.register_task(MyTask())


@app.task(base=MyTask, name='task_base_class_sample_3')
def add3(y):
    LOG.info(" tttttttttttttttttttttt task_base_class_sample_3")
    return add2._x + y