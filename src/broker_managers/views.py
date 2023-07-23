from functools import lru_cache
from typing import Any

from core.logger import logger
from deserializers.abc import Deserializer
from deserializers.deserializers import KafkaDeserializer
from models.models import BasicViewEvent, UserViewEvent
from storages.brokers import BrokerABC, get_kafka_instance

from .abc import EventSerializerManager

logger()


class ViewSerializerManager(EventSerializerManager):
    def __init__(self, deserializer: Deserializer, storage: BrokerABC):
        self.deserializer = deserializer
        self.storage = storage

    async def _deserialize(self, pydantic_model: UserViewEvent) -> dict[str, Any]:
        return await self.deserializer.deserialize(pydantic_model)

    async def save_to_storage(self, pydantic_model: UserViewEvent) -> bool:
        clean_view_event = BasicViewEvent(**pydantic_model.dict())
        data = await self._deserialize(clean_view_event)
        return await self.storage.save(topic="views", obj=data)


@lru_cache
def get_view_manager() -> ViewSerializerManager:
    return ViewSerializerManager(
        deserializer=KafkaDeserializer(), storage=get_kafka_instance()
    )
