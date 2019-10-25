from multiprocessing import Process
import time
import redis
import json

timeout = 5


def pub(r):
    for n in range(10):
        r.publish('channel', 'blah %d' % n)
        time.sleep(1.5)
    return


def sub_listen(r, name):
    p = r.pubsub()
    p.subscribe(['channel'])
    for item in p.listen():
        print('%s : %s' % (name, item))


def sub_get_message(r, name):
    p = r.pubsub()
    p.subscribe(['channel'])
    start = time.time()
    while True:
        message = p.get_message()
        if message:
            print('%s : %s' % (name, message))
        time.sleep(0.01)
        if time.time() - start > timeout:
            print('timeout happened, stop!')
            return


if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost', port=6379, db=1)
    Process(target=pub, args=(r,)).start()
    Process(target=sub_listen, args=(r, 'reader1')).start()
    Process(target=sub_get_message, args=(r, 'reader2')).start()
