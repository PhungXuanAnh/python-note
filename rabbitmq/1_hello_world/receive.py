#!/usr/bin/env python
import pika
server_ip = 'localhost'
queue_name ='hello'

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
        
def receiver(server_ip, queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=server_ip))
    channel = connection.channel()
    
    
    channel.queue_declare(queue=queue_name)
    
    channel.basic_consume(callback,
                          queue=queue_name,
                          no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    
if __name__ == '__main__':
    receiver(server_ip, queue_name)
