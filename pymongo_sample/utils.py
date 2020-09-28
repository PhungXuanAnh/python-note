import json
from bson import ObjectId
from bson.timestamp import Timestamp as BsonTimestamp

class ObjectIdEncoder(json.JSONEncoder):
    # https://api.mongodb.com/python/current/api/bson/objectid.html
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class BsonTimestampEncoder(json.JSONEncoder):
    # https://api.mongodb.com/python/current/api/bson/timestamp.html
    def default(self, o):
        if isinstance(o, BsonTimestamp):
            return o.as_datetime().strftime("[%Y-%m-%d]-[%H:%M:%S]")
        return json.JSONEncoder.default(self, o)

