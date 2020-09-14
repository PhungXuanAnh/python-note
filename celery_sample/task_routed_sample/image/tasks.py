from celery_app import app
import logging
import time

LOG = logging.getLogger('celery')

@app.task
def task_image():
    time.sleep(3)
    LOG.info(" tttttttttttttttttttttt task_image")