from celery_app import app
import logging

LOG = logging.getLogger('celery')

@app.task
def task_video():
    LOG.info(" tttttttttttttttttttttt task_video")