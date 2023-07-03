import os

from pydantic import BaseSettings

# from logging import config as logging_config


# from core.logger import LOG_LEVEL, get_logging_config


class ModelConfig:
    allow_population_by_field_name = True


class Settings(BaseSettings):
    project_name: str = "movix-events"

    view_event: str = "views"

    kafka_host: str = "localhost"
    kafka_port: int = 9092

    base_dir = os.path.dirname(os.path.dirname(__file__))

    # # log_level: str = LOG_LEVEL


settings = Settings()


# Применяем настройки логирования
# logging_config.dictConfig(get_logging_config(level=settings.log_level))
