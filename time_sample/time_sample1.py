'''
Created on Jun 26, 2017

@author: xuananh
'''
import datetime
import calendar
import time
import dateutil.parser  # pip install python-dateutil
from dateutil.tz import tzutc

print('----------------------------------------------------------- timezone')
print(time.tzname)

print('----------------------------------------------------------- convert other format to python datetime')
print('UTC timestamp now : ', time.time())
print('UTC timestamp now : ', datetime.datetime.now().timestamp())
print('UTC timestamp now : ', calendar.timegm(time.gmtime()))
print('UTC timestamp to datetime :       ', datetime.datetime.fromtimestamp(1536775161))
print('UTC timestamp to datatime - 24h : ', datetime.datetime.fromtimestamp(1536775161 - 24 * 60 * 60))

print('RFC 3339 format: ', dateutil.parser.parse('2008-09-03T20:56:35.450686Z'))
print('                 ', datetime.datetime(2008, 9, 3, 20, 56, 35, 450686, tzinfo=tzutc()))

print('ISO 8601 extended format: ', dateutil.parser.parse('2008-09-03T20:56:35.450686'))
print('                          ', datetime.datetime(2008, 9, 3, 20, 56, 35, 450686))

print('ISO 8601 basic format: ', dateutil.parser.parse('20080903T205635.450686'))
print('                       ', datetime.datetime(2008, 9, 3, 20, 56, 35, 450686))

print('ISO 8601 basic format, date only: ', dateutil.parser.parse('20080903'))
print('                                  ', datetime.datetime(2008, 9, 3, 0, 0))

print('----------------------------------------------------------- format datetime')
my_time = dateutil.parser.parse("2018-06-06T08:01:53.420Z")
print('my_time:          ', my_time)
print("my_time formated: ", my_time.strftime("[%Y-%m-%d]-[%H:%M:%S]"))


print('----------------------------------------------------------- period')
start = datetime.datetime.now()
print("start:          ", start)

print('....spleeping 3s...')
time.sleep(3)

now = datetime.datetime.now()
print("now:          ", now)

period = (now - start).seconds
print("period: ", period)

print('----------------------------------------------------------- datetime ago')
now = datetime.datetime.now()
datetime_7_day_ago = now - datetime.timedelta(days=7)
print("now :           ", now)
print("date_7_day_ago: ", datetime_7_day_ago)

today = datetime.date.today()
date_7_day_ago = today - datetime.timedelta(days=7)
print('today           ', today)
print('date_7_day_ago: ', date_7_day_ago)
