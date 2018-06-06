'''
Created on Jun 26, 2017

@author: xuananh
'''
import datetime
import time

timestr = time.strftime("[%Y-%m-%d]-[%H:%M:%S]-")
print("111111111111111111 {}".format(timestr))

#=============================================
start = datetime.datetime.now()
print("22222222222222222 start = {}".format(start))
 
time.sleep(5)
 
now = datetime.datetime.now()
print("33333333333333333 now = {}".format(start))
 
period = (now - start).seconds
print("44444444444444444 period = {}".format(period))


import dateutil.parser
datestring= "2018-06-06T04:52:15.526Z"
yourdate = dateutil.parser.parse(datestring)
print(yourdate)
