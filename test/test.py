"""
key: attendance:yyyy-mm-dd
bit: 0-99
1: present status
0: absence status

redis.setbit(attendance:yyyy-mm-dd, user_id, 1)
"""

import redis
import random
import datetime


pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
client = redis.Redis(connection_pool=pool)
pipe = client.pipeline()

USER_NUMBER = 100
DAY_NUMBER = 2

PRESENT_STATUS = 1
ABSENCE_STATUS = 0


def generate_attendance_randomly(number_days):
    if number_days == 0:
        return False

    date = datetime.datetime(2018, 1, 1)

    for _ in range(0, number_days):

        rate_present = random.randint(70, 99)
        rate_attendance = [PRESENT_STATUS] * rate_present + [ABSENCE_STATUS] * (100 - rate_present)

        for user_id in range(0, USER_NUMBER):
            client.setbit(name='attendance:{}'.format(date.strftime("%Y-%m-%d")),
                          offset=user_id,
                          value=random.choice(rate_attendance))

        date = date + datetime.timedelta(days=1)
    return True


def print_attendance_daily():
    current_date = datetime.datetime(2018, 1, 1)
    for _ in range(0, DAY_NUMBER):
        next_date = current_date + datetime.timedelta(days=1)
        ids_present = []
        ids_absence = []

        for user_id in range(0, USER_NUMBER):
            if client.getbit('attendance:{}'.format(current_date.strftime("%Y-%m-%d")), user_id) == PRESENT_STATUS:
                ids_present.append(user_id)
            else:
                ids_absence.append(user_id)

        present = client.bitcount('attendance:{}'.format(current_date.strftime("%Y-%m-%d")))
        print('---------------- date: {}--------------'.format(current_date.strftime("%Y-%m-%d")))
        print('counts present: ', present)
        print('ids present: ', ids_present)
        print('counts absence: ', USER_NUMBER - present)
        print('ids absence: ', ids_absence)
        print("")

        current_date = next_date


def print_attendance_consecutive_days():
    current_date = datetime.datetime(2018, 1, 1)
    client.set('sum_present_2_consecutive_days', '')
    client.set('sum_absence_2_consecutive_days', '')

    for _ in range(0, DAY_NUMBER):
        next_date = current_date + datetime.timedelta(days=1)

        # calculate users present 2 consecutive days
        pipe.bitop('and',
                   'present_2_consecutive_days',
                   'attendance:{}'.format(current_date.strftime("%Y-%m-%d")),
                   'attendance:{}'.format(next_date.strftime("%Y-%m-%d")))
        pipe.bitop('or',
                   'sum_present_2_consecutive_days',
                   'sum_present_2_consecutive_days',
                   'present_2_consecutive_days')

        # calculate users absence 2 consecutive days
        pipe.bitop('OR',
                   'absence_2_consecutive_days',
                   'attendance:{}'.format(current_date.strftime("%Y-%m-%d")),
                   'attendance:{}'.format(next_date.strftime("%Y-%m-%d")))
        pipe.bitop('not',
                   'absence_2_consecutive_days',
                   'absence_2_consecutive_days')
        pipe.bitop('or',
                   'sum_absence_2_consecutive_days',
                   'sum_absence_2_consecutive_days',
                   'absence_2_consecutive_days')
        pipe.execute()

        current_date = next_date

    ids_present_2_consecutive_days = list()
    ids_absence_2_consecutive_days = list()

    for user_id in range(0, USER_NUMBER):
        if client.getbit('sum_present_2_consecutive_days', user_id):
            ids_present_2_consecutive_days.append(user_id)

        if client.getbit('sum_absence_2_consecutive_days', user_id):
            ids_absence_2_consecutive_days.append(user_id)

    print('-------------------statistic 2 consecutive days ----------------------')
    print('counts present 2 consecutive days: ', len(ids_present_2_consecutive_days))
    print('ids present 2 consecutive days: ', ids_present_2_consecutive_days)
    print('counts absence 2 consecutive days: ', len(ids_absence_2_consecutive_days))
    print('ids absence 2 consecutive days: ', ids_absence_2_consecutive_days)


if __name__ == '__main__':
    generate_attendance_randomly()
    print_attendance_daily()
    print_attendance_consecutive_days()

    client.flushall()