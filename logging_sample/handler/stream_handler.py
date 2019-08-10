import logging
import sys
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s - %(message)s',
                    filename='/tmp/stream_handler_test.txt',
                    filemode='a')

my_handler = logging.StreamHandler(sys.stdout)
my_handler.setLevel(logging.INFO)
my_handler.setFormatter(logging.Formatter('%(name)s: %(asctime)s - %(levelname)s - %(message)s'))

logging.info('aaaaaaaaaaaaaa dont add handler')
logging.getLogger('').addHandler(my_handler)
logging.info('aaaaaaaaaaaaaa added handler')


logger = logging.getLogger('my-log')
logger.setLevel(logging.INFO)
logger.info('bbbbbbbbbbbbb dont add handler')

logger.addHandler(my_handler)
logger.info('bbbbbbbbbbbbb added handler')
