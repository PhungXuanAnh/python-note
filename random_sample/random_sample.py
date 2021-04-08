import random
import time
import datetime

print('choose 1 random number in range 0 - 9: ', random.randint(0, 9))

foo = [1, 2, 0, 0, 3, 4, 8, 9]
print('random choice a value from a specified list: ', random.choice(foo))
print('random choice multiple values from a specified list: ', random.choices(foo))


# choose a random child list from a larger list
print(random.sample(range(0, 10), 3))
print(random.sample(range(0, 10), 3))
print(random.sample(range(0, 10), 4))
print(random.sample(range(0, 10), 5))

start_timestamp = time.mktime(time.strptime('Jun 1 2010  01:33:00', '%b %d %Y %I:%M:%S'))
end_timestamp = time.mktime(time.strptime('Jun 1 2017  12:33:00', '%b %d %Y %I:%M:%S'))
def randomize_time(start_timestamp,end_timestamp):
    print(time.strftime('%b %d %Y %I:%M:%S', time.localtime(random.randrange(start_timestamp,end_timestamp))))
    # return time.strftime('%b %d %Y %I:%M:%S', time.localtime(random.randrange(start_timestamp,end_timestamp)))
randomize_time(start_timestamp,end_timestamp)


def randomtimes(n=100):
    start = "2021-1-1 00:00:00"
    end = "2021-12-1 00:00:00"
    frmt = '%Y-%m-%d %H:%M:%S'
    stime = datetime.datetime.strptime(start, frmt)
    etime = datetime.datetime.strptime(end, frmt)

    td = etime - stime
    # return [random.random() * td + stime for _ in range(n)]
    return random.random() * td + stime
print(randomtimes())