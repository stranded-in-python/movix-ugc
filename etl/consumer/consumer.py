from confluent_kafka import Consumer, KafkaException, KafkaError
import time
import logging
from models import Settings, Message
import clickhouse_connect
import json


def json_decoder(value):
    return json.loads(value.decode('utf-8'))


def to_deadleter_queue(msg):
    logging.error('Exception on decode message to model: %s', (str(msg.value()),))


def to_csv_line(m: Message):
    return f"{m.id},{m.user_id},{m.film_id},{m.frameno},{m.timestamp}"

settings = Settings()

consumer = Consumer({
    'bootstrap.servers': settings.kafka_server,
    'group.id': settings.group_id,
    'auto.offset.reset': 'latest',
    #'auto.offset.reset': 'earliest',
    'partition.assignment.strategy': 'roundrobin',
    'enable.auto.commit': 'true',
    'session.timeout.ms': '45000',
    'broker.address.family': 'v4',
})

consumer.subscribe([settings.topic])

client = clickhouse_connect.get_client(host=settings.ch_host, port=settings.ch_port, username=settings.ch_username, password=settings.ch_password)

BATCH_TIMEOUT = settings.batch_timeout
BATCH_SIZE = settings.batch_size

messages = []
timeout_seconds = BATCH_TIMEOUT

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            timeout_seconds -= 1
            if timeout_seconds >= 0:
                continue

        if msg:
            err = msg.error()
            if err:
                if err.code() != KafkaError._PARTITION_EOF:
                    raise KafkaException(msg.error())
            else:
                messages.append(msg)

        if timeout_seconds < 0 or len(messages) >= BATCH_SIZE:
            if messages:
                with open('data.csv', 'wt', encoding='utf-8') as file:
                    for message in messages:
                        try:
                            m = json_decoder(message)
                            model = Message(
                                id=m['id'],
                                user_id=m['user_id'],
                                film_id=m['film_id'],
                                frameno=m['frameno']
                            )
                            file.write(to_csv_line(model))
                        except:
                            to_deadleter_queue(message)
                messages =[]

            timeout_seconds = BATCH_TIMEOUT


            print(f"Readed 10 messages")
            time.sleep(5)


finally:
    # Close the consumer
    consumer.close()
