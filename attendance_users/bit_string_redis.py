from redis import StrictRedis, exceptions
import traceback
from redis_config import REDIS
import random

USERS = 100


def get_redis():
    try:
        r = StrictRedis(host=REDIS['host'], port=REDIS['port'], db=REDIS['db'])
        if r.ping():
            return r
    except:
        pass
        # traceback.print_exc()
    return None


def init_user_ids():
    '''
    generate user ids from 0 to n
    '''
    user_ids = []
    for i in xrange(0, USERS):
        user_ids.append(i)
    return user_ids


def init_data_a_day(user_ids, day):
    '''
    random users visit company one day
    bit 1: presence
    bit 0: absence
    '''
    r = get_redis()
    if r is None:
        return False
    elif user_ids is None or len(user_ids) == 0 or day is None or day == '':
        return False
    else:
        try:
            r.delete(day)
            for i in user_ids:
                r.setbit(day, i, random.randrange(0, 2))
        except:
            traceback.print_exc()
            return False
    return True


def get_present_users_a_day(user_ids, day):
    if user_ids is None or len(user_ids) == 0 or day is None or day == '':
        return None
    try:
        r = get_redis()
        if r is None or r.exists(day) is False:
            return None
        data = get_bits(user_ids, day)
        return get_all_postion_by_bit_value(data, 1)
    except:
        traceback.print_exc()
    return None


def get_absent_users_a_day(user_ids, day):
    if user_ids is None or len(user_ids) == 0 or day is None or day == '':
        return None
    try:
        r = get_redis()
        if r is None or r.exists(day) is False:
            return None
        data = get_bits(user_ids, day)
        return get_all_postion_by_bit_value(data, 0)
    except:
        traceback.print_exc()
    return None


def present_users_consecutive_days(user_ids, keys):
    if user_ids is None or len(user_ids) == 0 or keys is None or type(keys) is not list or len(keys) == 0:
        return None
    try:
        r = get_redis()
        if r is None:
            return None
        dest_key = 'present_users_consecutive_days'
        r.bitop('AND', dest_key, *keys)
        data = get_bits(user_ids, dest_key)
        return get_all_postion_by_bit_value(data, 1)
        # print get_bits(user_ids, dest_key)
        # return r.bitcount(dest_key)
    except:
        traceback.print_exc()
    return None


def absent_users_consecutive_days(user_ids, keys):
    if user_ids is None or len(user_ids) == 0 or keys is None or type(keys) is not list or len(keys) == 0:
        return None
    try:
        r = get_redis()
        if r is None:
            return None
        dest_key = 'absent_users_consecutive_days'
        r.bitop('XOR', dest_key, *keys)
        data = get_bits(user_ids, dest_key)
        return get_all_postion_by_bit_value(data, 0)
        # print get_bits(user_ids, dest_key)
        # return len(user_ids) - r.bitcount(dest_key)
    except:
        traceback.print_exc()
    return None


def get_all_postion_by_bit_value(data, value):
    result = []
    for elm in data:
        if elm.get('status') is not None and elm['status'] == value:
            result.append(elm)
    return result


def get_bits(user_ids, key):
    result = []
    try:
        r = get_redis()
        if r is None:
            return None
        for element in user_ids:
            temp = {}
            temp['id'] = element
            bit_value = r.getbit(key, element)
            temp['status'] = bit_value
            result.append(temp)
    except:
        traceback.print_exc()
    return result


def display_oneday(data, day, type):
    if data is None:
        print "Have an error"
    else:
        print "%s users of %s: %s" % (type, day, len(data))
        print "detail"
        print data


if __name__ == '__main__':

    print '-------------init infor----------------------'
    # init user ids
    user_ids = init_user_ids()
    print user_ids

    # init day1
    init_data_a_day(user_ids=user_ids, day='day1')
    print get_bits(user_ids=user_ids,
                   key='day1')
    # init day2
    init_data_a_day(user_ids=user_ids, day='day2')
    print get_bits(user_ids=user_ids,
                   key='day2')

    print "------------------statistic-------------------"
    # present users
    present_users_day1 = get_present_users_a_day(user_ids=user_ids, day='day1')
    display_oneday(present_users_day1, 'day1', 'present')
    present_users_day2 = get_present_users_a_day(user_ids=user_ids, day='day1')
    display_oneday(present_users_day1, 'day2', 'present')

    print "----------------------------------------------"
    # Absent users
    absent_users_day1 = get_absent_users_a_day(user_ids=user_ids, day='day1')
    display_oneday(absent_users_day1, 'day1', 'absent')
    absent_users_day1 = get_absent_users_a_day(user_ids=user_ids, day='day1')
    display_oneday(absent_users_day1, 'day2', 'absent')

    print "----------------------------------------------"
    keys = ['day1', 'day2']
    # present_users_consecutive_days both days
    present_users = present_users_consecutive_days(user_ids=user_ids,
                                                   keys=keys)
    if present_users is None:
        print "Have an error"
    else:
        print "present users consecutive days: %s" % len(present_users)
        print "detail"
        print present_users

    print "----------------------------------------------"
    # absent_users_consecutive_days both days
    absent_users = absent_users_consecutive_days(user_ids=user_ids,
                                                 keys=keys)
    if absent_users is None:
        print "Have an error"
    else:
        print "absent users consecutive days: %s" % len(absent_users)
        print "detail"
        print absent_users
