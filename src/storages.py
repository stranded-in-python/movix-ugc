import logging
from abc import ABC, abstractmethod
from typing import Any

from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError

from config import settings
from logger import logger

logger()

class StorageABC(ABC):
    
    @abstractmethod
    async def save(obj: dict[Any]):
        ...


class KafkaStorage(StorageABC):
    def __init__(self):
        self.kafka = KafkaProducer(bootstrap_servers=[f"{settings.kafka_host}:{settings.kafka_port}"])

    async def save(self, obj: dict[str, bytes]) -> bool:
        try:
            self.kafka.send(**obj)
            return True
        except KafkaTimeoutError as e:
            logging.exception("Failed to send to broker with %s" % e)
            return False


