"""
https://pymongo.readthedocs.io/en/stable/api/pymongo/change_stream.html
https://docs.mongodb.com/manual/changeStreams/
https://docs.mongodb.com/manual/reference/method/db.collection.watch/#db.collection.watch
https://docs.mongodb.com/manual/reference/change-events
https://docs.mongodb.com/manual/administration/change-streams-production-recommendations/
"""

import json
import random
import time
import logging
import pymongo
import threading
from pymongo import InsertOne, DeleteOne, ReplaceOne, UpdateOne, UpdateMany
from utils import  BsonTimestampEncoder
from url import AUTHEN_URL

# below url for connect to a replica set, this replica set start by using docker-compose from this link:
# https://github.com/PhungXuanAnh/tech-note/tree/master/sample/database/mongodb/mongodb_replica_docker_compose

# AUTHEN_URL = "mongodb://localhost:27011,localhost:27012,localhost:27013/DB_NAME?replicaSet=rs0"
# AUTHEN_URL = "mongodb://localhost:27017"
client = pymongo.MongoClient("localhost", 27017)
# client = pymongo.MongoClient(AUTHEN_URL)

FULL_DOCUMENT_TYPE = "updateLookup"
PIPELINE = [
    {
        "$match": {
            "$or": [
                {
                    'operationType': 'update',
                    "updateDescription.updatedFields.assigned_user_id": {"$exists": True}
                },
                {
                    'operationType': 'update',
                    "updateDescription.updatedFields.is_completed": {"$exists": True}
                },
            ]
        }
    }
    # {"$match": {"operationType": "insert"}}
    # {"$match": {"operationType": "update"}}
]

db = client.test_database
collection = db.test_collection


def insert_sample_data(from_id=0):
    collection.drop()
    for i in range(from_id, from_id + 3):
        collection.insert_one(
            {
                "_id": i,
                "age": random.choice(range(1, 100)),
                "name": random.choice(["Anh", "Hoa", "Nghia", "Phuc", "Hieu"]),
                "address": random.choice(
                    ["Hanoi", "HCM", "Hai Phong", "Quang Ninh", "Ha Tay"]
                ),
            },
        )
    for item in collection.find({}, {"_id": False}):
        print("Sample data  :", item)
    print("------------------------------------------------------------")


def test_do_collection_action():
    time.sleep(1.5)
    collection.insert_one(
        {
            "_id": 400,
            "age": random.choice(range(1, 100)),
            "name": random.choice(["Anh", "Hoa", "Nghia", "Phuc", "Hieu"]),
            "address": random.choice(
                ["Hanoi", "HCM", "Hai Phong", "Quang Ninh", "Ha Tay"]
            ),
        },
    )

    time.sleep(1)
    collection.update_one({"_id": 400}, {"$set": {"age": 400, "name": "400", "address": "400"}})

    time.sleep(1)
    collection.replace_one(
        {"_id": 400}, {"_id": 400, "age": "444", "name": "444", "address": "444"}
    )

    time.sleep(1)
    collection.delete_one({"_id": 400})

    time.sleep(1)
    # https://pymongo.readthedocs.io/en/stable/api/pymongo/collection.html#pymongo.collection.Collection.bulk_write
    requests = [
        InsertOne({
            "_id": 500,
            "age": random.choice(range(1, 100)),
            "name": random.choice(["Anh", "Hoa", "Nghia", "Phuc", "Hieu"]),
            "address": random.choice(
                ["Hanoi", "HCM", "Hai Phong", "Quang Ninh", "Ha Tay"]
            ),
        }),
        UpdateOne({"_id": 500}, {"$set": {"age": 500, "name": "500", "address": "500"}}),
        ReplaceOne({"_id": 555}, {"_id": 555, "age": "555", "name": "555", "address": "555"}),
        DeleteOne({"_id": 500}),
        UpdateMany({"_id": 0}, {"$set": {"age": 0}})
    ]
    collection.bulk_write(requests, ordered=True)
    

def blocking_listener():
    insert_sample_data()
    try:
        resume_token = None
        # with collection.watch(PIPELINE, FULL_DOCUMENT_TYPE) as stream:
        # with collection.watch(PIPELINE) as stream:
        # with collection.watch() as stream:
        with collection.watch(pipeline=None, full_document=FULL_DOCUMENT_TYPE) as stream:
            for event_change in stream:
                print(" ============================== {} ============================== ".format(event_change["operationType"]))
                print(json.dumps(event_change, indent=4, sort_keys=True, cls=BsonTimestampEncoder))
                print("\n\n\n")
                resume_token = stream.resume_token
    except pymongo.errors.PyMongoError as e:
        print(e.args)
        # The ChangeStream encountered an unrecoverable error or the
        # resume attempt failed to recreate the cursor.
        if resume_token is None:
            # There is no usable resume token because there was a
            # failure during ChangeStream initialization.
            logging.error("...")
        else:
            # Use the interrupted ChangeStream's resume token to create
            # a new ChangeStream. The new stream will continue from the
            # last seen insert change without missing any events.
            with db.collection.watch(PIPELINE, resume_after=resume_token) as stream:
                for event_change in stream:
                    print(" ============================== {} ============================== ".format(event_change["operationType"]))
                    print(json.dumps(event_change, indent=4, sort_keys=True, cls=BsonTimestampEncoder))
                    print("\n\n\n")


def non_blocking_listener():
    insert_sample_data()
    # with collection.watch(pipeline=PIPELINE, full_document=FULL_DOCUMENT_TYPE) as stream:
    # with collection.watch(pipeline=PIPELINE) as stream:
    # with collection.watch() as stream:
    with collection.watch(pipeline=None, full_document=FULL_DOCUMENT_TYPE) as stream:
        while stream.alive:
            change = stream.try_next()
            # Note that the ChangeStream's resume token may be updated
            # even when no changes are returned.
            print("Current resume token: %r \n\n\n" % (stream.resume_token,))
            if change is not None:
                print(" ============================== {} ============================== ".format(change["operationType"]))
                print(json.dumps(change, indent=4, sort_keys=True, cls=BsonTimestampEncoder))
                print("\n\n\n")
                continue
            # We end up here when there are no recent changes.
            # Sleep for a while before trying again to avoid flooding
            # the server with getMore requests when no changes are
            # available.
            # time.sleep(10)
            time.sleep(1)


if __name__ == "__main__":
    threading.Thread(target=test_do_collection_action, args=[]).start()
    # insert_sample_data(11)
    blocking_listener()
    # non_blocking_listener()
