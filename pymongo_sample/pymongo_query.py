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
    for i in range(0, 10000):
        collection.insert_one(
            {
                "_id": i,
                "age": random.choice(range(1, 100)),
                "name": random.choice(['Anh', 'Hoa', 'Nghia', 'Phuc', 'Hieu']),
                "address": random.choice(['Hanoi', 'HCM', "Hai Phong", "Quang Ninh", "Ha Tay"])
            },
        )
    # for item in collection.find({}, {'_id': False}):
    #     print("Sample data  :", item)
    print('------------------------------------------------------------')


class Paging(object):

    def skip_9800_record(self):
        for item in collection.find().skip(9800):
            print(item)

    def limit_100_record(self):
        for item in collection.find().limit(100):
            print(item)

    def skip_5000_record_limit_50_record(self):
        for item in collection.find().skip(5000).limit(50):
            print(item)

    def sort_by_age_skip_5000_record_limit_50_record(self):
        for item in collection.find().sort("age").skip(5000).limit(50):
            print(item)


class Other(object):

    def find_item_have_age_equal_10_or_51_or_99(self):
        for item in collection.find({'age': {'$in': [10, 51, 99]}}).limit(100):
            print(item)

    
if __name__ == "__main__":
    insert_sample_data()

    # p = Paging()
    # p.skip_9800_record()
    # p.limit_100_record()
    # p.skip_5000_record_limit_50_record()
    # p.sort_by_age_skip_5000_record_limit_50_record()

    # q = Other()
    # q.find_item_have_age_equal_10_or_51_or_99()
    
