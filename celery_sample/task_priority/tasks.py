from celery_app import app
import logging
import time

LOG = logging.getLogger('celery')

@app.task
def normal_task():
    time.sleep(0)
    LOG.info(" tttttttttttttttttttttt normal_task")


@app.task
def high_priority_task(arg=None):
    for _ in range(0, 10):
        LOG.info(" tttttttttttttttttttttt high_priority_task : {}".format(arg))
        time.sleep(1)