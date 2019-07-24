import pymongo

client = pymongo.MongoClient('localhost', 27017)

db = client.test
# db = client['test']

print("db.name: {}".format(db.name))
print("db.my_collection: {}".format(db.my_collection))
print("db['my_collection']: {}".format(db['my_collection']))

# db.my_collection.insert_one({"x": 1}).inserted_id
# db.my_collection.insert_one({"x": 2}).inserted_id
# db.my_collection.insert_one({"x": 3}).inserted_id

item = db.my_collection.find_one()
print("get one document: {}".format(item['x']))

print('get all document -----------------------------')
for item in db.my_collection.find():
    print(item["x"])

print('create index and sort------------------------------------')
db.my_collection.create_index("x")

for item in db.my_collection.find().sort("x", pymongo.ASCENDING):
    print(item["x"])
