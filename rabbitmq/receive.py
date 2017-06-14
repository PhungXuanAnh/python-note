#!/usr/bin/env python
import pika

# import pdb
# pdb.set_trace()

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='10.64.0.167'))
channel = connection.channel()


channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print body
#     print(" [x] Received %r" % body)
#     ch.close()  # this line to close connection right after receive message

# channel.basic_consume(consumer_callback, queue, no_ack, exclusive, consumer_tag, arguments)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
