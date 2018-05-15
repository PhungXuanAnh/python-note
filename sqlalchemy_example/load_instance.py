'''
Created on Apr 4, 2017

@author: xuananh
'''

from models import User, Session

s = Session()

for user in s.query(User):
    print('===============================================')
    print(type(user))
    print(user.name)
    print(user.address)
    print(user.password)
    print(user.profile)