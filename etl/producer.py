from confluent_kafka import Producer
import socket
from time import sleep
import time
import json
from faker import Faker
import uuid
import random
from consumer.models import Settings, Message
from utils import UUIDEncoder


fake = Faker()

conf = {
    'bootstrap.servers': "localhost:9092",
    'client.id': socket.gethostname(),
    #!'batch.size': 600,
    #'linger.ms': 500,
    'acks': 1,
    'retries': 3,
    #'max.in.flight.requests.per.connection': 5,

    # Если надо, чтобы каждое сообщение(или транзакция?), которой присваивается номер, записавалась один раз
    #'enable.idempotence': 'true',
    #'acks': 'all',
}

producer = Producer(conf)

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

for _ in range(40):
    m = Message(
        id=random.getrandbits(34),
        user_id=uuid.UUID(int=random.getrandbits(128)),
        film_id=uuid.UUID(int=random.getrandbits(128)),
        frameno=random.getrandbits(32),
        timestamp=fake.date_time()
    )

    # Trigger any available delivery report callbacks from previous produce() calls
    producer.poll(0)

    # Asynchronously produce a message. The delivery report callback will
    # be triggered from the call to poll() above, or flush() below, when the
    # message has been successfully delivered or failed permanently.
    producer.produce('watching_movies', json.dumps(m.dict(), cls=UUIDEncoder).encode(), callback=delivery_report)

# Wait for any outstanding messages to be delivered and delivery report
# callbacks to be triggered.
producer.flush()


# from kafka import KafkaProducer
# from time import sleep
#
#
# producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
#
# producer.send(
#     topic='test1',
#     value=b'1611039931',
#     key=b'500271+tt0120338',
# )
#
#sleep(1)


# from kafka import KafkaProducer
# from kafka.errors import KafkaError
# import json
# import logging
#
# producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
#                          linger_ms = 500)
#
# def on_send_success(record_metadata):
#     print(record_metadata.topic)
#     print(record_metadata.partition)
#     print(record_metadata.offset)
#
# def on_send_error(excp):
#     logging.error('I am an errback', exc_info=excp)
#     # handle exception
#
# # produce asynchronously
# for _ in range(100):
#
#     # produce asynchronously with callbacks
#     producer.send('test1', b'raw_bytes').add_callback(on_send_success).add_errback(on_send_error)
#
# # block until all async messages are sent
# producer.flush()
