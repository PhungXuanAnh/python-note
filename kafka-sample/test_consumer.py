import json
from kafka import KafkaConsumer

topic = 'my-topic'
kafka_servers = ['localhost:9092']
# kafka_servers = ['167.71.198.165:9092']

consumer = KafkaConsumer(topic,
                         auto_offset_reset='earliest',
                         value_deserializer=lambda m: json.loads(m.decode('ascii')),
                         enable_auto_commit=False,
                         bootstrap_servers=kafka_servers)

for message in consumer:
    print('topic:     {}'.format(message.topic))
    print('partition: {}'.format(message.partition))
    print('offset:    {}'.format(message.offset))
    print('key:       {}'.format(message.key))
    print('value:     {}'.format(message.value))
    print('---------------------------------')
    # if message.value.get('timestamp'):
    #     if not message.value.get('post_like'):
    #         print('offset:    {}'.format(message.offset))
    #         print('value:     {}'.format(message.value))
    #         print('---------------------------------')
