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
            {"_id": 1, "name": "A", "hours": 80, "resources": 10, 'OT': 3},
            {"_id": 2, "name": "B", "hours": 40, "resources": 40, 'OT': 1},
            {"_id": 3, "name": "C", "hours": 30, "resources": 41, 'OT': 2},
            {"_id": 4, "name": "D", "hours": 20, "resources": 24, 'OT': 1},
            {"_id": 5, "name": "E", "hours": 40, "resources": 67, 'OT': 4},
            {"_id": 6, "name": "F", "hours": 45, "resources": 89, 'OT': 5},
            {"_id": 7, "name": "G", "hours": 60, "resources": 90, 'OT': 2},
            {"_id": 8, "name": "H", "hours": 40, "resources": 51, 'OT': 1},
            {"_id": 9, "name": "I", "hours": 40, "resources": 42, 'OT': 1},
        ])

    def divide_8(self):
        " Chia cho 8 để tính toán số ngày làm việc"
        for item in collection.aggregate(
            [
                {'$project': {'name': 1, 'workdays': {'$divide': ["$hours", 8]}}}
            ]
        ):
            print("Số ngày làm việc  :", item)
        print('------------------------------------------------------------')

    def divide_between_fields(self):
        """
            Chia hours cho resource để tính số giờ trung bình cần làm ra 1 resource
            và sắp xếp trường này theo thứ tự giảm dần  
        """
        for item in collection.aggregate(
            [
                {'$project': {'name': 1, 'average_performance': {'$divide': ["$hours", "$resources"]}}},
                {"$sort": {"average_performance": pymongo.DESCENDING}}
            ]
        ):
            print("average  :", item)
        print('------------------------------------------------------------')

    def sum_hour_OT(self):
        """
            Tính tổng số giờ làm việc bao gồm cả OT
        """
        for item in collection.aggregate(
            [
                {'$project': {'name': 1, 'sum_working_hour': {'$sum': ["$hours", "$OT"]}}},
                {"$sort": {"sum_working_hour": pymongo.DESCENDING}}
            ]
        ):
            print("Tổng số giờ làm việc  :", item)
        print('------------------------------------------------------------')

    def sum_hour_then_div_resource(self):
        """
            Tính tổng số giờ làm việc, sau đó chia cho số tài nguyên để tính số giờ trung bình
            làm ra 1 tài nguyên
        """
        for item in collection.aggregate(
            [
                {'$project': {'name': 1, 'average': {'$divide': [{'$sum': ["$hours", "$OT"]}, "$resources"]}}},
                {"$sort": {"average": pymongo.DESCENDING}}
            ]
        ):
            print("AVERAGE  :", item)
        print('------------------------------------------------------------')


if __name__ == "__main__":
    operator = Aggregation_Divide()
    operator.divide_8()
    operator.divide_between_fields()
    operator.sum_hour_OT()
    operator.sum_hour_then_div_resource()
