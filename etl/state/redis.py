import redis
from backoff import on_exception
from logger import logger


class Storage:
    def __init__(self, base_key: str, host: str, port: int, db: int = 0):
        self._redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.key = base_key

    def _gen_key(self, partition: int):
        return f"{self.key}:{str(partition)}"

    @on_exception(redis.ConnectionError, logger)
    def save(self, partition: int, value: int):
        self._redis.set(self._gen_key(partition), value)

    @on_exception(redis.ConnectionError, logger)
    def retrieve(self, partition: int) -> int:
        result = 0
        value = self._redis.get(self._gen_key(partition))
        if value:
            result = int(value)
        return result
