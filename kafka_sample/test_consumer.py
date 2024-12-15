"""
Start kafka server with docker:
    docker run -d --name test-kafka \
            -p 2181:2181 \
            -p 9092:9092 \
            --env ADVERTISED_HOST=0.0.0.0\
            --env ADVERTISED_PORT=9092 \
            spotify/kafka
"""

import json

from common import kafka_servers, topic
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    topic,
    auto_offset_reset="earliest",
    value_deserializer=lambda m: json.loads(m.decode("ascii")),
    enable_auto_commit=False,
    bootstrap_servers=kafka_servers,
)

for message in consumer:
    print("topic:     {}".format(message.topic))
    print("partition: {}".format(message.partition))
    print("offset:    {}".format(message.offset))
    print("key:       {}".format(message.key))
    print("value:     {}".format(message.value))
    print("---------------------------------")
