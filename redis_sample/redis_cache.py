import redis
import json

r = redis.StrictRedis(host='localhost', port=6379, db=1)

key = 'aaa'
data = {'key1': 'value1'}
time_expire = 10

r.setex(key, time_expire, json.dumps(data))

print(r.get(key))
