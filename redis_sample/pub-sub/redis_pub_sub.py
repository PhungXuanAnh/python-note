from multiprocessing import Process
import time
import redis
import json
import traceback

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


def sub_get_message(r, name, timeout=None):
    p = r.pubsub()
    p.subscribe(['channel'])
    start = time.time()
    while True:
        message = p.get_message()
        if message:
            print('%s : %s' % (name, message))
        time.sleep(0.01)
        if timeout and time.time() - start > timeout:
            print('Cannot get publish message from redis. Timeout happened: {}s'.format(timeout))
            return None


class RedisPubSub(object):
    """
        This class handler redis pub/sub functions, it will continually retry to connect server,
        if connection lost
    """

    def __init__(self, host, port, db, channel):
        self.channel = channel
        self.pool = redis.ConnectionPool(host=host, port=port, db=db)
        self._connect()

    def _connect(self, next_handler=None, handler_args={}):
        self._redis = redis.Redis(connection_pool=self.pool)
        while True:
            try:
                self._redis.ping()
                if next_handler:
                    return next_handler(**handler_args)
                break
            except redis.exceptions.ConnectionError:
                traceback.print_exc()
                print('Cannot connect to Redis, retrying...')
            except Exception:
                traceback.print_exc()
            time.sleep(1)

    def pub(self, current_number=0):
        try:
            for n in range(current_number, 100):
                self._redis.publish(self.channel, 'blah %d' % n)
                print('publishing message {}'.format(n))
                time.sleep(1)
            print('Publisher stopped')
            return
        except redis.exceptions.ConnectionError:
            self._connect(self.pub, {'current_number': n})
        except Exception:
            traceback.print_exc()

    def sub_listen(self, name):
        try:
            p = self._redis.pubsub()
            p.subscribe([self.channel])
            for message in p.listen():
                if message['type'] == 'message':
                    print('%s : %s' % (name, message))
                    # return message['data']
            print('{} stopped'.format(name))
        except redis.exceptions.ConnectionError:
            return self._connect(self.sub_listen, {'name': name})
        except Exception:
            traceback.print_exc()

    def sub_get_message(self, name, timeout=None):
        try:
            p = self._redis.pubsub()
            p.subscribe([self.channel])
            start = time.time()
            while True:
                message = p.get_message()
                if message and message['type'] == 'message':
                    print('%s : %s' % (name, message))
                    # return message['data']
                time.sleep(0.01)
                if timeout and time.time() - start > timeout:
                    print('================================{} stopped. Timeout happened: {}s'.format(name, timeout))
                    return None
            print('============================ {} stopped'.format(name))
        except redis.exceptions.ConnectionError:
            return self._connect(self.sub_get_message, {'name': name, 'timeout': timeout})
        except Exception:
            traceback.print_exc()


if __name__ == '__main__':
    # r = redis.StrictRedis(host='localhost', port=6379, db=1)
    # Process(target=pub, args=(r,)).start()
    # Process(target=sub_listen, args=(r, 'reader1')).start()
    # Process(target=sub_get_message, args=(r, 'reader2')).start()

    r_handler = RedisPubSub('localhost', 6379, 0, 'test')
    Process(target=r_handler.pub).start()
    Process(target=r_handler.sub_listen, args=('reader1',)).start()
    Process(target=r_handler.sub_get_message, args=('reader2', 11,)).start()
