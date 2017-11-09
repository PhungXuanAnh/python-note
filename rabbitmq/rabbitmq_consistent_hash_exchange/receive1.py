#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='ccc',
                         exchange_type='x-consistent-hash')
#                          durable=True)

# result = channel.queue_declare(exclusive=True)
# queue_name = result.method.queue

queue_name ='qq5'
channel.queue_declare(queue=queue_name)

channel.queue_bind(exchange='ccc',
                   queue=queue_name,
                   routing_key="1000")

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)
    time.sleep(1)
    print(" [x] Received %r" % body)    
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_consume(callback,
                      queue=queue_name)

channel.start_consuming()
