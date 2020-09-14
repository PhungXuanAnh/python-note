from celery_app import app
import logging

LOG = logging.getLogger('celery')

@app.task
def task_web():
    LOG.info(" tttttttttttttttttttttt task_web")