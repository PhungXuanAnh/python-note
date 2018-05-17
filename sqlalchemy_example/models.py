'''
Created on Apr 4, 2017

@author: xuananh
sudo -H pip install sqlalchemy
'''
from sqlalchemy import Column, Integer, Unicode, UnicodeText, String, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# NOTE: tao database voi charset va collate la uft8 voi cau lenh sau:
# CREATE DATABASE test11 CHARACTER SET utf8 COLLATE utf8_unicode_ci;'


MYSQL_USER     = 'root'
MYSQL_PASSWORD = '7VuNSOTKEFE6w7'
MYSQL_HOST     = '127.0.0.1'
MYSQL_PORT     = 3309
MYSQL_DB       = 'test11'
MYSQL_CHARSET  = 'utf8mb4' # it it import to automatically convert(encode/decode) data to unicode using utf8
MYSQL_URI      = 'mysql://{user}:{password}@{host}:{port}/{database}?charset={charset}'
mysql_uri = MYSQL_URI.format(user     = MYSQL_USER,
                        password = MYSQL_PASSWORD,
                        host     = MYSQL_HOST,
                        port     = MYSQL_PORT,
                        database = MYSQL_DB,
                        charset  = MYSQL_CHARSET
                        )
print(mysql_uri)
engine = create_engine(mysql_uri, encoding='utf-8', echo=True)

Session = sessionmaker(bind=engine)
Base = declarative_base(bind=engine)

def randompassword():
    import string
    import random
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randint(8, 12)
    return ''.join(random.choice(chars) for x in range(size))

def gen_password():
    from random import choice

    # # python 2
    # from string import letters
    # return ''.join(choice(letters) for n in xrange(10))

    # python 3
    from string import ascii_letters
    return ''.join(choice(ascii_letters) for n in range(10))
class User(Base):
    __tablename__ = 'users'
    id       = Column(Integer, primary_key=True)
    name     = Column(Unicode(40))
    address  = Column(UnicodeText, nullable=True)
    password = Column(String(20))
    profile  = Column(Text)

    def __init__(self, name, address=None, password=None):
        self.name = name
        self.address = address
        if password is None:
            password = gen_password()
        self.password = password

Base.metadata.create_all()
