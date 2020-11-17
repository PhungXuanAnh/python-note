"""
https://docs.mongodb.com/manual/tutorial/query-arrays/
"""
import json
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
import pymongo
import random
import time
import threading
from utils import ObjectIdEncoder
from url import AUTHEN_URL
import traceback


client = pymongo.MongoClient('localhost', 27017)
# client = pymongo.MongoClient(AUTHEN_URL)

db = client.test_database
collection = db.test_collection


class TransactionExample(object):

    def __init__(self):
        collection.drop()
        for i in range(0, 3):
            collection.insert_one(
                {
                    "_id": i,
                    "age": random.choice(range(1, 100)),
                    "name": random.choice(['Anh', 'Hoa', 'Nghia', 'Phuc', 'Hieu']),
                }
            )
        for item in collection.find({}, {'_id': False}):
            print("Sample data: ", item)
        print('------------------------------------------------------------')

    def causally_consistent_read(self, sleep_time=1):
        # Refer: https://api.mongodb.com/python/current/api/pymongo/client_session.html#transactions
        with client.start_session() as session:
            collection.update_one(
                {'_id': 0},
                {'$set': {'name': "bbbbbbbbbbbbbbbbbbb", 'age': 22222222222222222}},
                session=session
            )
            time.sleep(sleep_time)

        for item in collection.find():
            print("After causally_consistent_read: ", item)
        print('------------------------------------------')


    def callback(self, session, custom_arg, name=None, age=0, sleep_time=1):
            print("======================= custom_arg: {}".format(custom_arg))
            print("======================= name: {}".format(name))
            print("======================= age: {}".format(age))

            collection.update_one(
                {'_id': 0},
                {'$set': {'name': name}},
                session=session
            )
            time.sleep(sleep_time)

    def run_transaction_callback(self, sleep_time=1):
        # Refer: https://api.mongodb.com/python/current/api/pymongo/client_session.html#classes
        # part: with_transaction

        with client.start_session() as session:
            session.with_transaction(lambda s: self.callback(s, "custom_arg", name="----------> run_transaction_callback", sleep_time=sleep_time))

        for item in collection.find():
            print("run_transaction_callback : ", item)
        print('------------------------------------------')

    def run_transaction(self, name, sleep_time):
        print("======================== {}".format(name))
        try:
            with client.start_session() as session:
                with session.start_transaction():
                    collection.update_one(
                        {'_id': 0},
                        {'$set': {'name': name}},
                        session=session
                    )

                time.sleep(sleep_time)

                # NOTE: cannot get proper result here 
                for item in collection.find():
                    print("run_transaction : ", item)
                print('------------------------------------------')
        except:
            traceback.print_exc()

    def test_block_write(self):
        """
            
        """
        trans_sleep_time = 3
        threading.Thread(target=self.run_transaction_callback, args=[trans_sleep_time]).start()
        # threading.Thread(target=self.run_transaction, args=["---------> run_transaction", trans_sleep_time]).start()

        # this below code in main thread cannot modify database because transaction blocked collection
        time.sleep(1)
        collection.update_one(
            {'_id': 0},
            {'$set': {'name': "---------------> test_block_write:"}},
        )
        time.sleep(5)

        # print out final data
        for item in collection.find():
            print("test_block_write: ", item)
        print('------------------------------------------')

    def test_transaction_error_and_retry(self):
        """
            This method for test and fix error:
                pymongo.errors.OperationFailure: WriteConflict, full error: {'errorLabels': ['TransientTransactionError'], 'operationTime': Timestamp(1605596737, 86), 'ok': 0.0, 'errmsg': 'WriteConflict', 'code': 112, 'codeName': 'WriteConflict', '$clusterTime': {'clusterTime': Timestamp(1605596737, 86), 'signature': {'hash': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', 'keyId': 0}}}
                2 reasons cause this error:
                - maxTransactionLockRequestTimeoutMillis, see: https://developpaper.com/solve-the-problem-of-mongodb-transaction-writeconflict/
                - all of your transactions modify the same document

            There are still some others error, see here for how to retry transaction: 
            https://docs.mongodb.com/manual/core/transactions-in-applications/#transactions-retry
            https://docs.mongodb.com/manual/reference/method/Session.commitTransaction/#retryable
        """
        def run_start_transaction(name):
            try:
                with client.start_session() as session:
                    with session.start_transaction():
                        collection.update_one(
                            {'_id': 0},
                            {'$set': {'name': name}},
                            session=session
                        )
            except:
                # NOTE: when run start_transaction(), below error can arise:
                # pymongo.errors.OperationFailure: WriteConflict
                # to fix this error, using with_transaction() method
                traceback.print_exc()

        def test_callback(session, name):
            collection.update_one(
                {'_id': 0},
                {'$set': {'name': name}},
                session=session
            )

        def run_with_transaction_callback(name):
            try:
                with client.start_session() as session:
                    session.with_transaction(lambda s: test_callback(s, name=name))
            except:
                traceback.print_exc()

        number_thread = 10
        pool = ThreadPool(number_thread)
        
        results = pool.map_async(run_start_transaction, range(0, 1000))            # <---------- this cause OperationFailure: WriteConflict
        # results = pool.map_async(run_with_transaction_callback, range(0, 1000))  # <---------- this fix above error, read more about with_transaction
                                                                                    # for more detail how it can fix this error: 
                                                                                    # https://api.mongodb.com/python/current/api/pymongo/client_session.html#with_transaction

        results.wait()  # blocking


if __name__ == "__main__":
    transaction_example = TransactionExample()
    # transaction_example.run_transaction()
    # transaction_example.causally_consistent_read()
    # transaction_example.test_block_write()
    transaction_example.test_call_multiple_transaction()
