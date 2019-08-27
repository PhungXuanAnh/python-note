import json
import traceback
from kafka import KafkaProducer
from kafka.errors import KafkaError

topic = 'my-topic'
kafka_servers = ['localhost:9092']
# kafka_servers = ['167.71.198.165:9092']


def on_send_success(record_metadata):
    print('topic:     {}'.format(record_metadata.topic))
    print('partition: {}'.format(record_metadata.partition))
    print('offset:    {}'.format(record_metadata.offset))

producer = KafkaProducer(
    bootstrap_servers=kafka_servers,
    value_serializer=lambda m: json.dumps(m).encode('ascii'))

producer.send(topic, {'key': 'value'})\
    .add_callback(on_send_success)

producer.flush()
