from functools import lru_cache
from typing import Any

from core.logger import logger
from deserializers.abc import Deserializer
from deserializers.deserializers import KafkaDeserializer
from .abc import EventSerializerManager
from models.models import BasicViewEvent
from storages.storages import KafkaStorage, StorageABC

logger()

class ViewSerializerManager(EventSerializerManager):
    def __init__(self, deserializer: Deserializer, storage: StorageABC):
        self.deserializer = deserializer
        self.storage = storage

    async def _deserialize(self, pydantic_model: BasicViewEvent) -> dict[str, Any]:
        return await self.deserializer.deserialize(pydantic_model)

    async def save_to_storage(self, pydantic_model: BasicViewEvent) -> bool:
        data = await self._deserialize(pydantic_model)
        return await self.storage.save(topic="views", obj=data)


@lru_cache
def get_view_manager() -> ViewSerializerManager:
    return ViewSerializerManager(
        deserializer=KafkaDeserializer(), storage=KafkaStorage()
    )
