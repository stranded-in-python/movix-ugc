from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from deserializers.deserializers import Deserializer
from storages.storages import StorageABC


class EventSerializerManager(ABC):
    def __init__(self, deserializer: Deserializer, storage: StorageABC):
        self.deserializer = deserializer
        self.storage = storage

    @abstractmethod
    async def _deserialize(self, pydantic_model: BaseModel) -> dict[Any, str]:
        return await self.deserializer.deserialize(pydantic_model.dict())

    @abstractmethod
    async def save_to_storage(self, pydantic_model: BaseModel) -> bool:
        data = self._deserialize(pydantic_model)
        return await self.storage.save(data)
