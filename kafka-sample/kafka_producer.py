import json
import traceback
from kafka import KafkaProducer
from kafka.errors import KafkaError

# topic = 'my-topic'
# topic = 'facebook-items'
topic = '135_tommy'

# kafka_servers = ['localhost:9092']
kafka_servers = ['167.71.198.165:9092']

# # -----------------------------------------------------
# # # asynchronous by default
# producer = KafkaProducer(bootstrap_servers=kafka_servers)
# future = producer.send(topic, b'raw_bytes')

# # block for 'synchronous' sends
# try:
#     record_metadata = future.get(timeout=10)
# except KafkaError:
#     # decide what todo if produce request failed...
#     traceback.print_exc()

# # successfully result returns assigned partition and offset
# print(record_metadata.topic)
# print(record_metadata.partition)
# print(record_metadata.offset)

# # -----------------------------------------------------
# # produce keyed message to enable hashed partitioning
# producer = KafkaProducer(bootstrap_servers=kafka_servers)
# producer.send(topic, key=b'foo', value=b'bar')

# # -----------------------------------------------------
# # encode objects via msgpack
# producer = KafkaProducer(value_serializer=msgpack.dumps)
# producer.send('msgpack-topic', {'key': 'value'})

# -----------------------------------------------------
# # produce json message
producer = KafkaProducer(
    bootstrap_servers=kafka_servers,
    value_serializer=lambda m: json.dumps(m).encode('ascii'))
producer.send(topic, dict({'crawler_status': 'closed'}))

# produce asynchronously
# producer = KafkaProducer(bootstrap_servers=kafka_servers)
# for _ in range(100):
#     producer.send('my-topic', b'msg')


# def on_send_success(record_metadata):
#     print(record_metadata.topic)
#     print(record_metadata.partition)
#     print(record_metadata.offset)


# def on_send_error(excp):
#     print(excp)


# # produce asynchrously with callbacks
# producer = KafkaProducer(bootstrap_servers=kafka_servers)
# producer.send(topic, b'raw_bytes')\
#     .add_callback(on_send_success)\
#     .add_errback(on_send_error)

# # block until all async messages are sent
producer.flush()

# # configure multiple retries
# producer = KafkaProducer(retries=5)
