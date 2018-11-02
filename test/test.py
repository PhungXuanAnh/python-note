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

    counts_present_2_consecutive_days = list()
    counts_absence_2_consecutive_days = list()

    for j in range(0, USER_NUMBER):
        if client.getbit('logged-in:present_2_consecutive_days_sum', j):
            counts_present_2_consecutive_days.append(j)

        if client.getbit('logged-in:absence_2_consecutive_days_sum', j):
            counts_absence_2_consecutive_days.append(j)

    print('-------------------statistic 2 consecutive days ----------------------')
    print('counts_present_2_consecutive_days: ', len(counts_present_2_consecutive_days))
    print('ids present 2 consecutive days: ', counts_present_2_consecutive_days)
    print('counts_absence_2_consecutive_days: ', len(counts_absence_2_consecutive_days))
    print('id absence 2 consecutive days: ', counts_absence_2_consecutive_days)


if __name__ == '__main__':
    # generate_attendance_randomly()
    # print_attendance_every_day()
    print_attendance_consecutive_days()
