from abc import ABC
from typing import Any

from pydantic import BaseModel


class Deserializer(ABC):
    async def deserialize(self, model: BaseModel) -> dict[Any, str]:
        ...
