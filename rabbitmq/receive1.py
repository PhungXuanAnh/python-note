#!/usr/bin/env python
import pika


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    ch.stop_consuming(consumer_tag = 'hello')
        
def start_consumer(queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='10.64.0.167'))
    channel = connection.channel()
    
    
    channel.queue_declare(queue='hello')
    
    # channel.basic_consume(consumer_callback, queue, no_ack, exclusive, consumer_tag, arguments)
    
    channel.basic_consume(callback,
                          queue='hello',
                          no_ack=True,
                          consumer_tag = 'hello')
    
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    start_consumer(queue = 'hello')
