#!/usr/bin/env python
import pika
import time

identifier = 1

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)
#     time.sleep(body.count(b'.'))
    if int(body) != identifier:
#         ch.basic_reject(delivery_tag = method.delivery_tag)            
        ch.basic_nack(delivery_tag = method.delivery_tag)
        return
#     time.sleep(30)
    print(" [x] Received %r" % body)    
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue')

channel.start_consuming()
