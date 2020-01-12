"""
https://docs.mongodb.com/manual/tutorial/query-arrays/
"""
import json
import pymongo
from utils import ObjectIdEncoder
from url import AUTHEN_URL


# client = pymongo.MongoClient('localhost', 27017)
client = pymongo.MongoClient(AUTHEN_URL)

db = client.test
collection = db.test_query_array

# match an array
# for item in db.inventory.find({"tags": ["red", "blank"]}):
#     print(item['tags'])
# print('------------------------------------------------')
# for item in db.inventory.find({"tags": {"$all": ["red", "blank"]}}):
#     print(item['tags'])
# print('------------------------------------------------')
# for item in db.inventory.find({"tags": {"$all": ["blank"]}}):
#     print(item['tags'])

# # Query an Array for an Element
# print('------------------------------------------------')
# for item in db.inventory.find({"tags": "red"}):
#     print(item['tags'])


def insert_sample_data():
    collection.drop()
    collection.insert_many([
        {
            "item": "item1",
            "array": [
                {"key1": "A", "key2": 10},
                {"key1": "B", "key2": 13}
            ],
            "array1": [1, 2, 3]
        },
        {
            "item": "item2",
            "array": [
                {"key1": "D", "key2": 11},
                {"key1": "C", "key2": 11}
            ],
            "array1": [1, 4, 3]
        },
        {
            "item": "item3",
            "array": [
                {"key1": "C", "key2": 12},
                {"key1": "B", "key2": 11}
            ],
            "array1": [4, 5, 2]
        },
        {
            "item": "item4",
            "array": [
                {"key1": "C", "key2": 12},
                {"key1": "B", "key2": 13}
            ],
            "array1": [2, 6, 3]
        }
    ])
    for item in collection.find({'_id': False}):
        print("Sample data  :", item)
    print('------------------------------------------------------------')


class Query_Array_Embeded_Document(object):
    """
        https://docs.mongodb.com/manual/tutorial/query-array-of-documents/
    """

    def match_array_contain_document_have_key1_B(self):
        for item in collection.find({"array": {"$elemMatch": {"key1": "B"}}}, {'_id': False}):
            print("Queried data :", item)

    def match_array_have_key1_A_key2_10(self):
        for item in collection.find({"array": {"key1": "A", "key2": 10}}, {'_id': False}):
            print("Queried data :", item)

    def match_array1_contain_3(self):
        for item in collection.find({"array1": {"$all": [3]}}, {'_id': False}):
            print("Queried data :", item)

    def match_array1_contain_2_and_3(self):
        for item in collection.find({"array1": {"$all": [2, 3]}}, {'_id': False}):
            print("Queried data :", item)

    def match_array1_contain_value_greate_or_equal_3(self):
        for item in collection.find({"array1": {"$gte": 3}}, {'_id': False}):
            print("Queried data :", item)

    # ----------------- other condition see above link


class Find_And_Do_Something(object):
    """
        https://docs.mongodb.com/manual/reference/method/db.collection.find/
        https://docs.mongodb.com/manual/reference/method/db.collection.findAndModify/
        https://docs.mongodb.com/manual/reference/method/db.collection.findOne/
        https://docs.mongodb.com/manual/reference/method/db.collection.findOneAndDelete/
        https://docs.mongodb.com/manual/reference/method/db.collection.findOneAndReplace/
        https://docs.mongodb.com/manual/reference/method/db.collection.findOneAndUpdate/
    """

    def find_item1_change_name(self):
        item = collection.find_one_and_update(
            {"item": "item1"},
            {"$set": {"item": "item 11"}},
            {'_id': False}
        )
        print(item)
        print('--------------------------------')
        for item in collection.find({}, {'_id': False}):
            print("Queried data :", item)

    def find_item2_add_set(self):
        item = collection.find_one_and_update(
            {"item": "item2"},
            {"$set": {"key1": "value1", "key2": "value2"}},
            {'_id': False}
        )
        print(item)
        print('--------------------------------')
        for item in collection.find({}, {'_id': False}):
            print("Queried data :", item)

    def find_item4_remove_array(self):
        item = collection.find_one_and_update(
            {"item": "item4"},
            {"$unset": {"array": ""}},
            {'_id': False}
        )
        print(item)
        print('--------------------------------')
        for item in collection.find({}, {'_id': False}):
            print("Queried data :", item)

    def find_item5_or_add_new_with_array(self):
        item = collection.find_one_and_update(
            {"item": "item5"},
            {
                '$addToSet': {'array': {"$each": [
                    {"key1": "C", "key2": 55},
                    {"key1": "B", "key2": 55}
                ]}}
            },
            upsert=True
        )
        print(item)
        print('--------------------------------')
        for item in collection.find({}, {'_id': False}):
            print("Queried data :", item)


if __name__ == "__main__":
    insert_sample_data()

    query = Query_Array_Embeded_Document()
    query.match_array_contain_document_have_key1_B()
    # query.match_array_have_key1_A_key2_10()
    # query.match_array1_contain_3()
    # query.match_array1_contain_2_and_3()
    # query.match_array1_contain_value_greate_or_equal_3()

    find = Find_And_Do_Something()
    # find.find_item1_change_name()
    # find.find_item2_add_set()
    # find.find_item4_remove_array()
    # find.find_item5_or_add_new_with_array()
