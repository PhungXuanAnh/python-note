import json
import random
import pymongo
import time
import requests
import traceback
import sys
import logging
import os

class SlackWebhookHandler(logging.Handler):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url        
        logging.Handler.__init__(self)
        
    def emit(self, record):
        msg = self.format(record)
        headers = {'Content-type': 'application/json'}
        try:
            requests.post(url=self.webhook_url, headers=headers, json={"text": msg})
        except:
            traceback.print_exc()

WEBHOOK_URL = os.environ['WEBHOOK_URL']
ENV = os.environ['ENV']

slack_webhook_handler = SlackWebhookHandler(webhook_url=WEBHOOK_URL)
slack_webhook_handler.setLevel(logging.INFO)
slack_webhook_handler.setFormatter(logging.Formatter(
                         '`%(name)-12s` - [%(asctime)s] - `%(levelname)-3s`: %(message)s'))
LOG = logging.getLogger(ENV + '-CHECK-UNCOMPLETED-TASKS')
LOG.addHandler(slack_webhook_handler)


AUTHEN_URL = os.environ['MONGO_AUTH']

client = pymongo.MongoClient(AUTHEN_URL)

db = client[ENV]
collection = db.users

pipeline = [
    {
        u"$match": {
            u"is_active": True,
            u"is_deleted": False,
            u"is_suspend": {
                u"$ne": True
            },
            u"profile_verification_status": 2.0
        }
    }, 
    {
        u"$lookup": {
            u"from": u"tasks",
            u"let": {
                u"user_id": u"$_id"
            },
            u"pipeline": [
                {
                    u"$match": {
                        u"$expr": {
                            u"$eq": [
                                u"$assigned_user_id",
                                u"$$user_id"
                            ]
                        },
                        u"is_completed": False
                    }
                }
            ],
            u"as": u"tasks"
        }
    }, 
    {
        u"$project": {
            u"_id": {
                u"$toString": u"$_id"
            },
            u"uncompleted_tasks": 1.0,
            u"real_uncompleted_tasks": {
                u"$size": u"$tasks"
            }
        }
    }, 
    {
        u"$match": {
            u"$expr": {
                u"$ne": [
                    u"$uncompleted_tasks",
                    u"$real_uncompleted_tasks"
                ]
            }
        }
    }
]

    
while True:
    cursor = collection.aggregate(pipeline)
    invalid_data = list(cursor)
    if len(invalid_data) > 0:
        LOG.error(json.dumps(invalid_data))
    
    time.sleep(300)

