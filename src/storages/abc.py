from abc import ABC, abstractmethod
from typing import Any


class BrokerABC(ABC):
    @abstractmethod
    async def save(self, obj: dict[Any]):
        ...


class StorageABC(ABC):
    @abstractmethod
    async def get_by_id(self):
        ...
