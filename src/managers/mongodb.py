from typing import Any
from uuid import UUID

from bson.typings import _DocumentType
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
        # {'ok': 1.0}

    async def get(self, collection: str, *args) -> list[dict[str, Any]] | None:
        print(*args)
        return await self.get_client()[settings.mongo_db_name][collection].find(*args).to_list(length=None)

    async def insert(self, collection: str, *args):
        print(*args)
        await self.get_client()[settings.mongo_db_name][collection].insert_one(*args)

    # likes.find_one({'user_id': 'f158bd08-975d-4ac1-8f7d-c07c9a053c13', 'movie_id': 'bb1a3666-dac1-4f7c-bcdd-95df42609d48'})

    # print(likes.update_one({'user_id': 'f158bd08-975d-4ac1-8f7d-c07c9a053c13', 'movie_id': 'bb1a3665-dac1-4f7c-bcdd-95df42609d48'}, {'$set': {'score': 7}}, upsert=True))

    # print([doc for doc in likes.find({"$and": [{ 'movie_id': { '$eq': "89b13f05-dce8-4966-a6d8-6324102c6ba8" } }, {'user_id': {'$eq': '67274148-5798-4b04-9f42-78f339ac62c'}}]})])
    # print(likes.find_one({"$and": [{ 'movie_id': "89b13f05-dce8-4966-a6d8-6324102c6ba8" } , {'user_id': '67274148-5798-4b04-9f42-78f339ac62c'}]})
    # async def insert(self, collection: str, document: RawBSONDocument) -> InsertOneResult:
    # return await self.get_client()[settings.mongo_db_name][collection].insert_one(document)

    # данная конструкция создаст документ, если его нет и апдейтнет его в противном случае (параметр upsert)
    # return await self.get_client()[settings.mongo_db_name][collection].update_one(document, {'$set': document}, upsert=True)

    # async def update(self, collection: str, *args, **kwargs): # не додумал пока
    #     return await self.get_client()[settings.mongo_db_name][collection].update_one(upsert=True)
    #     # например update_one({'user_id': 'be19cf8d-4eb9-4fbd-a34f-71348e2dbd6b', 'score': 8}, {'$set': {'score': 7}})

    # insert + update
    async def upsert(
        self, collection: str, filters: dict[str, Any], document: dict[str, Any]
    ) -> InsertOneResult:
        # данная конструкция создаст документ, если его нет и апдейтнет его в противном случае (параметр upsert)
        result = await self.get_client()[settings.mongo_db_name][collection].update_one(
            filters, {'$set': document}, upsert=True
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
        # [{'_id': 'movie_id', 'avg_val': 9.0}]

    async def get_count(
        self, collection: str, document: dict[str, Any]
    ) -> dict[str, int]:
        col = self.get_client()[settings.mongo_db_name][collection]
        result = await col.aggregate(
            [{"$match": document}, {"$count": "count"}]
        ).to_list(length=1)
        try:
            return result[0]  # {'count': 1}
        except IndexError:
            return {'count': 0}

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
            AsyncIOMotorClient(
                host=settings.mongo_host,
                port=settings.mongo_port,
                uuidRepresentation='standard',
            )
        )
    return manager
