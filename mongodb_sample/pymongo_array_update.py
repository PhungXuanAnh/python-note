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
        $addToSet operator will check exist before append element into array
    """

    def add_v4_array1_v0_array2(self):
        collection.update(
            {'_id': 1},
            {'$addToSet': {'array1': "v4", 'array2': 'v0'}}
        )
        for item in collection.find():
            print("After data : ", item)

    def add_other_item(self):
        """
            Hàm này sẽ update một item, nếu item này không có thì sẽ insert 1 cái
            Item này không chỉ có array như sample data phía trên mà có thêm key
            khác mà ta muốn thêm vào item này 
        """
        collection.update_one(
            {'_id': 2},
            {'$addToSet': {'array1': "v0", 'array2': 'v0'}, "$set": {"key1": "value1"}},
            True
        )
        for item in collection.find():
            print("After data : ", item)
        collection.update_one(
            {'_id': 2},
            {'$addToSet': {'array1': "v1", 'array2': 'v1'}, "$set": {"key2": "value2"}},
            True
        )
        for item in collection.find():
            print("After data : ", item)


if __name__ == "__main__":
    insert_sample_data()

    rm = RemoveItem()
    # rm.remove_v1_v2_array1_v3_array2()

    update = AddItem()
    # update.add_v4_array1_v0_array2()
    update.add_other_item()
