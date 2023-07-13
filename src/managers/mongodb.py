from typing import Any
from bson.raw_bson import RawBSONDocument
from bson.typings import _DocumentType

from pymongo.results import InsertOneResult
from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings
from .abc import DBClient, MongoDBManagerABC

class MongoDBClient(AsyncIOMotorClient, DBClient):
    """Обёртка для ElasticSearch"""

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
    
    async def on_startup(self):
        await self._client.admin.command('ping')

    async def get(self, collection: str, *args, **kwargs) -> _DocumentType | None:
        return await self.get_client()[settings.mongo_db_name][collection].find_one(*args, **kwargs)

    # async def insert(self, collection: str, document: RawBSONDocument) -> InsertOneResult:
    #     # return await self.get_client()[settings.mongo_db_name][collection].insert_one(document)
    #     # данная конструкция создаст документ, если его нет и апдейтнет его в противном случае
    #     return await self.get_client()[settings.mongo_db_name][collection].update_one(document, {'$set': document}, upsert=True)

    # async def update(self, collection: str, *args, **kwargs): # не додумал пока
    #     return await self.get_client()[settings.mongo_db_name][collection].update_one(upsert=True)
    #     # например update_one({'user_id': 'be19cf8d-4eb9-4fbd-a34f-71348e2dbd6b', 'score': 8}, {'$set': {'score': 7}})

    # insert + update
    async def upsert(self, collection: str, document: RawBSONDocument) -> InsertOneResult:
        return await self.get_client()[settings.mongo_db_name][collection].update_one(document, {'$set': document}, upsert=True)

    async def get_average(self, collection: str, field: str, field_id: str, id: str) -> dict[str, Any]:
        aggregation = await self.get_client()[settings.mongo_db_name][collection] \
            .aggregate([{"$match": { field_id: id}},{'$group': {'_id': None, 'avg_val':{'$avg':f"${field}"}}}])
        return next(aggregation)
        # {'_id': 'movie_id', 'avg_val': 7.0}

def get_manager() -> MongoDBManagerABC:
    """
    Получить instance менеджера
    """

    manager: MongoDBManagerABC | None = MongoDBManager.get_instance()
    if manager is None:
        manager = MongoDBManager(MongoDBClient(host=settings.mongo_host, port=settings.mongo_port))
    return manager
