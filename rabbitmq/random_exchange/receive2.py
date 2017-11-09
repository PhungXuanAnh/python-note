#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='rdx22',
                        exchange_type='x-random')

# result = channel.queue_declare(exclusive=True)
# queue_name = result.method.queue

queue_name = 'random222'
channel.queue_declare(queue=queue_name,
                      auto_delete=True)

channel.queue_bind(exchange='rdx22',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)
    time.sleep(10)
    print(" [x] Received %r" % body)    
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(callback,
                      queue=queue_name)

channel.start_consuming()
