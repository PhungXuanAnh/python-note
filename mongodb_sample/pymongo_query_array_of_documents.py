"""
https://docs.mongodb.com/manual/tutorial/query-array-of-documents/
"""
import pymongo
from bson.son import SON

client = pymongo.MongoClient('localhost', 27017)

db = client.query_array_of_document

# print('---------------------------------------------------')
# for item in db.inventory.find({'instock.qty': {"$lte": 20}}):
#     print(item['instock'])
# print('---------------------------------------------------')
# for item in db.inventory.find({'instock.qty': {"$eq": 5}}):
#     print(item['instock'])
# print('---------------------------------------------------')
# for item in db.inventory.find({"instock.qty": 5, "instock.warehouse": "A"}):
#     print(item['instock'])

db.inventory.insert_many([
    {"item": "journal",
     "instock": [
         SON([("warehouse", "A"), ("qty", 5)]),
         SON([("warehouse", "C"), ("qty", 15)])]},
    {"item": "notebook",
     "instock": [
         SON([("warehouse", "C"), ("qty", 5)])]},
    {"item": "paper",
     "instock": [
         SON([("warehouse", "A"), ("qty", 60)]),
         SON([("warehouse", "B"), ("qty", 15)])]},
    {"item": "planner",
     "instock": [
         SON([("warehouse", "A"), ("qty", 40)]),
         SON([("warehouse", "B"), ("qty", 5)])]},
    {"item": "postcard",
     "instock": [
         SON([("warehouse", "B"), ("qty", 15)]),
         SON([("warehouse", "C"), ("qty", 35)])]}])
