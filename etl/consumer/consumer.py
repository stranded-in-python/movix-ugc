from logger import logger
import time
import uuid

import clickhouse_connect
import pendulum
from clickhouse_connect.driver.tools import insert_file
from clickhouse_connect.driver.exceptions import ClickHouseError
from confluent_kafka import Consumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException

from models import Message
from models import Settings
from utils import json_decoder
from contextlib import contextmanager
from backoff import on_exception

class Executer:
    def __init__(self):
        self.settings = Settings()
        self.data_filename = 'data.csv'
        self.column_names = [field for field in Message.__fields__]

    @contextmanager
    def _get_consumer(self):
        consumer = Consumer({
            'bootstrap.servers': self.settings.kafka_server,
            'group.id': self.settings.group_id,
            'auto.offset.reset': 'latest',
            #'auto.offset.reset': 'earliest',
            'partition.assignment.strategy': 'roundrobin',
            'enable.auto.commit': 'true',
            'session.timeout.ms': '45000',
            #'broker.address.family': 'v4',
        })
        consumer.subscribe([self.settings.topic])
        try:
            yield consumer
        finally:
            consumer.close()

    @on_exception(
        exception=ClickHouseError,
        start_sleep_time=1,
        factor=2,
        border_sleep_time=15,
        max_retries=15,
        logger=logger,
    )
    def _set_client_db(self):
        self.client =  clickhouse_connect.get_client(
            host=self.settings.ch_host,
            port=self.settings.ch_port,
            database=self.settings.ch_db,
            username=self.settings.ch_username,
            password=self.settings.ch_password
        )


    @contextmanager
    def _get_client_db(self):
        self._set_client_db()
        try:
            yield self.client
        finally:
            self.client.close()

    def _to_deadleter_queue(self, message: bytes):
        logger.error('Exception on message to model: %s', (str(message),))

    def _to_csv_line(self, model: Message):
        # Приведём формат времени к clickhouse
        model.timestamp = model.timestamp.format('YYYY-MM-DD hh:mm:ss')
        return ','.join([str(getattr(model, field, '')) for field in Message.__fields__]) + '\n'

    @on_exception(
        exception=ClickHouseError,
        start_sleep_time=1,
        factor=2,
        border_sleep_time=15,
        max_retries=15,
        logger=logger,
    )
    def _data_to_clickhouse(self):
        insert_file(
            self.client,
            self.settings.ch_table,
            self.data_filename,
            column_names=self.column_names,
            database=self.settings.ch_db,
        )

    def run(self):
        timeout_seconds = self.settings.batch_timeout
        messages = []
        with self._get_consumer() as consumer:
            with self._get_client_db() as _:
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

                    messages_read = len(messages)
                    if timeout_seconds < 0 or messages_read >= self.settings.batch_size:
                        if messages:
                            with open(self.data_filename, 'wt') as file:
                                for message in messages:
                                    try:
                                        m = json_decoder(message.value())
                                        ts = message.timestamp()[1]
                                        model = Message(
                                            id=m['id'],
                                            user_id=uuid.UUID(m['user_id']),
                                            film_id=uuid.UUID(m['film_id']),
                                            frameno=m['frameno'],
                                            timestamp=pendulum.from_timestamp(timestamp=ts//1000)
                                        )
                                        file.write(self._to_csv_line(model))
                                    except Exception as e:
                                        self._to_deadleter_queue(message.value())
                                        logger.error(e)

                            messages =[]

                            self._data_to_clickhouse()

                        timeout_seconds = self.settings.batch_timeout
                        if messages_read:
                            logger.warning(f"Pushed {messages_read} messages")
                        else:
                            logger.warning(f"No messages, to sleep")
                            time.sleep(5)

if __name__ == '__main__':
    exec = Executer()
    exec.run()