"""
https://docs.mongodb.com/manual/changeStreams/
https://docs.mongodb.com/manual/reference/method/db.collection.watch/#db.collection.watch
https://docs.mongodb.com/manual/reference/change-events/#change-streams-update-event
"""
import json
import random
import pymongo
from utils import ObjectIdEncoder
from url import AUTHEN_URL


# client = pymongo.MongoClient('localhost', 27017)
client = pymongo.MongoClient(AUTHEN_URL)

db = client.dev
collection = db.users

try:
    with collection.watch([{'$match': {'operationType': 'update'}}]) as stream:
        for insert_change in stream:
            # Do something
            print(insert_change)
except pymongo.errors.PyMongoError as e:
    # The ChangeStream encountered an unrecoverable error or the
    # resume attempt failed to recreate the cursor.
    print(e.args)
    
