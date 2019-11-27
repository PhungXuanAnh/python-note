from multiprocessing import Process
import time
import redis
import json

channel1 = 'test'


def sub1(r, name):
    pubsub = r.pubsub()
    pubsub.subscribe([channel1])
    for item in pubsub.listen():
        print('%s : %s' % (name, item))
        if item['data'] == b'{"value": 5}':
            pubsub.unsubscribe()
            return item['data'].decode()


def sub2(r, name):
    pubsub = r.pubsub()
    pubsub.subscribe([channel1])
    while True:
        message = pubsub.get_message()
        print('%s : %s' % (name, message))
        if message and message['data'] == b'{"value": 5}':
            break
        time.sleep(1)
    return message


r = redis.StrictRedis(host='localhost', port=6379, db=10)

Process(target=sub1, args=(r, 'reader01')).start()
result = sub2(r, 'reader02')
result = sub1(r, 'reader10')
print('result: {}'.format(result))
print(type(result))
