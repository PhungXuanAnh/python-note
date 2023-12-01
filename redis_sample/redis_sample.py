import redis
import json

r = redis.StrictRedis(host='localhost', port=6379, db=1)
def connect_directly():
    r0 = redis.StrictRedis(host='localhost', port=6379, db=1)
    print(r0.set('set2', 'bar'))
    print(r0.set('set2', 'value', px=5000, nx=True))    # create key if not exists
    print(r0.get('set2'))
    print('--------------------')
    print(r0.set('set1', 'value', px=5000, nx=True))    # create key if not exists
    print(r0.get('set1'))
    print(r0.get('not exist key'))

def connect_using_pool():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=2)
    r1 = redis.Redis(connection_pool=pool)
    r1.set('pool_sample', 'this is value of pool sample key')
    print(r1.get('pool_sample'))

def pipeline():
    # using pipeline to call multi command to server
    pool = redis.ConnectionPool(host='localhost', port=6379, db=3)
    r2 = redis.Redis(connection_pool=pool)
    r2.set('bing', 'baz')
    # Use the pipeline() method to create a pipeline instance
    pipe = r.pipeline()
    # The following SET commands are buffered
    pipe.set('foo', 'bar')
    pipe.get('bing')
    # the EXECUTE call sends all buffered commands to the server, returning
    # a list of responses, one for each command.
    print(pipe.execute())
    # or combine all above command in one
    print(pipe.set('foo', 'bar').sadd('faz', 'baz').incr('auto_number').execute())                  

def set_bit():
    r.setbit('set_bit_sample', 3, 1)
    print(r.get('set_bit_sample'))

def check_key_exist():
    print(r.exists('unknow_key'))
    
    r.set("know_key", "value")
    print(r.exists('know_key'))

def save_a_dict():
    mydict = { 'var1' : 5, 'var2' : 9, 'var3': [1, 5, 9] }
    key = "save_a_dict"
    r.set(key, json.dumps(mydict))
    print(r.get(key))
    print(json.loads(r.get(key)))


if __name__ == "__main__":
    connect_directly()
    # connect_using_pool()
    # pipeline()
    # set_bit()
    # check_key_exist()
    # save_a_dict()