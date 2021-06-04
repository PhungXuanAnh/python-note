'''
Created on Jun 26, 2017

@author: xuananh
'''
import datetime
import calendar
import time
import dateutil.parser
from dateutil.tz import tzutc

def get_timezone():
    print(time.tzname)

def format_datetime_for_some_standar(): 
    print('UTC timestamp now 1: ', time.time())
    print('UTC timestamp now 2: ', datetime.datetime.now().timestamp())
    print('UTC timestamp now 3: ', datetime.datetime.utcnow())
    print('UTC timestamp now 4: ', calendar.timegm(time.gmtime()))
    print('UTC timestamp to datetime :       ', datetime.datetime.fromtimestamp(1575963196))
    print('UTC timestamp to datatime - 24h : ', datetime.datetime.fromtimestamp(1575963196 - 24 * 60 * 60))
    print('UTC timestamp to hour :       ', datetime.datetime.fromtimestamp(1575963196).hour)

    print('RFC 3339 format: ', dateutil.parser.parse('2008-09-03T20:56:35.450686Z'))
    print('                 ', datetime.datetime(2008, 9, 3, 20, 56, 35, 450686, tzinfo=tzutc()))

    print('ISO 8601 extended format: ', dateutil.parser.parse('2008-09-03T20:56:35.450686'))
    print('                          ', datetime.datetime(2008, 9, 3, 20, 56, 35, 450686))

    print('ISO 8601 basic format: ', dateutil.parser.parse('20080903T205635.450686'))
    print('                       ', datetime.datetime(2008, 9, 3, 20, 56, 35, 450686))

    print('ISO 8601 basic format, date only: ', dateutil.parser.parse('20080903'))
    print('                                  ', datetime.datetime(2008, 9, 3, 0, 0))

def datetime_format():
    print('-------------------------- datetime format ------------------------------')
    my_time = dateutil.parser.parse("2018-06-06T08:01:53.420Z")
    print('my_time:          ', my_time)
    print("my_time formated: ", my_time.strftime("[%Y-%m-%d]-[%H:%M:%S]"))
    my_time = datetime.datetime.now()
    print('my_time:          ', my_time)
    print("my_time formated: ", my_time.strftime("[%Y-%m-%d]-[%H:%M:%S]"))


def get_time_period():
    start = datetime.datetime.now()
    print("start:          ", start)

    print('....spleeping 3s...')
    time.sleep(3)

    now = datetime.datetime.now()
    print("now:          ", now)

    period = (now - start).seconds
    print("period: ", period)


    t1 = datetime.datetime(2008, 9, 3, 20, 56, 35, 450686)
    t2 = datetime.datetime(2008, 9, 5, 20, 56, 45, 450686)
    print("NOTE: It should use total_seconds when t2 - t1 > 1 day, see the difference below:")
    print("(t2-t1).seconds(): {}".format((t2-t1).seconds))
    print("(t2-t1).total_seconds(): {}".format((t2-t1).total_seconds()))

def datetime_in_pass():
    now = datetime.datetime.now()
    datetime_7_day_ago = now - datetime.timedelta(days=7)
    print("now :           ", now)
    print("date_7_day_ago: ", datetime_7_day_ago)

    today = datetime.date.today()
    date_7_day_ago = today - datetime.timedelta(days=7)
    print('today           ', today)
    print('date_7_day_ago: ', date_7_day_ago)

def date_time_in_furture():
    now = datetime.datetime.now()
    datetime_7_day_ago = now + datetime.timedelta(days=7)
    print("now :                 ", now)
    print("date_7_day_in_future: ", datetime_7_day_ago)
    print("timestamp: ", datetime_7_day_ago.timestamp())

    today = datetime.date.today()
    date_7_day_ago = today + datetime.timedelta(days=7)
    print('today                 ', today)
    print('date_7_day_in_future: ', date_7_day_ago)
    print("timestamp: ", datetime_7_day_ago.timestamp())


def time_around_a_moment():
    d = datetime.datetime.utcnow()
    for i in range(-2, 3):
        d1 = d + datetime.timedelta(minutes=i)
        print(d1.strftime("%Y-%m-%dT%H:%M"))
        # print(d1.strftime("%Y-%m-%d"))

def extract_year_month_day_hour_minute_second():
    print('-----------------------extract_year_month_day_hour_minute_second-----------------------')
    print('year: ', datetime.datetime.now().year)
    print('month: ', datetime.datetime.now().month)
    print('day: ', datetime.datetime.now().day)
    print('hour: ', datetime.datetime.now().hour)
    print('minute: ', datetime.datetime.now().minute)
    print('second: ', datetime.datetime.now().second)

if __name__ == '__main__':
    print(datetime.date(1991, 1, 1))
    get_timezone()
    
    format_datetime_for_some_standar()
    datetime_format()
    
    get_time_period()
    
    datetime_in_pass()
    date_time_in_furture()
    time_around_a_moment()

    extract_year_month_day_hour_minute_second()
