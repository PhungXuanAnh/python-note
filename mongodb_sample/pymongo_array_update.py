import pymongo
import json

client = pymongo.MongoClient('localhost', 27017)

db = client.test
collection = db.test_update_array


def insert_sample_data():
    collection.drop()
    collection.insert([
        {
            '_id': 1,
            'array1': ["v1", "v2", "v3"],
            'array2': ["v1", "v2", "v3"]
        }
    ])
    for item in collection.find():
        # print(json.dumps(item, indent=4, sort_keys=True))
        print("Before data: ", item)


class RemoveItem(object):
    """"
        https://docs.mongodb.com/manual/reference/operator/update/pull/
    """

    def remove_v1_v2_array1_v3_array2(self):
        """[remove "value4", "value5" in array1, and "value0" in array2]
        """
        collection.update(
            {},
            {'$pull': {'array1': {'$in': ["v1", "v2"]}, 'array2': "v3"}},
            multi=True
        )
        for item in collection.find():
            print("After data : ", item)

    # --------------- other remove ( remove item that match condition...), see above link


class AddItem(object):
    """
        https://docs.mongodb.com/manual/reference/operator/update/addToSet/
    """

    def add_v4_array1_v0_array2(self):
        collection.update(
            {'_id': 1},
            {'$addToSet': {'array1': "v4", 'array2': 'v0'}}
        )
        for item in collection.find():
            print("After data : ", item)


if __name__ == "__main__":
    insert_sample_data()

    rm = RemoveItem()
    # rm.remove_v1_v2_array1_v3_array2()

    add = AddItem()
    add.add_v4_array1_v0_array2()
