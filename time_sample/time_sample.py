'''
Created on Jun 26, 2017

@author: xuananh
'''
import datetime
import time

start = datetime.datetime.now()
print("start = {}".format(start))

time.sleep(5)

now = datetime.datetime.now()
print("now = {}".format(start))

period = (now - start).seconds
print("period = {}".format(period))
