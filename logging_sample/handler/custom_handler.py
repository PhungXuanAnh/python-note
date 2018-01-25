import logging
import pika
import sys

class RabbitmqHandler(logging.Handler):
    def __init__(self, host_ip, queue):
        self.host_ip = host_ip
        self.queue = queue
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.host_ip))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        
        logging.Handler.__init__(self)
        
    def emit(self, record):
        msg = self.format(record)
        self.channel.basic_publish(exchange='',
                                    routing_key=self.queue,
                                    body=msg)
        
logging.basicConfig(level=logging.INFO,
                    format='%(name)-12s %(asctime)s  %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    stream=sys.stdout)
logger1 = logging.getLogger('logger1')
logger2 = logging.getLogger('logger2')

#======================================== add handler
rabbit_handler = RabbitmqHandler(host_ip='localhost', queue='hello')
rabbit_handler.setLevel(logging.INFO)
rabbit_handler.setFormatter(logging.Formatter(
                         '%(name)-20s: %(levelname)-20s %(message)s'))
logging.getLogger("logger1").addHandler(rabbit_handler)
#========================================

logger1.info('11111111111111111111')
logger2.info('22222222222222222222')
logging.info('00000000000000000000')


