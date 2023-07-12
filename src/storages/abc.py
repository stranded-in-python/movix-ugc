from abc import ABC, abstractmethod
from typing import Any


class StorageABC(ABC):
    @abstractmethod
    async def save(obj: dict[Any]):
        ...
