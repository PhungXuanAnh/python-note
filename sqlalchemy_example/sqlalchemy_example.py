'''
Created on Apr 4, 2017

@author: xuananh
sudo -H pip install sqlalchemy
'''
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from random import choice
from string import letters

engine = create_engine('sqlite:///teste.db', echo=True)
Base = declarative_base(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(40))
    address = Column(UnicodeText, nullable=True)
    password = Column(String(20))

    def __init__(self, name, address=None, password=None):
        self.name = name
        self.address = address
        if password is None:
            password = ''.join(choice(letters) for n in xrange(10))
        self.password = password

Base.metadata.create_all()

# Session = sessionmaker(bind=engine)
# s = Session()
# 
# 
# # create instances of my user object
# u = User('nosklo')
# u.address = '66 Some Street #500'
# 
# u2 = User('lakshmipathi')
# u2.password = 'ihtapimhskal'
# 
# # testing
# s.add_all([u, u2])
# s.commit()
# 
# for user in s.query(User):
#     print type(user), user.name, user.password