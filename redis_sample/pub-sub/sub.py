from multiprocessing import Process
import time
import redis
import json

channel1 = 'test'


def sub(r, name):
    pubsub = r.pubsub()
    pubsub.subscribe([channel1])
    for item in pubsub.listen():
        print('%s : %s' % (name, item['data']))
        if item['data'] == b'5':
            pubsub.unsubscribe()


r = redis.StrictRedis(host='localhost', port=6379, db=10)

Process(target=sub, args=(r, 'reader1')).start()
Process(target=sub, args=(r, 'reader2')).start()
sub(r, 'reader0')
