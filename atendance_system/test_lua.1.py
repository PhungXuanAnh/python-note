"""
key: logged-in:yyyy-mm-dd
bit: 0-99
1: logged in
0: don't logged in

redis.setbit(logged-in:yyyy-mm-dd, user_id, 1)
"""

import redis
import random
import datetime


pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
client = redis.Redis(connection_pool=pool)
pipe = client.pipeline()

USER_NUMBER = 100


class LuaRedisClient(redis.Redis):

    def __init__(self, *args, **kargs):
        super(LuaRedisClient, self).__init__(*args, **kargs)
        for name, snippet in self._get_lua_funcs():
            self._create_lua_method(name, snippet)

    def _get_lua_funcs(self):
        """
            Return name/snippet pair for earch lua function in the atoms.lua file
        """
        with open('../redis_sample/lua-scripts/get_active_position.lua', 'r') as f:
            for func in f.read().strip().split('function '):
                if func:
                    bits = func.split('\n', 1)
                    name = bits[0].split('(')[0].strip()
                    snippet = bits[1].rsplit('end', 1)[0].strip()
                    yield name, snippet

    def _create_lua_method(self, name, snippet):
        """
            Registers the code snippet as a Lua script, and binds the script to the
            client as a method that can be called with the same signature as regular
            client methods, eg with a single key arg.
        """
        script = self.register_script(snippet)
        # method = lambda key, *a, **k: script(keys=[key], args=a, **k)

        def method(key, *a, **k):
            return script(keys=[key], args=a, **k)

        setattr(self, name, method)


def generate_attendance_randomly():
    client.flushall()
    date = datetime.datetime(2018, 1, 1)
    for _ in range(0, 31):
        rate_present = random.randint(70, 99)
        rate_attendance = [1] * rate_present + [0] * (100 - rate_present)
        for user_id in range(0, USER_NUMBER):
            client.setbit(name='logged-in:{}'.format(date.strftime("%Y-%m-%d")),
                          offset=user_id,
                          value=random.choice(rate_attendance))
        date = date + datetime.timedelta(days=1)


def print_attendance_every_day():
    current_date = datetime.datetime(2018, 1, 1)
    for _ in range(0, 31):
        next_date = current_date + datetime.timedelta(days=1)
        counts_present = []
        counts_absence = []

        for j in range(0, USER_NUMBER):
            if client.getbit('logged-in:{}'.format(current_date.strftime("%Y-%m-%d")), j):
                counts_present.append(j)
            else:
                counts_absence.append(j)

        present = client.bitcount('logged-in:{}'.format(current_date.strftime("%Y-%m-%d")))
        print('---------------- date: {}--------------'.format(current_date.strftime("%Y-%m-%d")))
        print('counts present: ', present)
        print('ids present: ', counts_present)
        print('counts absence: ', USER_NUMBER - present)
        print('ids absence: ', counts_absence)

        current_date = next_date


def print_attendance_consecutive_days():
    current_date = datetime.datetime(2018, 1, 1)
    client.set('logged-in:present_2_consecutive_days_sum', '')
    client.set('logged-in:absence_2_consecutive_days_sum', '')

    for _ in range(0, 31):
        next_date = current_date + datetime.timedelta(days=1)

        # calculate users present 2 consecutive days
        pipe.bitop('and',
                   'logged-in:present_2_consecutive_days',
                   'logged-in:{}'.format(current_date.strftime("%Y-%m-%d")),
                   'logged-in:{}'.format(next_date.strftime("%Y-%m-%d")))
        pipe.bitop('or',
                   'logged-in:present_2_consecutive_days_sum',
                   'logged-in:present_2_consecutive_days_sum',
                   'logged-in:present_2_consecutive_days')

        # calculate users absence 2 consecutive days
        pipe.bitop('OR',
                   'logged-in:absence_2_consecutive_days',
                   'logged-in:{}'.format(current_date.strftime("%Y-%m-%d")),
                   'logged-in:{}'.format(next_date.strftime("%Y-%m-%d")))
        pipe.bitop('not',
                   'logged-in:absence_2_consecutive_days',
                   'logged-in:absence_2_consecutive_days')
        pipe.bitop('or',
                   'logged-in:absence_2_consecutive_days_sum',
                   'logged-in:absence_2_consecutive_days_sum',
                   'logged-in:absence_2_consecutive_days')
        pipe.execute()

        current_date = next_date

    lua = """
        local str = redis.call("GET", KEYS[1]);
        local ids = {}

        for i = 1, #str do
            local byte = str:byte(i)

            for j = 0, 7 do
                if (bit.band(byte, 2^(7-j)) ~= 0) then
                    ids[#ids + 1] = j + (i-1)*8
                end
            end
        end

        return ids
    """
    multiply = client.register_script(lua)
   
    print('counts_present_2_consecutive_days: ', client.bitcount('logged-in:present_2_consecutive_days_sum'))
    print('ids present 2 consecutive days: ', multiply(keys=['logged-in:present_2_consecutive_days_sum']))

    print('counts_absence_2_consecutive_days: ', client.bitcount('logged-in:absence_2_consecutive_days_sum'))
    print('ids absence 2 consecutive days: ', multiply(keys=['logged-in:absence_2_consecutive_days_sum']))


if __name__ == '__main__':
    generate_attendance_randomly()
    # print_attendance_every_day()
    print_attendance_consecutive_days()
