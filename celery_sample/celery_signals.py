"""
    References:
        https://docs.celeryproject.org/en/stable/userguide/signals.html
        https://medium.com/meilleursagents-engineering/how-we-monitor-asynchronous-tasks-da25728173d6
"""
import logging
from celeryconfig import LOGGING
from celery.utils.dispatch import Signal

# task signal
from celery.signals import (
    task_failure,
    task_postrun,
    task_prerun,
    task_success,
    task_received,
    task_retry
    # there are still many other task signals
)

# worker signal
from celery.signals import (
    celeryd_init,
    worker_init,
    worker_ready
)

# logging signal
from celery.signals import (
    setup_logging,
    after_setup_logger,
    after_setup_task_logger
)

LOG = logging.getLogger('celery')


# ========================================= TASK signals ============================
@task_prerun.connect
def task_prerun_handler(task_id, task, *args, **kwargs):
    LOG.error(' sssssssssssssssssssssssssss 1 {} : {}'.format(task.name, task_id))

@task_received.connect
def task_received_handler(request, *args, **kwargs):
    LOG.error(' sssssssssssssssssssssssssss 2 {}'.format(request))

@task_postrun.connect
def task_postrun_handler(task_id, task, *args, **kwargs):
    LOG.error(' sssssssssssssssssssssssssss 3 {} : {}'.format(task.name, task_id))

@task_success.connect
def task_success_handler(result, **kwargs):
    LOG.error(' sssssssssssssssssssssssssss 4 {}'.format(result))

@task_failure.connect
def task_failure_handler(task_id, exception, traceback, einfo, *args, **kwargs):
    LOG.error(' sssssssssssssssssssssssssss 5 {} \n\n\n {} \n\n\n {}'.format(task_id, exception, traceback))


@task_retry.connect
def task_retry_handler(request, reason, einfo, *args, **kwargs):
    LOG.error(' sssssssssssssssssssssssssss 6 {} : {} : {}'.format(request, reason, einfo))


# ========================================= LOGGING signals ============================

@setup_logging.connect
def config_loggers(*args, **kwags):
    from logging.config import dictConfig
    dictConfig(LOGGING)
