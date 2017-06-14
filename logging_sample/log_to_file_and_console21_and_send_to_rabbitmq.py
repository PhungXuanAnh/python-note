import sys
import threading
import Queue
import logging

class LoggerRedirected(object):
    def __init__(self, logs_file, thread_lock):
        self.stream = sys.stdout
#         self.file = open(logs_file, "a")
        self.file = logs_file
        self.thread_lock = thread_lock

    def write(self, message):
        self.thread_lock.acquire()
        self.stream.write(message)
#         self.file.write(message)
        with open(self.file, 'a') as logs_file:
            logs_file.write(message)
        self.thread_lock.release()

    def flush(self):
        #this flush method is needed for python 3 compatibility.
        #this handles the flush command by doing nothing.
        #you might want to specify some extra behavior here.
        pass  

def __push_logs_to_rabbitmq():
    # empty logs file
    with open(logs_file, 'w') as logs_file:
        pass
        
    def push_message_periodically():
        import pika, time
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=messq_ip))
        channel = connection.channel()
        
        channel.queue_declare(queue=logs_message_queue)
        
        while workQueue.empty():
            time.sleep(2)
            
            try:
                msg = None
                thread_lock.acquire()
                with open(logs_file, 'r') as logs_file:
                    msg = logs_file.read()
                    
                # empty logs file
                with open(logs_file, 'w') as logs_file:
                    pass
                thread_lock.release()   
                    
                if msg != '' and msg != None:
                    channel.basic_publish(exchange='',
                                          routing_key=logs_message_queue,
                                          body=msg)
                    
            except Exception as e:
                logging.error(e.message)
            
        
        connection.close()
            
    t1 = threading.Thread(target=push_message_periodically, args=[])
    t1.start()

logs_file = 'logsfile21.out'
thread_lock = threading.Lock()
sys.stdout = LoggerRedirected(logs_file, thread_lock)
workQueue = Queue.Queue(10)

messq_ip = 'localhost'
logs_message_queue = 'web_queue'

__push_logs_to_rabbitmq()
print "Hello"

