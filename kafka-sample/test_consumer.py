import json
from kafka import KafkaConsumer

topic = 'my-topic1'
group_id = 'my-group1'
kafka_servers = ['localhost:9092']

consumer = KafkaConsumer(topic,
                         auto_offset_reset='earliest',
                         value_deserializer=lambda m: json.loads(m.decode('ascii')),
                         enable_auto_commit=False,
                         bootstrap_servers=kafka_servers,
                         group_id=group_id)

for message in consumer:
    print('topic:     {}'.format(message.topic))
    print('partition: {}'.format(message.partition))
    print('offset:    {}'.format(message.offset))
    print('key:       {}'.format(message.key))
    print('value:     {}'.format(message.value))
    print('---------------------------------')
