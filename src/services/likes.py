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

    async def get_average_score_by_id(self, film_id: UUID) -> FilmAverageScore | None:
        return await self.storage.get_average_score(film_id)

    async def insert_film_score(
        self, user_id: UUID, film_id: UUID, score: int
    ) -> FilmEditScore:
        await self.storage.insert_film_score(user_id, film_id, score)
        return FilmEditScore(film_id=film_id, user_id=user_id, score=score)

    async def update_film_score(
        self, user_id: UUID, film_id: UUID, score: int
    ) -> FilmEditScore:
        await self.storage.insert_film_score(user_id, film_id, score)
        return FilmEditScore(film_id=film_id, user_id=user_id, score=score)

    async def delete_film_score(self, user_id: UUID, film_id: UUID) -> None:
        await self.storage.delete_film_score(
            user_id, film_id
        )  # не вижу смысла что-то возвращать

    async def get_likes(self, film_id: UUID) -> FilmLikes:
        return await self.storage.get_likes(film_id)


@lru_cache
def get_like_service() -> LikeService:
    return LikeService(storage=LikeStorage(get_mongo_manager))
