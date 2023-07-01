from abc import ABC, abstractmethod
from typing import Any
from functools import lru_cache

from pydantic import BaseModel

from serializers import EventSerializerABC, EventSerializer
from models import BasicViewEvent

class ViewServiceABC(ABC):
    def __init__(self, deserializer: EventSerializerABC):
        self.deserializer = deserializer

    @abstractmethod
    async def deserialize_to_binary(self, pydantic_model: BaseModel) -> dict[str, bytes]:
        await self.deserializer.deserialize_to_binary(pydantic_model.dict())


class ViewService(ViewServiceABC):
    def __init__(self, serializer: EventSerializerABC):
        self.deserializer = serializer

    async def deserialize_to_binary(self, pydantic_model: BasicViewEvent) -> dict[str, bytes]:
        return await self.deserializer.deserialize_to_binary(pydantic_model.dict())

@lru_cache
def get_view_service() -> ViewService:
    return ViewService(serializer=EventSerializer())
