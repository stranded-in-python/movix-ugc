import logging
import asyncio
from abc import ABC, abstractmethod
from typing import Any

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

    async def get_producer(self) -> None:
        self.producer = AIOKafkaProducer(
            bootstrap_servers=f"{settings.kafka_host}:{settings.kafka_port}",
            value_serializer=msgpack.dumps)
        try:
            await self.producer.start()
        except Exception as e:
            logging.exception("Failed to connect to broker:%s" % e)

    async def save(self, topic: str, obj: dict[str, Any]) -> bool:
        key = obj.pop("key_binary")
        try:
            await self.producer.send(topic=topic, key=key, value=obj)
            return True
        except AttributeError:
            await self.get_producer()
            await self.producer.send(topic=topic, key=key, value=obj)
            return True
        except Exception as e:
            logging.exception("Failed to send to broker:%s" % e)
            return False
