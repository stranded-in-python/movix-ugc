from uuid import UUID
from functools import lru_cache

from .abc import LikeServiceABC
from storages.abc import StorageABC

from models.likes import FilmLikes, FilmAverageScore, FilmEditScore, DeletedFilm


class LikeService(LikeServiceABC):
    def __init__(self, storage: StorageABC):
        self.storage = storage
    

    async def get_likes_by_id(self, film_id: UUID) -> FilmLikes | None:
        ...


    async def get_average_score_by_id(self, film_id: UUID) -> FilmAverageScore:
        ...


    async def edit_film_score(self, user_id: UUID, film_id: UUID, score: int) -> FilmEditScore:
        ...


    async def delete_film_score(self, user_id: UUID, film_id: UUID) -> DeletedFilm:
        ...


@lru_cache
def get_like_service() -> LikeService:
    # return FilmService(storage=FilmElasticStorage(manager=get_elastic_manager))
    pass
