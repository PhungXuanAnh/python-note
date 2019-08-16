import logging
from logging.handlers import RotatingFileHandler

my_handler = RotatingFileHandler(filename='/tmp/rotating_file_handler.log',
                                 mode='a',
                                 maxBytes=5 * 1024,
                                 backupCount=3,
                                 encoding=None,
                                 delay=0)
my_handler.setLevel(logging.INFO)
my_handler.setFormatter(logging.Formatter(
    '%(name)-5s %(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s'))
logging.getLogger('').addHandler(my_handler)

while True:
    logging.error("aaaaaaaaaaaaaaaaaaaa")

"""
check:
        tailf /tmp/rotating_file_handler.log
"""