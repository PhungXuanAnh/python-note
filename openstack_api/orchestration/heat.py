'''
Created on Oct 5, 2017

@author: xuananh
'''
from stack import Stacks

class Heat(object):
    def __init__(self, os_token, orchestration_admin_url):
        self.stacks = Stacks(os_token, orchestration_admin_url)
        