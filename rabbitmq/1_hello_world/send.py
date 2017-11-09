#!/usr/bin/env python
import pika
server_ip = 'localhost'
queue_name ='hello'
message = 'Hello World!'

def sender(server_ip, queue_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=server_ip))
    channel = connection.channel()
    
    
    channel.queue_declare(queue=queue_name)
    
    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=message)
    print(" [x] Sent 'Hello World!'")
    connection.close()

if __name__ == '__main__':
    sender(server_ip, queue_name, message)
