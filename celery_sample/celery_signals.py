import logging
from celery.signals import (
    task_failure,
    task_postrun,
    task_prerun,
    task_success,
    task_received
)

LOG = logging.getLogger('celery')

@task_prerun.connect
def task_prerun_handler(task_id, task, *args, **kwargs):
    LOG.error(' sssssssssssssssssssssssssss 1 {}'.format(task.name))

@task_received.connect
def task_received_handler(request, *args, **kwargs):
    LOG.error(' sssssssssssssssssssssssssss 2 {}'.format(request))