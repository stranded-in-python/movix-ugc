import os

from pydantic import BaseSettings, Field, SecretStr


class ModelConfig:
    allow_population_by_field_name = True


class Settings(BaseSettings):
    project_name: str = "movix-events"

    view_event: str = "views"

    kafka_host: str = Field("localhost", env="KAFKA_HOST")
    kafka_port: str = Field("9092", env="KAFKA_PORT")
    group_id: str = Field("group_watching_movies", env="KAFKA_GROUP_ID")
    topic: str = Field("watching_movies", env="KAFKA_TOPIC")
    batch_timeout: int = Field(10, env="BATCH_TIMEOUT")  # in sec
    batch_size: int = Field(10, env="BATCH_SIZE")
    ch_host: str = Field("localhost", env="CLICKHOUSE_HOST")
    ch_port: int = Field(18123, env="CLICKHOUSE_PORT")
    ch_db: str = Field("db1", env="CLICKHOUSE_DATABASE")
    ch_table: str = Field("watching_movies", env="CLICKHOUSE_TABLE")
    ch_username: str = Field("user1", env="CLICKHOUSE_USERNAME")
    ch_password: str = Field("pass1", env="CLICKHOUSE_PASSWORD")

    access_token_secret: SecretStr = SecretStr('ACCESS')
    access_token_audience: str = 'movix:auth'

    auth_user_rights_endpoint: str = 'http://auth:8000/api/v1/users/user_id/roles'

    mongo_host: str = Field("localhost", env="MONGO_HOST")
    mongo_port: int = Field(27017, env="MONGO_PORT")
    mongo_db_name: str = Field("ugc", env="MONGO_DB_NAME")

    @property
    def kafka_server(self):
        return f"{self.kafka_host}:{self.kafka_port}"

    base_dir = os.path.dirname(os.path.dirname(__file__))


settings = Settings()
