import os

from pydantic import BaseSettings, Field


class ModelConfig:
    allow_population_by_field_name = True


class Settings(BaseSettings):
    project_name: str = "movix-events"

    view_event: str = "views"

    kafka_host: str = Field("localhost", env="KAFKA_HOST")
    kafka_port: str = Field("9092", env="KAFKA_PORT")
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    group_id: str = Field("group_watching_movies", env="KAFKA_GROUP_ID")
    topic: str = Field("watching_movies", env="KAFKA_TOPIC")
    batch_timeout: int = Field(10, env="BATCH_TIMEOUT")  # in sec
    batch_size: int = Field(10, env="BATCH_SIZE")
    ch_host: str = Field("localhost", env="CLICKHOUSE_HOST")
    ch_port: int = Field(18123, env="CLICKHOUSE_PORT")
    ch_db: str = Field("movix_db", env="CLICKHOUSE_DATABASE")
    ch_table: str = Field("watching_movies", env="CLICKHOUSE_TABLE")
    ch_username: str = Field("movix", env="CLICKHOUSE_USERNAME")
    ch_password: str = Field("qwe123", env="CLICKHOUSE_PASSWORD")

    @property
    def kafka_server(self):
        return f"{self.kafka_host}:{self.kafka_port}"

    base_dir = os.path.dirname(os.path.dirname(__file__))


settings = Settings()
