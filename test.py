import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq_external'))
channel = connection.channel()

# channel.queue_declare(queue='mail_channel')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(callback,
                      queue='mail_channel',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
