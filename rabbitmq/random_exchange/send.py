#!/usr/bin/env python
import pika
import sys
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='rdx22',
                        exchange_type='x-random')

message = 0

# channel.basic_publish(exchange='rdx',
#                       routing_key='',
#                       body=str(message))
while True:
    channel.basic_publish(exchange='rdx22',
                          routing_key='',
                          body=str(message))
    time.sleep(10)
    message = message + 1

print(" [x] Sent %r" % message)
connection.close()
