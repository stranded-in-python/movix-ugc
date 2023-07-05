from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Any

from pydantic import BaseModel

from core.deserializers import BrokerDeserializer, KafkaDeserializer
from core.models import BasicViewEvent
from core.storages import KafkaStorage, StorageABC
from settings.logger import logger

logger()


class EventSerializerManager(ABC):
    def __init__(self, deserializer: BrokerDeserializer, storage: StorageABC):
        self.deserializer = deserializer
        self.storage = storage

    @abstractmethod
    async def _deserialize(self, pydantic_model: BaseModel) -> dict[Any, str]:
        return await self.deserializer.deserialize(pydantic_model.dict())

    @abstractmethod
    async def save_to_storage(self, pydantic_model: BaseModel) -> bool:
        data = self._deserialize(pydantic_model)
        return await self.storage.save(data)


class ViewSerializerManager(EventSerializerManager):
    def __init__(self, deserializer: BrokerDeserializer, storage: StorageABC):
        self.deserializer = deserializer
        self.storage = storage

    async def _deserialize(self, pydantic_model: BasicViewEvent) -> dict[Any, str]:
        return await self.deserializer.deserialize(pydantic_model)

    async def save_to_storage(self, pydantic_model: BasicViewEvent) -> bool:
        data = await self._deserialize(pydantic_model)
        return await self.storage.save(topic="views", obj=data)


@lru_cache
def get_view_manager() -> ViewSerializerManager:
    return ViewSerializerManager(
        deserializer=KafkaDeserializer(), storage=KafkaStorage()
    )
