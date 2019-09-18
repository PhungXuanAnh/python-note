"""
https://docs.mongodb.com/manual/reference/operator
"""
import json
import pymongo
from utils import ObjectIdEncoder


client = pymongo.MongoClient('localhost', 27017)

db = client.test
collection = db.test_operator


def insert_sample_data(data):
    collection.drop()
    collection.insert_many(data)
    for item in collection.find():
        # print("Before data: ", json.dumps(item, indent=4, sort_keys=True, cls=ObjectIdEncoder))
        item.pop('_id')
        print("Sample data  :", item)
    print('------------------------------------------------------------')


class Aggregation_Divide(object):
    """
        https://docs.mongodb.com/manual/reference/operator/aggregation/divide/
    """

    def __init__(self):
        insert_sample_data([
            {"_id": 1, "name": "A", "hours": 80, "resources": 10},
            {"_id": 2, "name": "B", "hours": 40, "resources": 4}
        ])

    def divide_8(self):
        " Chia cho 8 để tính toán số giờ làm việc "
        for item in collection.aggregate(
            [
                {'$project': {'name': 1, 'workdays': {'$divide': ["$hours", 8]}}}
            ]
        ):
            print("Output data  :", item)

    def divide_between_fields(self):
        " Chia hours cho resource để tính số giờ trung bình cần làm ra 1 resource "
        for item in collection.aggregate(
            [
                {'$project': {'name': 1, 'average_performance': {'$divide': ["$hours", "$resources"]}}}
            ]
        ):
            print("Output data  :", item)


if __name__ == "__main__":
    operator = Aggregation_Divide()
    # operator.divide_8()
    operator.divide_between_fields()