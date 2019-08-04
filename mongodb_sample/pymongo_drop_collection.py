import pymongo

client = pymongo.MongoClient('localhost', 27017)

db = client['brandlytic-spark']

collection = db['69051_mytam.info_color']

collection.drop()

client.close()
