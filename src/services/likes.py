from uuid import UUID

from .abc import LikeServiceABC
from storages.abc import StorageABC

from models.likes import FilmLikes, FilmAverageScore, FilmEditScore


class LikeService(LikeServiceABC):
    def __init__(self, storage: StorageABC):
        self.storage = storage

    async def get_likes_by_id(self, film_id: UUID) -> FilmLikes | None:
        film_likes = await self.storage.get_by_id(film_id)

        if not film_likes:
            return None
        return FilmLikes(**dict(film_likes))

    async def get_average_score_by_id(self, film_id: UUID) -> FilmAverageScore:
        ...

    async def edit_film_score(self, user_id: UUID, film_id: UUID, score: int) -> FilmEditScore:
        ...
