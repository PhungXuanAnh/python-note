#!/usr/bin/env python
import pika
import sys
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='ccc',
                         exchange_type='x-consistent-hash')
#                          durable=True)

message = 0

# channel.basic_publish(exchange='rdx',
#                       routing_key='',
#                       body=str(message))
while True:
    channel.basic_publish(exchange='ccc',
                          routing_key='2000',
                          body=str(message))
    time.sleep(1)
    message = message + 1

print(" [x] Sent %r" % message)
connection.close()
