'''
Created on Apr 4, 2017

@author: xuananh
'''
from sqlalchemy_example import User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# create instances of my user object
u = User('nosklo')
u.address = '66 Some Street #500'

u2 = User('lakshmipathi')
u2.password = 'ihtapimhskal'

# testing
engine = create_engine('sqlite:///teste.db', echo=True)
Session = sessionmaker(bind=engine)
s = Session()
s.add_all([u, u2])
s.commit()