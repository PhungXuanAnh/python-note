"""
Redis is an in-memory datastructure server. It has facility to manipulate
bitstrings in their Strings datastructure. There are 100 users. Some of them
come to the office, some are absent on any particular day. Everyday they
come, they log-in to an attendance system. We have to know how many users
logged-in on a particular day. Please use Redis Bitstrings to find a solution and
code it (Python or GO) so that in real time we can query how many users (out
of 100) have logged in till now and print their ids.
We are also interested in knowing all the users who came on consecutive days
and those who were absent on two consecutive days. Please write the code
and test cases so that you generate 100 users attendance randomly on both
days and print out
- the total counts of presence each day (along with their ids)
- the total count of absence each day (along with their ids)
- the total count of users who were present on two consecutive days (along
with their ids)
- the total count of users who were absent on two consecutive days (along
with their ids)

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
redis_cli = redis.Redis(connection_pool=pool)


def generate_attendance_randomly():
    date = datetime.datetime(2018, 1, 1)
    for i in range(0, 31):
        for user_id in range(0, 99):
            redis_cli.setbit(name='logged-in:{}'.format(date.strftime("%Y-%m-%d")), offset=user_id, value=random.choice([1, 1, 1, 0]))
        date = date + datetime.timedelta(days=1)


def print_output():
    counts_present_2_consecutive_days = set()
    counts_absence_2_consecutive_days = set()

    date = datetime.datetime(2018, 1, 1)
    for _ in range(0, 30):
        next_date = date + datetime.timedelta(days=1)
        counts_present = []
        counts_absence = []

        redis_cli.bitop('AND',
                        'logged-in:present',
                        'logged-in:{}'.format(date.strftime("%Y-%m-%d")),
                        'logged-in:{}'.format(next_date.strftime("%Y-%m-%d")))

        redis_cli.bitop('OR',
                        'logged-in:absence',
                        'logged-in:{}'.format(date.strftime("%Y-%m-%d")),
                        'logged-in:{}'.format(next_date.strftime("%Y-%m-%d")))

        for j in range(0, 100):
            if redis_cli.getbit('logged-in:{}'.format(date.strftime("%Y-%m-%d")), j):
                counts_present.append(j)
            else:
                counts_absence.append(j)
            
            if redis_cli.getbit('logged-in:present', j):
                counts_present_2_consecutive_days.add(j)

            if not redis_cli.getbit('logged-in:absence', j):
                counts_absence_2_consecutive_days.add(j)

        present = redis_cli.bitcount('logged-in:{}'.format(date.strftime("%Y-%m-%d")))
        print('---------------- date: {}--------------'.format(date.strftime("%Y-%m-%d")))
        print('counts present: ', present)
        print('ids present: ', counts_present)
        print('counts absence: ', 100 - present)
        print('ids absence: ', counts_absence)                      

        date = next_date
    print('counts_present_2_consecutive_days: ', counts_present_2_consecutive_days)
    print('counts_absence_2_consecutive_days: ', counts_absence_2_consecutive_days)


if __name__ == '__main__':
    # generate_attendance_randomly()
    print_output()

# key1 = 0101
# key2 = 1100
# key1 and key2 = 0100
# key1 or key 2 = 1101

# setbit key1 1 0
# setbit key1 2 1
# setbit key1 3 0
# setbit key1 4 1

# setbit key2 1 1
# setbit key2 2 1
# setbit key2 3 0
# setbit key2 4 0
