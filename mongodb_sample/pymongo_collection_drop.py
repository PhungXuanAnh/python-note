import pymongo
from mongo_url import AUTHEN_URL

# client = pymongo.MongoClient('localhost', 27018)
client = pymongo.MongoClient(AUTHEN_URL)

db = client['test_database']

collection = db['test_collection']

collection.drop()

client.close()
