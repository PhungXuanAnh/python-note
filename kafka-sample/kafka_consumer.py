import json
from kafka import KafkaConsumer

topic = 'my-topic'
topic = 'facebook-items'
group_id = 'my-group'
kafka_servers = ['localhost:9092']

# # -----------------------------------------------------
# #  to consum latest messages and auto-commit offsets
# consumer = KafkaConsumer(topic,
#                          group_id=group_id,
#                          bootstrap_servers=kafka_servers)

# # -----------------------------------------------------
# # consume earliest available messages, don't commit offsets
# consumer = KafkaConsumer(topic,
#                          auto_offset_reset='earliest',
#                          enable_auto_commit=False,
#                          bootstrap_servers=kafka_servers)

# -----------------------------------------------------
# consume json messages
consumer = KafkaConsumer(topic,
                         value_deserializer=lambda m: json.loads(m.decode('ascii')),
                         bootstrap_servers=kafka_servers)

# -----------------------------------------------------
# consume msgpack
# KafkaConsumer(value_deserializer=msgpack.unpackb)

# -----------------------------------------------------
# stop iteration if no message after 1 sec
# KafkaConsumer(consumer_timeout_ms=1000)

# -----------------------------------------------------
# subscribe to a regex topic pattern
# consumer = KafkaConsumer()
# consumer.subscribe(pattern='^awesome.*')

# -----------------------------------------------------
# use multiple consumers in parallel kafka brokers
# typically you would run each on a different server / process / cpu
# consumer1 = KafkaConsumer('my-topic',
#                           group_id='my-group',
#                           bootstrap_servers='my.server.com')
# consumer2 = KafkaConsumer('my-topic',
#                           group_id='my-group',
#                           bootstrap_servers='my.server.com')


# -----------------------------------------------------
# print result
for message in consumer:
    # message value and key are raw bytes -- decode if necessary!
    # ex: for unicode: message.value.decode('utf-8')
    print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                         message.offset, message.key,
                                         message.value))
