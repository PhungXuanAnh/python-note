from multiprocessing import Process
import time
import redis
import json


channel1 = 'test'


def pub(r):
    for n in range(10):
        r.publish(channel1, json.dumps({'value': n}))
        time.sleep(1)

    
r = redis.StrictRedis(host='localhost', port=6379, db=10)

pub(r)
