import pika
import json

QUEUE = 'result'
# HOST = 'localhost'
HOST = '188.166.238.142'
PORT = 5673
connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST, port=PORT))
channel = connection.channel()


channel.queue_declare(queue=QUEUE)


def callback(ch, method, properties, body):
    print(json.dumps(json.loads(body), indent=4, sort_keys=True))
    print('--------------------------------------------------')
#     ch.close()  # this line to close connection right after receive message

# channel.basic_consume(consumer_callback, queue, no_ack, exclusive, consumer_tag, arguments)

channel.basic_consume(queue=QUEUE, on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
