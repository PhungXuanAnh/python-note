'''
Created on Apr 4, 2017

@author: xuananh
'''

from sqlalchemy_example import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# testing
engine = create_engine('sqlite:///teste.db', echo=True)
Session = sessionmaker(bind=engine)
s = Session()

for user in s.query(User):
    print type(user), user.name, user.password