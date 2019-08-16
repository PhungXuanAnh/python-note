import logging

# default level is WARNING
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

# change level to DEBUG
# NOTE: it must comment above code
# logging.disable(logging.INFO)
# logging.disable(logging.NOTSET)
print('----------------------------------------------')
logger1 = logging.getLogger('logger1')
logger1.setLevel(level=logging.DEBUG)
logger1.debug('This is a debug message')
logger1.info('This is an info message')
logger1.warning('This is a warning message')
logger1.error('This is an error message')
logger1.critical('This is a critical message')
print('----------------------------------------------')
logger1.setLevel(level=logging.ERROR)
logger1.debug('This is a debug message')
logger1.info('This is an info message')
logger1.warning('This is a warning message')
logger1.error('This is an error message')
logger1.critical('This is a critical message')

# logging.basicConfig(level=logging.DEBUG)
# logging.debug('This will get logged')
