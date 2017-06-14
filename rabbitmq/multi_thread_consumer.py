#!/usr/bin/env python
import pika
import threading
import time

def callback(ch, method, properties, body):
	print(" [x] Received %r" % body)
#     ch.close()  # this line to close connection right after receive message

def start_consummer(queue):
	connection = pika.BlockingConnection(pika.ConnectionParameters(
	        host='10.64.0.167'))
	channel = connection.channel()
	
	channel.queue_declare(queue=queue)
	
	# channel.basic_consume(consumer_callback, queue, no_ack, exclusive, consumer_tag, arguments)
	
	channel.basic_consume(callback,
	                      queue=queue,
	                      no_ack=True)
	
	print(' [*] Waiting for messages. To exit press CTRL+C\n')
	channel.start_consuming()
	
	
f1 = threading.Thread(target=start_consummer, args=["11111"]) # pass args as a list
f1.start()
print('aaaaaaaaaaaaaaaaaaaaaaaaaaa 1')
f2 = threading.Thread(target=start_consummer, args=["22222"])
f2.start()
print('aaaaaaaaaaaaaaaaaaaaaaaaaaa 2')
f3 = threading.Thread(target=start_consummer, args=["33333"])
f3.start()
print('aaaaaaaaaaaaaaaaaaaaaaaaaaa 3')
while True:
	time.sleep(3)
	pass


