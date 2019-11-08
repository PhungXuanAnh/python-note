# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Text

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(40))
    age = Column(Integer, default=0)
    address = Column(UnicodeText, nullable=True)

    def __init__(self, name, age, address=None):
        self.name = name
        self.age = age
        self.address = address

    def __repr__(self):
        return "<User(name='{}',\t age='{}',\t address='{}')>".format(self.name, self.age, self.address)
