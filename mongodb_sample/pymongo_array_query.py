"""
https://docs.mongodb.com/manual/tutorial/query-arrays/
"""
import json
import pymongo
from utils import ObjectIdEncoder


client = pymongo.MongoClient('localhost', 27017)

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
            ]
        },
        {
            "item": "item2",
            "array": [
                {"key1": "D", "key2": 11},
                {"key1": "C", "key2": 11}
            ]
        },
        {
            "item": "item3",
            "array": [
                {"key1": "C", "key2": 12},
                {"key1": "B", "key2": 11}
            ]
        },
        {
            "item": "item4",
            "array": [
                {"key1": "C", "key2": 12},
                {"key1": "B", "key2": 13}
            ]
        }
    ])
    for item in collection.find():
        # print("Before data: ", json.dumps(item, indent=4, sort_keys=True, cls=ObjectIdEncoder))
        item.pop('_id')
        print("Sample data  :", item)
    print('------------------------------------------------------------')


class Query_Array_Embeded_Document(object):
    """
        https://docs.mongodb.com/manual/tutorial/query-array-of-documents/
    """

    def extract_match_key1_A_key2_10(self):
        for item in collection.find({"array": {"key1": "A", "key2": 10}}):
            item.pop('_id')
            print("Queried data :", item)

    # ----------------- other condition see above link


if __name__ == "__main__":
    insert_sample_data()

    query = Query_Array_Embeded_Document()
    query.extract_match_key1_A_key2_10()
