from datetime import datetime
from typing import Callable
from uuid import UUID

from managers.mongodb import MongoDBManager
from models.bookmarks import ShortBookmark

from .abc import StorageABC


class BookmarkStorage(StorageABC):
    def __init__(self, manager: Callable[[], MongoDBManager]):
        self.manager = manager
        self.collection = 'bookmarks'
        self.timestamp_field = 'timestamp'
        self.movie_id_field = 'film_id'
        self.user_id_field = 'user_id'

    async def insert_bookmark(
        self, user_id: UUID, film_id: UUID, timestamp: datetime
    ) -> None:
        await self.manager().upsert(
            self.collection,
            {self.user_id_field: user_id, self.movie_id_field: film_id},
            {
                self.user_id_field: user_id,
                self.movie_id_field: film_id,
                self.timestamp_field: timestamp,
            },
        )

    async def delete_bookmark(self, user_id: UUID, film_id: UUID) -> None:
        await self.manager().delete(
            self.collection, {self.user_id_field: user_id, self.movie_id_field: film_id}
        )

    async def get_bookmarks(self, user_id: UUID) -> list[ShortBookmark] | None:
        bookmarks: list | None = await self.manager().get(
            self.collection, {self.user_id_field: {"$eq": user_id}}
        )
        if not bookmarks:
            return None
        return [ShortBookmark(**doc) for doc in bookmarks]
