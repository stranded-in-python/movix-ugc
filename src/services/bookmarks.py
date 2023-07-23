from datetime import datetime
from functools import lru_cache
from uuid import UUID

from managers.mongodb import get_mongo_manager
from models.bookmarks import Bookmark, ShortBookmark
from storages.abc import StorageABC
from storages.bookmarks import BookmarkStorage

from .abc import BookmarkServiceABC


class BookmarkService(BookmarkServiceABC):
    def __init__(self, storage: StorageABC):
        self.storage = storage

    async def insert_bookmark(self, user_id: UUID, film_id: UUID) -> Bookmark:
        now = datetime.now()
        await self.storage.insert(user_id, film_id, now)
        return Bookmark(user_id=user_id, film_id=film_id, timestamp=now)

    async def delete_bookmark(self, user_id: UUID, film_id: UUID) -> Bookmark:
        await self.storage.delete(user_id, film_id)

    async def get_bookmarks(self, user_id: UUID) -> list[ShortBookmark]:
        return await self.storage.get(user_id)


@lru_cache
def get_bookmark_service() -> BookmarkService:
    return BookmarkService(storage=BookmarkStorage(get_mongo_manager))
