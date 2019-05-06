#!/usr/bin/env python
import pika
import json


def send(host_ip, queue, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host_ip))
    channel = connection.channel()

    channel.queue_declare(queue=queue)

    channel.basic_publish(exchange='',
                          routing_key=queue,
                          body=message)
    print(" [x] Sent '{}'".format(message))
    connection.close()


if __name__ == '__main__':
    host_ip = 'localhost'
    queue = '111'
    message = {
        "SessionId": "123",
        # 					"Command": "lock_run_test",
        # 					"Command": "unlock_run_test",
        "Command": "check_run_test",
        "Params": {},
        "From": "test"}

    send(host_ip, queue, json.dumps(message))
