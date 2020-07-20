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

# below url for connect to a replica set, this replica set start by using docker-compose from this link:
# https://github.com/PhungXuanAnh/tech-note/tree/master/sample/database/mongodb/mongodb_replica_docker_compose
AUTHEN_URL = "mongodb://localhost:27011,localhost:27012,localhost:27013/DB_NAME?replicaSet=rs0"
# client = pymongo.MongoClient('localhost', 27017)
client = pymongo.MongoClient(AUTHEN_URL)

db = client.dev
collection = db.tasks

pipeline = [
    {
        '$match': {
            "$or": [
                {
                    'operationType': 'update',
                    "updateDescription.updatedFields.assigned_user_id": {"$exists": True}
                },
                {
                    'operationType': 'update',
                    "updateDescription.updatedFields.is_completed": {"$exists": True}
                },
                {'operationType': 'insert'}
            ]
        }
    }
]
    

try:
    with collection.watch(pipeline) as stream:
        for change in stream:
            # Do something
            print(change)
except pymongo.errors.PyMongoError as e:
    # The ChangeStream encountered an unrecoverable error or the
    # resume attempt failed to recreate the cursor.
    print(e.args)
    
