"""
https://docs.mongodb.com/manual/tutorial/query-arrays/
"""
import json
import pymongo
import random
from utils import ObjectIdEncoder
from url import AUTHEN_URL


client = pymongo.MongoClient('localhost', 27017)
# client = pymongo.MongoClient(AUTHEN_URL)

db = client.test_database
collection = db.test_collection


def insert_sample_data():
    collection.drop()
    for i in range(0, 50):
        result = collection.insert_one(
            {
                "_id": i,
                "age": random.choice(range(50, 90)),
                "name": random.choice(['Anh', 'Hoa', 'Nghia', 'Phuc', 'Hieu']),
                "address": random.choice(['Hanoi', 'HCM', "Hai Phong", "Quang Ninh", "Ha Tay"]),
                "scores": random.sample(range(5, 10), 3)
            },
        )
        print("--------- document _id: {}".format(result.inserted_id))
    for item in collection.find():
        print(item)
    print(collection.find().count())
    print('------------------------------------------------------------')


class Delete(object):

    def __init__(self):
        insert_sample_data()

    def remove_all_items_which_have_scores_contain_5(self):
        result = collection.delete_many({
            "scores": {"$all": [5]}
        })
        print(result.acknowledged)
        print(result.deleted_count)
        print(collection.find().count())
        for item in collection.find():
            print(item)


if __name__ == "__main__":
    delete = Delete()
    delete.remove_all_items_which_have_scores_contain_5()
