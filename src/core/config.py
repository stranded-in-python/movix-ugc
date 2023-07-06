import os

from pydantic import BaseSettings


class ModelConfig:
    allow_population_by_field_name = True


class Settings(BaseSettings):
    project_name: str = "movix-events"

    view_event: str = "views"

    kafka_host: str = "broker"
    kafka_port: int = 9092

    base_dir = os.path.dirname(os.path.dirname(__file__))


settings = Settings()
