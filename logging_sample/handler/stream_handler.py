import logging
import sys
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='/tmp/stream_handler_test.txt',
                    filemode='a')

my_handler = logging.StreamHandler(sys.stdout)
my_handler.setLevel(logging.INFO)
my_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logging.getLogger('').addHandler(my_handler)


logging.info('aaaaaaaaaaaaaa')
