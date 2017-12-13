import pika

host_ip = '10.64.0.168'

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host_ip))
channel = connection.channel()

# channel.queue_declare(queue, passive, durable, exclusive, auto_delete, arguments)
channel.queue_delete(queue='backend555')