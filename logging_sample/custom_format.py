###################### Cach 1
import logging
 
extra = {'custom_format':'aaaaaaaa'}
 
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
 
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(custom_format)s : %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
 
logger = logging.LoggerAdapter(logger, extra)
logger.info('The sky is so blue')

###################### Cach 2

class AppFilter(logging.Filter):
    def filter(self, record):
        record.custom_format = 'bbbbbbbbbbbbbbbbbb'
        return True
 
logger1 = logging.getLogger(__name__)
logger1.setLevel(logging.INFO)
 
logger1.addFilter(AppFilter())
 
handler1 = logging.StreamHandler()
formatter1 = logging.Formatter('%(asctime)s %(custom_format)s : %(message)s')
handler1.setFormatter(formatter1)
logger1.addHandler(handler1)
 
logger1.info('The sky is so blue')


