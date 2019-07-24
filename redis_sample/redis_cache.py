import redis
import json

r = redis.StrictRedis(host='localhost', port=6379, db=1)

key = 'aaa'
data = {'key1': 'value1'}
time_expire = 100

r.setex(key, time_expire, json.dumps(data))

value = r.get(key)
value = value.decode('ascii')
print(type(value))
print(json.dumps(json.loads(value), indent=4, sort_keys=True))
