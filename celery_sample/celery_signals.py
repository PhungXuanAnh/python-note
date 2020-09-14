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
    task_retry,
    task_revoked
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
    LOG.debug(' sssssssssssssssssssssssssss 1 {} --- {} --- {} --- {}\n\n\n'.format(task.name, task_id, args, kwargs))

@task_received.connect
def task_received_handler(request, *args, **kwargs):
    LOG.debug(' sssssssssssssssssssssssssss 2 {} --- {} --- {}\n\n\n'.format(request, args, kwargs))
    # get all arguments which are passed to task
    # references:
    # https://stackoverflow.com/a/36848418/7639845
    # https://github.com/celery/celery/pull/6049/files#diff-967757bbcc28b0b65c94047bbcce4769
    # https://docs.celeryproject.org/en/stable/reference/celery.worker.request.html
    LOG.debug(' sssssssssssssssssssssssssss 20 : argument of this task: {}\n\n\n'.format(request.args))
    LOG.debug(" sssssssssssssssssssssssssss 21 {}".format(request.body))
    LOG.debug(" sssssssssssssssssssssssssss 22 task_id {}".format(request.task_id))


@task_postrun.connect
def task_postrun_handler(task_id, task, *args, **kwargs):
    LOG.debug(' sssssssssssssssssssssssssss 3 {} : {}'.format(task.name, task_id))

@task_success.connect
def task_success_handler(result, **kwargs):
    LOG.debug(' sssssssssssssssssssssssssss 4 {}'.format(result))

@task_failure.connect
def task_failure_handler(task_id, exception, traceback, einfo, *args, **kwargs):
    LOG.debug(' sssssssssssssssssssssssssss 5 {} \n\n\n {} \n\n\n {}'.format(task_id, exception, traceback))

@task_retry.connect
def task_retry_handler(request, reason, einfo, *args, **kwargs):
    LOG.debug(' sssssssssssssssssssssssssss 6 {} : {} : {}'.format(request, reason, einfo))


# ========================================= LOGGING signals ============================

@setup_logging.connect
def config_loggers(*args, **kwags):
    from logging.config import dictConfig
    dictConfig(LOGGING)
