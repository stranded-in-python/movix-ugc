from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class BrokerABC(ABC):
    @abstractmethod
    async def save(self, obj: dict[Any]):
        ...


class StorageABC(ABC):
    pass
