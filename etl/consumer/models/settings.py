from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    kafka_host: str = Field('localhost', env='KAFKA_HOST')
    kafka_port: str = Field('9092', env='KAFKA_PORT')
    group_id: str = Field('group_watching_movies', env='KAFKA_GROUP_ID')
    topic: str = Field('watching_movies', env='KAFKA_TOPIC')
    batch_timeout: int = Field(10, env='BATCH_TIMEOUT') # in sec
    batch_size: int = Field(10, env='BATCH_SIZE')
    ch_host: str = Field('localhost', env='CLICKHOUSE_HOST')
    ch_port: int = Field(18123, env='CLICKHOUSE_PORT')
    ch_db: str = Field('db1', env='CLICKHOUSE_DATABASE')
    ch_username: str = Field('user1', env='CLICKHOUSE_USERNAME')
    ch_password: str = Field('pass1', env='CLICKHOUSE_PASSWORD')

    @property
    def kafka_server(self):
        return f"{self.kafka_host}:{self.kafka_port}"
