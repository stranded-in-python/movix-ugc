from pydantic import BaseSettings, Field


class ModelConfig:
    allow_population_by_field_name = True


class Settings(BaseSettings):
    project_name: str = "movix-events"

    kafka_host: str = Field("localhost", env="KAFKA_HOST")
    kafka_port: str = Field("9092", env="KAFKA_PORT")

    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_base_key: str = Field("movix:ugc:etl", env="REDIS_BASE_KEY")

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

    mongo_host: str = Field("localhost", env="MONGO_HOST")
    mongo_port: str = Field("27017", env="MONGO_PORT")
    mongo_user: str | None = Field(env="MONGO_USER")
    mongo_password: str | None = Field(env="MONGO_PASSWORD")
    mongo_db: str = Field("test", env="MONGO_DB")
    mongo_rs: str | None = Field(env="MONGO_REPLICASET")
    mongo_authdb: str = Field("test", env="MONGO_AUTHDB")
    mongo_certpath: str | None = Field(env="MONGO_CERTPATH")

    @property
    def kafka_server(self):
        return f"{self.kafka_host}:{self.kafka_port}"

    @property
    def redis_key_prefix(self):
        return f"{self.redis_base_key}:{self.topic}"
