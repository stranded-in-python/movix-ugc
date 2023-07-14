from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class BrokerABC(ABC):
    @abstractmethod
    async def save(self, obj: dict[Any]):
        ...


class StorageABC(ABC):
    @abstractmethod
    async def get_average_score(self, id: UUID):
        ...
