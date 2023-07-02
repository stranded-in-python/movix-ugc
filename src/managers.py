from abc import ABC, abstractmethod
from typing import Any
from functools import lru_cache

from pydantic import BaseModel

from serializers import EventSerializerABC, EventSerializer
from storages import StorageABC, KafkaStorage
from models import BasicViewEvent

from logger import logger

logger()

class QueueSerializerManager(ABC):
    def __init__(self, deserializer: EventSerializerABC, storage: StorageABC):
        self.deserializer = deserializer
        self.storage = storage

    @abstractmethod
    async def _deserialize_to_binary_dict(self, pydantic_model: BaseModel) -> dict[str, bytes]:
        return await self.deserializer.deserialize_to_binary(pydantic_model.dict())
    
    @abstractmethod
    async def save_to_storage(self, pydantic_model: BaseModel):
        data = self._deserialize_to_binary_dict(pydantic_model)
        return await self.storage.save(data)


class ViewSerializerManager(QueueSerializerManager):
    def __init__(self, serializer: EventSerializerABC, storage: StorageABC):
        self.deserializer = serializer
        self.storage = storage

    async def _deserialize_to_binary_dict(self, pydantic_model: BasicViewEvent) -> dict[str, bytes]:
        return await self.deserializer.deserialize_to_binary(pydantic_model.dict())

    async def save_to_storage(self, pydantic_model: BasicViewEvent):
        data = await self._deserialize_to_binary_dict(pydantic_model)
        print(data)
        return await self.storage.save(data)

@lru_cache
def get_view_manager() -> ViewSerializerManager:
    return ViewSerializerManager(serializer=EventSerializer(), storage=KafkaStorage())
