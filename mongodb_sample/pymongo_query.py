"""
https://docs.mongodb.com/manual/tutorial/query-arrays/
"""
import json
import pymongo
import random
from utils import ObjectIdEncoder
from url import AUTHEN_URL


# client = pymongo.MongoClient('localhost', 27017)
client = pymongo.MongoClient(AUTHEN_URL)

db = client.test_database
collection = db.test_collection


def insert_sample_data():
    collection.drop()
    for _ in range(0, 10000):
        collection.insert_one(
            {
                "age": random.choice(range(10, 50)),
                "name": random.choice(['Anh', 'Hoa', 'Nghia', 'Phuc', 'Hieu']),
                "address": random.choice(['Hanoi', 'HCM', "Hai Phong", "Quang Ninh", "Ha Tay"])
            },
        )
    # for item in collection.find({'_id': False}):
    #     print("Sample data  :", item)
    print('------------------------------------------------------------')

if __name__ == "__main__":
    insert_sample_data()