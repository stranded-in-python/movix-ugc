from pydantic import BaseModel

from .abc import Deserializer


class KafkaDeserializer(Deserializer):
    async def deserialize(self, model: BaseModel) -> dict[str, str | bytes]:
        raw_dict = model.dict()
        deserialized_dict = {}
        deserialized_dict["key_binary"] = str(raw_dict.get("id")).encode("ascii")
        for key, val in raw_dict.items():
            deserialized_dict[key] = str(val)
        return deserialized_dict
