import random
import time
import datetime


def sample_basic_random():
    print('choose 1 random number in range 0 - 9: ', random.randint(0, 9))
    foo = [1, 2, 0, 0, 3, 4, 8, 9]
    print('random choice a value from a specified list: ', random.choice(foo))
    print('random choice multiple values from a specified list: ', random.choices(foo))
    print("Choose random 3 number in range 0-10: {}", random.sample(range(0, 10), 3))


def random_a_time_in_a_range(n=100):
    start = "2021-1-1 00:00:00"
    end = "2021-12-1 00:00:00"
    frmt = '%Y-%m-%d %H:%M:%S'
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)

    td = etime - stime
    # return [random.random() * td + stime for _ in range(n)]
    print("Random time in a range: {}".format(random.random() * td + stime))

if __name__ == '__main__':
    sample_basic_random()
    random_a_time_in_a_range()