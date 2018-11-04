"""
Author: Phung Xuan Anh
"""

import redis
import random
import datetime

PRESENCE_STATUS = 1
ABSENCE_STATUS = 0
REDIS_CONFIGS = {'host': 'localhost', 'port': 6379, 'db': 1}


def get_redis_client(redis_configs):
    try:
        client = redis.StrictRedis(host=redis_configs["host"], port=redis_configs["port"], db=redis_configs["db"], socket_timeout=5)
        client.ping()
        return client
    except:
        print('Can not connect to redis server')
        return None


def generate_binary_string_randomly(length):
    if length < 0:
        print("length of string must be larger than 0")
        return None

    random_number = random.randint(0, 2**length - 1)
    _binary = format(random_number, 'b')
    binary = "0" * (length - len(_binary))
    binary = binary + _binary
    return binary


def generate_attendance_randomly(date, number_users):
    if number_users <= 0:
        print('number_users must be unsigned integer')
        return False

    try:
        date = datetime.datetime(date["year"], date["month"], date["day"]).strftime("%Y-%m-%d")
        key_name = 'attendance:{}'.format(date)
    except Exception as e:
        print("You entered invalid date: {}".format(e))
        return False

    r_client = get_redis_client(REDIS_CONFIGS)
    if not r_client:
        return False

    binary_str = generate_binary_string_randomly(number_users)
    print("Data of {} is {}".format(date, binary_str))

    for user_id in range(0, number_users):
        r_client.setbit(name=key_name,
                        offset=user_id,
                        value=int(binary_str[user_id]))
    return True


def get_attendance_a_day(date, number_users):
    if number_users <= 0:
        print("number_users must be an unsigned integer")
        return None

    try:
        date = datetime.datetime(date["year"], date["month"], date["day"]).strftime("%Y-%m-%d")
        key_name = 'attendance:{}'.format(date)
    except Exception as e:
        print("You entered invalid date: {}".format(e))
        return None

    r_client = get_redis_client(REDIS_CONFIGS)
    if not r_client:
        return None

    if not r_client.exists(key_name):
        print("Data of day {} does not exist".format(date))
        return None

    ids_presence = []
    ids_absence = []

    for user_id in range(0, number_users):
        if r_client.getbit(key_name, user_id) == PRESENCE_STATUS:
            ids_presence.append(user_id)
        else:
            ids_absence.append(user_id)
    return {
        "ids_presence": ids_presence,
        "ids_absence": ids_absence
    }


def get_attendance_consecutive_days(first_date, number_users):
    if number_users <= 0:
        print("number_users must be an unsigned integer")
        return None

    try:
        _first_date = datetime.datetime(first_date["year"], first_date["month"], first_date["day"])
        _second_date = (_first_date + datetime.timedelta(days=1))

        key_first_date = 'attendance:{}'.format(_first_date.strftime("%Y-%m-%d"))
        key_second_date = 'attendance:{}'.format(_second_date.strftime("%Y-%m-%d"))
    except Exception as e:
        print("You entered invalid date: {}".format(e))
        return None

    r_client = get_redis_client(REDIS_CONFIGS)
    if not r_client:
        return None

    if not r_client.exists(key_first_date) or not r_client.exists(key_second_date):
        print('Data of date {} or {} is not exist'.format(_first_date, _second_date))
        return None

    # calculate users presence 2 consecutive days
    r_client.bitop('AND',
                   'presence_2_consecutive_days',
                   key_first_date,
                   key_second_date)

    # calculate users absence 2 consecutive days
    r_client.bitop('OR',
                   'absence_2_consecutive_days',
                   key_first_date,
                   key_second_date)

    ids_presence_2_consecutive_days = []
    ids_absence_2_consecutive_days = []

    for user_id in range(0, number_users):
        if r_client.getbit('presence_2_consecutive_days', user_id) == PRESENCE_STATUS:
            ids_presence_2_consecutive_days.append(user_id)

        if r_client.getbit('absence_2_consecutive_days', user_id) == ABSENCE_STATUS:
            ids_absence_2_consecutive_days.append(user_id)

    # print(r_client.bitcount('presence_2_consecutive_days'))

    return {
        "ids_presence": ids_presence_2_consecutive_days,
        "ids_absence": ids_absence_2_consecutive_days
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

    print("\n_________________________ generate attendance system data ___________________________")
    for date in dates:
        generate_attendance_randomly(date=date,
                                     number_users=NUMBER_USERS)

    print("\n_________________________ statistic attendance each day _____________________________")
    for date in dates:
        result = get_attendance_a_day(date=date,
                                      number_users=NUMBER_USERS)
        print('-------------- date: {}-{}-{}-----------'.format(date['year'], date['month'], date['day']))
        if result:
            print('counts of presence: ', len(result["ids_presence"]))
            print('ids presence: ', result["ids_presence"])
            print('counts of absence: ', len(result["ids_absence"]))
            print('ids absence: ', result["ids_absence"])
            print("")
        else:
            print('There is no data')

    print('\n__________________________ statistic attendance on 2 consecutive days ______________________')
    result = get_attendance_consecutive_days(first_date=dates[0],
                                             number_users=NUMBER_USERS)
    if result:
        print('counts of presence on 2 consecutive days: ', len(result['ids_presence']))
        print('user id present on 2 consecutive days: ', result['ids_presence'])
        print('counts of absence on 2 consecutive days: ', len(result['ids_absence']))
        print('user id absent on 2 consecutive days: ', result['ids_absence'])
    else:
        print("There is no data")
