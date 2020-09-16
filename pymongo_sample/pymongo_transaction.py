"""
https://docs.mongodb.com/manual/tutorial/query-arrays/
"""
import json
import pymongo
import random
import time
import threading
from utils import ObjectIdEncoder
from url import AUTHEN_URL


client = pymongo.MongoClient('localhost', 27017)
# client = pymongo.MongoClient(AUTHEN_URL)

db = client.test_database
collection = db.test_collection


class TransactionExample(object):

    def __init__(self):
        collection.drop()
        for i in range(0, 3):
            collection.insert_one(
                {
                    "_id": i,
                    "age": random.choice(range(1, 100)),
                    "name": random.choice(['Anh', 'Hoa', 'Nghia', 'Phuc', 'Hieu']),
                }
            )
        for item in collection.find({}, {'_id': False}):
            print("Sample data  1:", item)
        print('------------------------------------------------------------')

    def transaction1(self, sleep_time=1):
        # Refer: https://api.mongodb.com/python/current/api/pymongo/client_session.html#classes
        # part: with_transaction
        def callback(session, custom_arg, custom_kwarg=None):
            collection.update_one(
                {'_id': 0},
                {'$set': {'name': "David", 'age': 100}}
            )
            time.sleep(sleep_time)

        with client.start_session() as session:
            session.with_transaction(lambda s: callback(s, "custom_arg", custom_kwarg=1))

        for item in collection.find():
            print("After data : ", item)
        print('------------------------------------------')

    def transaction2(self, sleep_time=1):
        # Refer: https://api.mongodb.com/python/current/api/pymongo/client_session.html#transactions
        with client.start_session() as session:
            collection.update_one(
                {'_id': 0},
                {'$set': {'name': "David", 'age': 100}},
                session=session
            )
            time.sleep(sleep_time)

        for item in collection.find():
            print("After data 2: ", item)
        print('------------------------------------------')

    def test_block_write(self):
        threading.Thread()
        f2 = threading.Thread(target=self.transaction2, args=[3])
        f2.setName("ccccccccccccccccccccccccccc")
        f2.start()
        time.sleep(1)
        collection.update_one(
            {'_id': 0},
            {'$set': {'name': "David", 'age': 101}},
        )
        time.sleep(5)
        for item in collection.find():
            print("After data 3: ", item)
        print('------------------------------------------')

    
if __name__ == "__main__":
    transaction_example = TransactionExample()
    # transaction_example.transaction1()
    # transaction_example.transaction2()
    transaction_example.test_block_write()
