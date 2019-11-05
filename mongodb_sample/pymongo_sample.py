import pymongo
from mongo_url import AUTHEN_URL

client = pymongo.MongoClient('localhost', 27018)
client = pymongo.MongoClient(AUTHEN_URL)
print(client.server_info())    # NOTE: this statement can be used to check connection to mongodb server

db = client.test_database
# db = client['test']

print("db.name: {}".format(db.name))
print("db.test_collection: {}".format(db.test_collection))
print("db['test_collection']: {}".format(db['test_collection']))

db.test_collection.drop()
db.test_collection.insert_one({"x": 1}).inserted_id
db.test_collection.insert_one({"x": 2}).inserted_id
db.test_collection.insert_one({"x": 3}).inserted_id

item = db.test_collection.find_one()
print("get one document: {}".format(item['x']))

print('get all document -----------------------------')
for item in db.test_collection.find():
    print(item["x"])

print('create index and sort------------------------------------')
db.test_collection.create_index("x")

for item in db.test_collection.find().sort("x", pymongo.ASCENDING):
    print(item["x"])
