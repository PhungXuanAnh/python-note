from celery import Celery

app = Celery('task_name_1',
             broker='amqp://guest@localhost//',
             backend='rpc://',
             include=['tasks_longtime'])
