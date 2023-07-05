import logging
from abc import ABC, abstractmethod
from typing import Any

import msgpack
from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError

from settings.config import settings
from settings.logger import logger

logger()


class StorageABC(ABC):
    @abstractmethod
    async def save(obj: dict[Any]):
        ...


class KafkaStorage(StorageABC):
    def __init__(self):
        self.kafka = KafkaProducer(
            bootstrap_servers=[f"{settings.kafka_host}:{settings.kafka_port}"],
            value_serializer=msgpack.dumps,
        )

    async def save(self, topic: str, obj: dict[Any, str]) -> bool:
        key = obj.pop("key_binary")
        try:
            self.kafka.send(topic=topic, key=key, value=obj)
            return True
        except KafkaTimeoutError as e:
            logging.exception("Failed to send to broker with %s" % e)
            return False
