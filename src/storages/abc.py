from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class BrokerABC(ABC):
    @abstractmethod
    async def save(self, obj: dict[Any]):
        ...


class StorageABC(ABC):
    @abstractmethod
    async def insert(self, *args, **kwargs) -> None:
        ...

    @abstractmethod
    async def get(self, *args, **kwargs) -> BaseModel:
        ...

    @abstractmethod
    async def delete(self, *args, **kwargs) -> None:
        ...

    # @abstractmethod
    # async def get_count(self, *args, **kwargs) -> None:
    #     ...

    # @abstractmethod
    # async def get_average(self, *args, **kwargs) -> None:
    #     ...
