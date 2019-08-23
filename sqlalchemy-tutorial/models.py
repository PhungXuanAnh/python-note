# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Text

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(40))
    address = Column(UnicodeText, nullable=True)

    def __init__(self, name, address=None):
        self.name = name
        self.address = address

    def __repr__(self):
        return "<User(name='{}', address='{}')>".format(self.name, self.address)
