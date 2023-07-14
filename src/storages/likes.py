from typing import Callable
from uuid import UUID

from managers.mongodb import MongoDBManager
from models.likes import FilmAverageScore

from .abc import StorageABC


class LikeStorage(StorageABC):
    def __init__(self, manager: Callable[[], MongoDBManager]):
        self.manager = manager
        self.collection = 'likes'
        self.score_field = 'score'
        self.movie_id_field = 'movie_id'
        self.user_id_field = 'user_id'

    async def get_average_score(self, film_id: UUID):
        result = await self.manager().get_average(
            self.collection, self.score_field, self.movie_id_field, str(film_id)
        )
        if not result:
            return None
        return FilmAverageScore(film_id=film_id, average_score=result.get('avg_val'))

    async def delete_film_score(self, user_id: UUID, film_id: UUID):
        return await self.manager().delete(
            self.collection,
            {self.user_id_field: str(user_id), self.movie_id_field: str(film_id)},
        )
