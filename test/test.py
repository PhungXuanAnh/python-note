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

PRESENT_STATUS = 1
ABSENCE_STATUS = 0


def get_redis_client():
    client = redis.StrictRedis(host='localhost', port=6379, db=1)
    try:
        client.ping()
        return client
    except redis.ConnectionError:
        print('Error while connect to Redis server')
        return None


def genrate_rate_attendance_randomly():
    rate_present = random.randint(70, 99)
    return [PRESENT_STATUS] * rate_present + [ABSENCE_STATUS] * (100 - rate_present)


def generate_attendance_randomly(year, month, day, number_users):
    if number_users <= 0:
        print('number_users must be unsigned integer')
        return False

    try:
        date = datetime.datetime(year, month, day).strftime("%Y-%m-%d")
        key_name = 'attendance:{}'.format(date)
    except Exception as e:
        print("You entered invalid date: {}".format(e))
        return False

    r_client = get_redis_client()
    if not r_client:
        print("Can not connect to redis server")
        return False

    rate_attendance = genrate_rate_attendance_randomly()

    for user_id in range(0, number_users):
        r_client.setbit(name=key_name,
                        offset=user_id,
                        value=random.choice(rate_attendance))
    return True


def get_attendance_a_day(number_users, year, month, day):
    if number_users <= 0:
        print("number_users must be an unsigned integer")
        return None

    try:
        date = datetime.datetime(year, month, day).strftime("%Y-%m-%d")
        key_name = 'attendance:{}'.format(date)
    except Exception as e:
        print("You entered invalid date: {}".format(e))
        return None

    r_client = get_redis_client()
    if not r_client:
        print("Can not connect to redis server")
        return None

    if not r_client.exists(key_name):
        print("Data of day {} does not exist".format(date))
        return None

    ids_present = []
    ids_absence = []

    for user_id in range(0, number_users):
        if r_client.getbit(key_name, user_id) == PRESENT_STATUS:
            ids_present.append(user_id)
        else:
            ids_absence.append(user_id)
    return {
        "ids_present": ids_present,
        "ids_absence": ids_absence
    }


def get_attendance_consecutive_days(year, month, day, number_users):
    if number_users <= 0:
        print("number_users must be an unsigned integer")
        return None

    try:
        current_date = datetime.datetime(year, month, day)
        next_date = (current_date + datetime.timedelta(days=1))

        key_current_date = 'attendance:{}'.format(current_date.strftime("%Y-%m-%d"))
        key_next_date = 'attendance:{}'.format(next_date.strftime("%Y-%m-%d"))
    except Exception as e:
        print("You entered invalid date: {}".format(e))
        return None

    r_client = get_redis_client()
    if not r_client:
        return None

    # calculate users present 2 consecutive days
    r_client.bitop('AND',
                   'present_2_consecutive_days',
                   key_current_date,
                   key_next_date)

    # calculate users absence 2 consecutive days
    r_client.bitop('OR',
                   'absence_2_consecutive_days',
                   key_current_date,
                   key_next_date)

    ids_present_2_consecutive_days = []
    ids_absence_2_consecutive_days = []

    for user_id in range(0, number_users):
        if r_client.getbit('present_2_consecutive_days', user_id) == PRESENT_STATUS:
            ids_present_2_consecutive_days.append(user_id)

        if r_client.getbit('absence_2_consecutive_days', user_id) == ABSENCE_STATUS:
            ids_absence_2_consecutive_days.append(user_id)

    return {
        "present_ids": ids_present_2_consecutive_days,
        "absence_ids": ids_absence_2_consecutive_days
    }


if __name__ == '__main__':
    NUMBER_USERS = 100
    dates = [
        {
            "year": 2018,
            "month": 11,
            "day": 3
        },
        {
            "year": 2018,
            "month": 11,
            "day": 4
        }
    ]

    # -------------------- generate data -------------------------------------
    for date in dates:
        generate_attendance_randomly(year=date['year'],
                                     month=date['month'],
                                     day=date['day'],
                                     number_users=NUMBER_USERS)

    # ------------------------ statistic attendance every day ----------------
    for date in dates:
        result = get_attendance_a_day(number_users=NUMBER_USERS,
                                      year=date['year'],
                                      month=date['month'],
                                      day=date['day'])
        print('---------------- date: {}-{}-{}--------------'.format(date['year'], date['month'], date['day']))
        if result:
            print('counts present: ', len(result["ids_present"]))
            print('ids present: ', result["ids_present"])
            print('counts absence: ', len(result["ids_absence"]))
            print('ids absence: ', result["ids_absence"])
            print("")
        else:
            print('There is no data')

    print('-------------------statistic 2 consecutive days ----------------------')
    date = dates[0]
    result = get_attendance_consecutive_days(date['year'], date['month'], date['day'], NUMBER_USERS)
    if result:
        print('counts present 2 consecutive days: ', len(result['present_ids']))
        print('ids present 2 consecutive days: ', result['present_ids'])
        print('counts absence 2 consecutive days: ', len(result['absence_ids']))
        print('ids absence 2 consecutive days: ', result['absence_ids'])
    else:
        print("There is no data")
