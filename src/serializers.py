from abc import ABC, abstractmethod

class EventSerializerABC(ABC):
    
    @abstractmethod
    async def deserialize_to_binary(d: dict[str, str]) -> dict[str, bytes]:
        ...


class EventSerializer(EventSerializerABC):
        
    async def deserialize_to_binary(self, d: dict[str, str]) -> dict[str, bytes]:
        new_d = {}
        for key, val in d.items():
            new_d[key] = str(val).encode("utf-8")
        # {'value': b'5', 'key': b'UUID+UUID', 'topic': b'views'}
        return new_d
