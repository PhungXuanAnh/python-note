import logging

# default level is WARNING
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

# change level to DEBUG
# NOTE: it must comment above code
logging.basicConfig(level=logging.DEBUG)
logging.debug('This will get logged')
