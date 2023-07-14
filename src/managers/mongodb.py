from typing import Any

from bson.raw_bson import RawBSONDocument
from bson.typings import _DocumentType
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import InsertOneResult

from core.config import settings

from .abc import DBClient, MongoDBManagerABC


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
        # {'ok': 1.0}

    async def get(self, collection: str, *args, **kwargs) -> _DocumentType | None:
        return await self.get_client()[settings.mongo_db_name][collection].find_one(
            *args, **kwargs
        )

    # async def insert(self, collection: str, document: RawBSONDocument) -> InsertOneResult:
    # return await self.get_client()[settings.mongo_db_name][collection].insert_one(document)

    # данная конструкция создаст документ, если его нет и апдейтнет его в противном случае (параметр upsert)
    # return await self.get_client()[settings.mongo_db_name][collection].update_one(document, {'$set': document}, upsert=True)

    # async def update(self, collection: str, *args, **kwargs): # не додумал пока
    #     return await self.get_client()[settings.mongo_db_name][collection].update_one(upsert=True)
    #     # например update_one({'user_id': 'be19cf8d-4eb9-4fbd-a34f-71348e2dbd6b', 'score': 8}, {'$set': {'score': 7}})

    # insert + update
    async def upsert(
        self, collection: str, document: RawBSONDocument
    ) -> InsertOneResult:
        return await self.get_client()[settings.mongo_db_name][collection].update_one(
            document, {'$set': document}, upsert=True
        )

    async def get_average(
        self, collection: str, field: str, field_id: str, id: str
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
        # [{'_id': 'movie_id', 'avg_val': 9.0}]

    async def delete(self, collection: str, document: dict[str, Any]) -> None:
        col = self.get_client()[settings.mongo_db_name][collection]
        await col.delete_one(document)
        # likes.delete_one({"movie_id": "2abd36b6-d6cd-4286-bf6b-5d5950fba493"})
        # deleted_result.raw_result = {'n': 1, 'ok': 1.0}
        # deleted_result.deleted_count = 1


def get_mongo_manager() -> MongoDBManagerABC:
    """
    Получить instance менеджера
    """

    manager: MongoDBManagerABC | None = MongoDBManager.get_instance()
    if manager is None:
        manager = MongoDBManager(
            AsyncIOMotorClient(host=settings.mongo_host, port=settings.mongo_port)
        )
    return manager
