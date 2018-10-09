import redis
pool = redis.ConnectionPool(host='localhost', port=6379, db=2)
client = redis.Redis(connection_pool=pool)
pipe = client.pipeline()


def convert_to_binary(b_str):
    try:
        return convert_redis_str_to_binary_str(b_str.decode())
    except:
        return convert_hex_to_binary(str(b_str)[2:-1].replace('\\', '0'))


def convert_redis_str_to_binary_str(s):
    bitmap = ""
    for c in s:
        x = ord(c)
        str = bin(x).split('b')[1]
        if len(str) < 8:
            str = '0' * (8 - len(str)) + str
        bitmap += str
    return bitmap


def convert_hex_to_binary(hex_str):
    scale = 16  # equals to hexadecimal
    num_of_bits = 8
    return bin(int(hex_str, scale))[2:].zfill(num_of_bits)


def create_data():
    #        01234567
    # key1 = 11001100
    # key2 = 00101011

    # and = 00001000
    # or = 01101111
    # xor = 01100111
    # not = 10110011

    client.flushall()
    pipe.setbit('key1', 0, 1)
    pipe.setbit('key1', 1, 1)
    pipe.setbit('key1', 4, 1)
    pipe.setbit('key1', 5, 1)

    pipe.setbit('key2', 2, 1)
    pipe.setbit('key2', 7, 1)
    pipe.setbit('key2', 4, 1)
    pipe.setbit('key2', 6, 1)
    pipe.execute()


def print_data():
    print(client.get('key1'))
    print(client.get('key2'))
    print(convert_to_binary(client.get('key1')))
    print(convert_to_binary(client.get('key2')))


def bitop_sample():
    pipe.bitop('and', 'key_and', 'key1', 'key2')
    pipe.bitop('or', 'key_or', 'key1', 'key2')
    pipe.bitop('xor', 'key_xor', 'key1', 'key2')
    pipe.bitop('not', 'key_not', 'key1')
    pipe.execute()
    print(client.get('key_and'))
    print(convert_to_binary(client.get('key_and')))
    print(client.get('key_or'))
    print(convert_to_binary(client.get('key_or')))
    print(client.get('key_xor'))
    print(convert_to_binary(client.get('key_xor')))
    print(client.get('key_not'))
    print(convert_to_binary(client.get('key_not')))


def bitop_sample1():
    #         01234567
    key11 = [1, 0, 1, 0, 1, 0, 1, 0]
    key12 = [1, 1, 0, 0, 1, 1, 0, 1]

    for i in range(0, 8):
        client.setbit('key11', i, key11[i])
        client.setbit('key12', i, key12[i])
    print('key11: ', convert_to_binary(client.get('key11')))
    print('key12: ', convert_to_binary(client.get('key12')))

    client.bitop('xor', 'key11', 'key11', 'key12')
    print('xor11: ', convert_to_binary(client.get('key11')))

    client.delete('key11', 'key12')


def bitpos_sample():
    print(client.bitpos('key1', 1))
    print(client.bitpos('key2', 0))
    print(client.bitpos('key100', 1))


def lua_sample():
    lua = """
        local value = redis.call('GET', KEYS[1])
        value = tonumber(value)
        return value * ARGV[1]
        """
    multiply = client.register_script(lua)
    client.set('foo', 2)
    print(multiply(keys=['foo'], args=[5]))


if __name__ == '__main__':
    # create_data()
    # print_data()
    # bitop_sample()
    # bitop_sample1()
    # bitpos_sample()
    lua_sample()