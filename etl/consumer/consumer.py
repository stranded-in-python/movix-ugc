from confluent_kafka import Consumer, KafkaException, KafkaError
import time
import logging
from .models import Settings
import clickhouse_connect


settings = Settings()

c = Consumer({
    'bootstrap.servers': settings.kafka_server,
    'group.id': settings.group_id,
    'auto.offset.reset': 'latest',
    'partition.assignment.strategy': 'roundrobin',
    'enable.auto.commit': 'true',
    'session.timeout.ms': '45000',
    'broker.address.family': 'v4',
})

c.subscribe([settings.topic])

client = clickhouse_connect.get_client(host=settings.ch_host, port=settings.ch_port, username=settings.ch_username, password=settings.ch_password)

BATCH_TIMEOUT = settings.batch_timeout
BATCH_SIZE = settings.batch_size

messages = []
timeout_seconds = BATCH_TIMEOUT

try:
    while True:
        msg = c.poll(1.0)  # Poll for messages with a timeout of 1 second

        if msg is None:
            # If no message is available, decrease the timeout
            timeout_seconds -= 1
            if timeout_seconds >= 0:
                continue

        if msg:
            err = msg.error()
            if err:
                if err.code() != KafkaError._PARTITION_EOF:
                    # Handle other errors
                    raise KafkaException(msg.error())
            else:
                messages.append(msg)

        if timeout_seconds < 0 or len(messages) >= BATCH_SIZE:
            for message in messages:
                print(f"Received message: {message.value().decode('utf-8')}")

            timeout_seconds = BATCH_TIMEOUT
            messages =[]

            print(f"Readed 10 messages")
            time.sleep(5)


finally:
    # Close the consumer
    c.close()

