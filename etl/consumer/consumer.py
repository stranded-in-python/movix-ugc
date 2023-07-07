import time
import uuid
from contextlib import contextmanager
from typing import Any
from typing import Generator

import clickhouse_connect
import pendulum
from clickhouse_connect.driver import Client
from clickhouse_connect.driver.exceptions import ClickHouseError
from clickhouse_connect.driver.tools import insert_file
from confluent_kafka import Consumer as KafkaConsumer
from confluent_kafka import KafkaError
from confluent_kafka import KafkaException
from confluent_kafka import Message as KafkaMessage

from backoff import on_exception
from logger import logger
from models import Message
from models import Settings
from utils import json_decoder


class Executer:
    """Управление процессом ETL из Kafka в Clickhouse."""

    def __init__(self):
        self.settings = Settings()
        self.data_filename = 'data.csv'
        self.column_names = tuple(Message.__fields__.keys())

    @contextmanager
    def _get_consumer(self) -> Generator[KafkaConsumer, Any, Any]:
        consumer = KafkaConsumer({
            'bootstrap.servers': self.settings.kafka_server,
            'group.id': self.settings.group_id,
            'auto.offset.reset': 'latest',
            'partition.assignment.strategy': 'roundrobin',
            'enable.auto.commit': 'true',
            'session.timeout.ms': '45000',
            'broker.address.family': 'v4',
        })
        consumer.subscribe([self.settings.topic])
        try:
            yield consumer
        finally:
            consumer.close()

    @on_exception(
        exception=ClickHouseError,
        logger=logger,
    )
    def _set_client_db(self):
        self.client = clickhouse_connect.get_client(
            host=self.settings.ch_host,
            port=self.settings.ch_port,
            database=self.settings.ch_db,
            username=self.settings.ch_username,
            password=self.settings.ch_password,
        )

    @contextmanager
    def _get_client_db(self) -> Generator[Client, Any, Any]:
        self._set_client_db()
        try:
            yield self.client
        finally:
            self.client.close()

    def _to_deadletter_queue(self, message: bytes):
        logger.error('Exception on message to model: %s', (str(message),))

    def _to_csv_line(self, model: Message):
        # Приведём формат времени к clickhouse
        model.timestamp = model.timestamp.format('YYYY-MM-DD hh:mm:ss')
        return (
            ','.join([str(getattr(model, field, '')) for field in self.column_names])
            + '\n'
        )

    def _messages_to_csv(self, messages: list[KafkaMessage]):
        with open(self.data_filename, 'wt') as csv:
            for message in messages:
                try:
                    msg = json_decoder(message.value())                    
                    # Transform.
                    model = Message(
                        id=int(msg['id']),
                        user_id=uuid.UUID(msg['user_id']),
                        film_id=uuid.UUID(msg['film_id']),
                        frameno=int(msg['frameno']),
                        timestamp=pendulum.parse(msg['timestamp'])
                    )
                    csv.write(self._to_csv_line(model))
                except Exception as e:
                    self._to_deadletter_queue(message.value())
                    logger.error(e)

    @on_exception(
        exception=ClickHouseError,
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
        """Запуск цикла процесса ETL."""
        consumer: KafkaConsumer
        msg: KafkaMessage
        messages: list[KafkaMessage] = []
        timeout_seconds = self.settings.batch_timeout

        with self._get_consumer() as consumer:
            with self._get_client_db():
                while True:
                    # Extract.
                    msg = consumer.poll(1.0)

                    # Ограничиваем процесс по времени
                    if msg is None:
                        timeout_seconds -= 1
                        if timeout_seconds >= 0:
                            continue

                    if msg:
                        # Проверяем на ошибки
                        err = msg.error()
                        if err:
                            if err.code() != KafkaError._PARTITION_EOF:
                                raise KafkaException(msg.error())
                        else:
                            messages.append(msg)

                    messages_read = len(messages)
                    if timeout_seconds < 0 or messages_read >= self.settings.batch_size:
                        if messages:
                            self._messages_to_csv(messages)
                            # Load.
                            self._data_to_clickhouse()
                            # Очищаем
                            messages = []

                        timeout_seconds = self.settings.batch_timeout

                        if messages_read:
                            logger.warning(f"Pushed {messages_read} messages")
                        else:
                            logger.warning('No messages, to sleep')
                            time.sleep(5)


if __name__ == '__main__':
    exec = Executer()
    exec.run()
