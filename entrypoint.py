import sys

from pydantic import BaseSettings, Field

import clickhouse_connect
from clickhouse_connect.driver.client import Client
from clickhouse_connect.driver.exceptions import ClickHouseError

from confluent_kafka import Consumer, KafkaException

class Settings(BaseSettings):
    kafka_host: str = Field('localhost1', env='KAFKA_HOST')
    kafka_port: str = Field('9092', env='KAFKA_PORT')
    group_id: str = Field('group_watching_movies', env='KAFKA_GROUP_ID')
    topic: str = Field('watching_movies', env='KAFKA_TOPIC')
    batch_timeout: int = Field(10, env='BATCH_TIMEOUT') # in sec
    batch_size: int = Field(10, env='BATCH_SIZE')
    ch_host: str = Field('localhost', env='CLICKHOUSE_HOST')
    ch_port: int = Field(18123, env='CLICKHOUSE_PORT')
    ch_db: str = Field('db1', env='CLICKHOUSE_DATABASE')
    ch_table: str = Field('watching_movies', env='CLICKHOUSE_TABLE')
    ch_username: str = Field('user1', env='CLICKHOUSE_USERNAME')
    ch_password: str = Field('pass1', env='CLICKHOUSE_PASSWORD')

    @property
    def kafka_server(self):
        return f"{self.kafka_host}:{self.kafka_port}"


settings = Settings()

def ping_kafka():
    try:
        kc = Consumer({
                'bootstrap.servers': settings.kafka_server,
                'group.id': settings.group_id,
                'auto.offset.reset': 'latest',
                #'auto.offset.reset': 'earliest',
                'partition.assignment.strategy': 'roundrobin',
                'enable.auto.commit': 'true',
                'session.timeout.ms': '45000',
                #'broker.address.family': 'v4',
            })
        topics = kc.list_topics(timeout=1)

    except KafkaException:
        sys.exit(-1)
    finally:
        kc.close()

def ping_clickhouse():
    clickhouse_client = None
    try:
        clickhouse_client =  clickhouse_connect.get_client(
                host=settings.ch_host,
                port=settings.ch_port,
                database=settings.ch_db,
                username=settings.ch_username,
                password=settings.ch_password
            )
        if not clickhouse_client.ping():
            sys.exit(-2)
    except ClickHouseError:
        sys.exit(-2)
    finally:
        if clickhouse_client is not None:
            clickhouse_client.close()

ping_kafka()
ping_clickhouse()

sys.exit(0)