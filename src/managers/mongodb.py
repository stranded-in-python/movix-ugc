from typing import Any
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import InsertOneResult

from core.config import settings
from core.logger import logger

from .abc import DBClient, MongoDBManagerABC

logger()


class MongoDBClient(AsyncIOMotorClient, DBClient):
    """Обёртка для Mongodb"""

    ...


class MongoDBManager(MongoDBManagerABC):
    """
    Singleton для управления соединением с mongodb
    """

    def __init__(self, client: AsyncIOMotorClient):
        super().__init__(client)
        self._client: AsyncIOMotorClient

    def get_client(self) -> AsyncIOMotorClient:
        return self._client

    async def on_startup(self) -> dict[str, float]:
        return await self._client.admin.command('ping')

    async def get(self, collection: str, *args) -> list[dict[str, Any]] | None:
        return (
            await self.get_client()[settings.mongo_db_name][collection]
            .find(*args)
            .to_list(length=None)
        )

    async def get_and_sort(
        self,
        collection: str,
        sort_field: str,
        order: int,
        page_number: int,
        page_size: int,
        *args,
    ) -> list[dict[str, Any]] | None:
        return (
            await self.get_client()[settings.mongo_db_name][collection]
            .find(*args)
            .sort(sort_field, order)
            .skip(page_number)
            .limit(page_size)
            .to_list(length=None)
        )

    async def insert(self, collection: str, *args):
        await self.get_client()[settings.mongo_db_name][collection].insert_one(*args)

    async def upsert(self, collection: str, *args) -> InsertOneResult:
        result = await self.get_client()[settings.mongo_db_name][collection].update_one(
            *args, upsert=True
        )
        return result

    async def get_average(
        self, collection: str, field: str, field_id: str, id: UUID
    ) -> dict[str, Any] | None:
        col = self.get_client()[settings.mongo_db_name][collection]
        result = await col.aggregate(
            [
                {"$match": {field_id: id}},
                {'$group': {'_id': field_id, 'avg_val': {'$avg': f"${field}"}}},
            ]
        ).to_list(length=1)
        try:
            return result[0]
        except IndexError:
            return None

    async def get_count(
        self, collection: str, document: dict[str, Any]
    ) -> dict[str, int]:
        col = self.get_client()[settings.mongo_db_name][collection]
        result = await col.aggregate(
            [{"$match": document}, {"$count": "count"}]
        ).to_list(length=1)
        try:
            return result[0]
        except IndexError:
            return {'count': 0}

    async def delete(self, collection: str, document: dict[str, Any]) -> None:
        col = self.get_client()[settings.mongo_db_name][collection]
        return await col.delete_one(document)


def get_mongo_manager() -> MongoDBManagerABC:
    """
    Получить instance менеджера
    """

    manager: MongoDBManagerABC | None = MongoDBManager.get_instance()
    if manager is None:
        manager = MongoDBManager(
            AsyncIOMotorClient(
                host=settings.mongo_host,
                port=settings.mongo_port,
                uuidRepresentation='standard',
            )
        )
    return manager
