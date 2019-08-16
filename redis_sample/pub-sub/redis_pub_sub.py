from multiprocessing import Process
import time
import redis
import json


def pub(r):
    for n in range(10):
        r.publish('channel', 'blah %d' % n)
        time.sleep(5)


def sub(r, name):
    pubsub = r.pubsub()
    pubsub.subscribe(['channel'])
    for item in pubsub.listen():
        print('%s : %s' % (name, item['data']))


if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost', port=6379, db=1)
    Process(target=pub, args=(r,)).start()
    Process(target=sub, args=(r, 'reader1')).start()
    Process(target=sub, args=(r, 'reader2')).start()
