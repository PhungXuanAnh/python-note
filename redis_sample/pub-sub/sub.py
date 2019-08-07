from multiprocessing import Process
import time
import redis
import json


def sub(r, name):
    pubsub = r.pubsub()
    pubsub.subscribe(['channel'])
    for item in pubsub.listen():
        print('%s : %s' % (name, item['data']))


r = redis.StrictRedis(host='localhost', port=6379, db=10)

Process(target=sub, args=(r, 'reader1')).start()
Process(target=sub, args=(r, 'reader2')).start()
sub(r, 'reader0')
