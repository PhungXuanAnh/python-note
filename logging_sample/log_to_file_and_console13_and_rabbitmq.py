import logging
import pika
import threading
import json

class RabbitmqHandler(logging.Handler):
    def __init__(self, host_ip, queue):
        self.host_ip = host_ip
        self.queue = queue
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.host_ip))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        
    def emit(self, record):
        msg = self.format(record)
        self.channel.basic_publish(exchange='',
                                    routing_key=self.queue,
                                    body=msg)
        
class RabbitmqHandler1(logging.Handler):
    def __init__(self, host_ip, queue):
        self.host_ip = host_ip
        self.queue = queue
        
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.host_ip))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        
    def emit(self, record):
        message = {
                "SessionId": threading.current_thread().getName(),
                "Command": "push_logs",
                "Params": {
                    "Message": self.format(record)
                    },
                "From": "web"
            }
        
        self.channel.basic_publish(exchange='',
                                    routing_key=self.queue,
                                    body=json.dumps(message))        

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='logsfile12.out',
                    filemode='w')

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')

# tell the handler to use this format
console.setFormatter(formatter)

# add the handler to the root logger
logging.getLogger('').addHandler(console)

#================== add my logging handler
host_ip = 'localhost'
queue = 'hello'
rabbit_handler = RabbitmqHandler1(host_ip, queue)
rabbit_handler.setLevel(logging.INFO)
formatter1 = logging.Formatter('%(name)-20s: %(levelname)-20s %(message)s')
# formatter1=logging.Formatter("[%(asctime)s] [%(module)s.%(funcName)s:%(lineno)d] %(levelname)s: %(message)s")
rabbit_handler.setFormatter(formatter1)
#========================================
# Now, we can log to the root logger, or any other logger. First the root...
logging.info('Jackdaws love my big sphinx of quartz.')

# Now, define a couple of other loggers which might re+present areas in your
# application:

logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')

# add handler to logger1
logger1.addHandler(rabbit_handler)

logger1.debug('Quick zephyrs blow, vexing daft Jim.')
logger1.info('How quickly daft jumping zebras vex.')
logger2.warning('Jail zesty vixen who grabbed pay from quack.')
logger2.error('The five boxing wizards jump quickly.')


