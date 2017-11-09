#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', 
                      durable=True # make queue persistent
                      )

message = ' '.join(sys.argv[1:]) or "Hello World!"

# message = 1
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=str(message),
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
print(" [x] Sent %r" % message)
connection.close()
