from abc import ABC
from typing import Any

from pydantic import BaseModel


class BrokerDeserializer(ABC):
    async def deserialize(self, model: BaseModel) -> dict[Any, str]:
        ...


class KafkaDeserializer(BrokerDeserializer):
    async def deserialize(self, model: BaseModel) -> dict[str, str | bytes]:
        raw_dict = model.dict()
        deserialized_dict = {}
        deserialized_dict["key_binary"] = str(raw_dict.get("id")).encode("ascii")
        for key, val in raw_dict.items():
            deserialized_dict[key] = str(val)
        return deserialized_dict
