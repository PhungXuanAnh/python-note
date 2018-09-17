import pymongo

client = pymongo.MongoClient('localhost', 27017)

db = client.test
print(db.name)
print(db.my_collection)

# db.my_collection.insert_one({"x": 1}).inserted_id
# db.my_collection.insert_one({"x": 2}).inserted_id
# db.my_collection.insert_one({"x": 3}).inserted_id

print(db.my_collection.find_one())

for item in db.my_collection.find():
    print(item["x"])
print('--------------------------------------------')
db.my_collection.create_index("x")

for item in db.my_collection.find().sort("x", pymongo.ASCENDING):
    print(item["x"])

print([item["x"] for item in db.my_collection.find().limit(2).skip(1)])