import redis
import random
import bitstring
import time


def byte2hex(byteStr):
    return ''.join(["% 02X " % ord(x) for x in byteStr]).strip('').replace(' ', '')


def popcount(redis, bitkey):
    a = bin(int(byte2hex(r.get(bitkey)), 16))[2:]
    return a.count('1')


def random_user_offset():
    uid = random.randint(0, 10000000)
    visit = int(round(random.betavariate(1, 1), 0))
    return [uid, visit]


if __name__ == '__main__':

    r = redis.StrictRedis()
    r.delete('daily_active_users')

    ar = []
    start_time = time.time()
    for i in range(100):
        res = random_user_offset()
        # print(res)
        r.setbit('daily_active_users', int(res[0]), int(res[1]))
        ar.append(res[1])

    print(time.time() – start_time, 'seconds')
    print(sum(ar))
    print(popcount(r, 'daily_active_users'))
    print(time.time() – start_time, 'seconds')
