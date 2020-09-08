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
LOG = logging.getLogger(ENV + '-CHECK-NUMBER-ONLINE-VEHICLES')
LOG.addHandler(slack_webhook_handler)


AUTHEN_URL = os.environ['MONGO_AUTH']

client = pymongo.MongoClient(AUTHEN_URL)

db = client[ENV]
collection = db.users


pipeline = [
    {
        u"$match": {
            u"is_deleted": False
        }
    }, 
    {
        u"$lookup": {
            u"from": u"vehicles",
            u"let": {
                u"user_id": u"$_id"
            },
            u"pipeline": [
                {
                    u"$match": {
                        u"$expr": {
                            u"$eq": [
                                u"$owner",
                                u"$$user_id"
                            ]
                        },
                        u"status": 1.0
                    }
                }
            ],
            u"as": u"vehicles"
        }
    }, 
    {
        u"$project": {
            "_id": {"$toString": "$_id"},
            u"number_online_vehicles": 1.0,
            u"real_number_online_vehicles": {
                u"$size": u"$vehicles"
            }
        }
    }, 
    {
        u"$match": {
            u"$expr": {
                u"$ne": [
                    u"$number_online_vehicles",
                    u"$real_number_online_vehicles"
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

