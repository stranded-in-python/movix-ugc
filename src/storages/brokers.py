import asyncio
import logging
from typing import Any

import msgpack
from aiokafka import AIOKafkaProducer

from core.config import settings
from core.logger import logger

from .abc import BrokerABC

logger()

# переименовать бы файл в brokers


class KafkaBroker(BrokerABC):
    @classmethod
    async def create(cls):
        self = KafkaBroker()
        self.producer = AIOKafkaProducer(
            bootstrap_servers=f"{settings.kafka_host}:{settings.kafka_port}",
            value_serializer=msgpack.dumps,
        )
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


def get_kafka_instance() -> KafkaBroker:
    instance = asyncio.run(KafkaBroker.create())
    return instance
