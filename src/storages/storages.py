import logging
from abc import ABC, abstractmethod
from typing import Any

import asyncio
import msgpack
from aiokafka import AIOKafkaProducer

from core.config import settings
from core.logger import logger

logger()


class StorageABC(ABC):
    @abstractmethod
    async def save(obj: dict[Any]):
        ...

class KafkaStorage(StorageABC):

    @classmethod
    async def create(cls):
        self = KafkaStorage()
        self.producer = AIOKafkaProducer(
            bootstrap_servers=f"{settings.kafka_host}:{settings.kafka_port}",
            value_serializer=msgpack.dumps)
        await self.producer.start()
        return self
    
    async def save(self, topic: str, obj: dict[str, Any]) -> bool:
        key = obj.pop("key_binary")
        try:
            await self.producer.send(topic=topic, key=key, value=obj)
            return True
        except Exception as e:
            logging.exception("Failed to send to broker:%s" % e)
            return False

def get_kafka_instance() -> KafkaStorage:
    instance = asyncio.run(KafkaStorage.create())
    return instance
