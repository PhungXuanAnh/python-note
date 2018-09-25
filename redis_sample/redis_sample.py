import redis

# it will create its own connection
r = redis.StrictRedis(host='localhost', port=6379, db=1)
r.set('set2', 'bar')
print(r.get('set2'))

# using 1 connection for multiple client
pool = redis.ConnectionPool(host='localhost', port=6379, db=2)
r = redis.Redis(connection_pool=pool)
r.set('set1', 'set1value')

# using pipeline to call multi command to server
pool = redis.ConnectionPool(host='localhost', port=6379, db=3)
r = redis.Redis(connection_pool=pool)
r.set('bing', 'baz')
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