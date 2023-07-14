from functools import lru_cache
from uuid import UUID

from managers.mongodb import get_mongo_manager
from models.likes import FilmAverageScore, FilmEditScore, FilmLikes
from storages.abc import StorageABC
from storages.likes import LikeStorage

from .abc import LikeServiceABC


class LikeService(LikeServiceABC):
    def __init__(self, storage: StorageABC):
        self.storage = storage

    async def get_likes_by_id(self, film_id: UUID) -> FilmLikes | None:
        pass

    async def get_average_score_by_id(self, film_id: UUID) -> FilmAverageScore | None:
        return await self.storage.get_average_score(film_id)

    async def edit_film_score(
        self, user_id: UUID, film_id: UUID, score: int
    ) -> FilmEditScore:
        pass

    async def delete_film_score(self, user_id: UUID, film_id: UUID) -> None:
        await self.storage.delete_film_score(
            user_id, film_id
        )  # не вижу смысла что-то возвращать


@lru_cache
def get_like_service() -> LikeService:
    return LikeService(storage=LikeStorage(get_mongo_manager))
