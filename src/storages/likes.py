from typing import Callable
from uuid import UUID

from managers.mongodb import MongoDBManager
from models.likes import FilmAverageScore, FilmLikes

from .abc import StorageABC


class LikeStorage(StorageABC):
    def __init__(self, manager: Callable[[], MongoDBManager]):
        self.manager = manager
        self.collection = 'likes'
        self.score_field = 'score'
        self.movie_id_field = 'film_id'
        self.user_id_field = 'user_id'

    async def get_average_score(self, film_id: UUID) -> FilmAverageScore:
        result = await self.manager().get_average(
            self.collection, self.score_field, self.movie_id_field, film_id
        )
        if not result:
            return None
        return FilmAverageScore(film_id=film_id, average_score=result.get('avg_val'))

    async def get_likes(self, film_id: UUID) -> FilmLikes:
        likes = await self.manager().get_count(
            self.collection, {self.movie_id_field: film_id, self.score_field: 10}
        )
        dislikes = await self.manager().get_count(
            self.collection, {self.movie_id_field: film_id, self.score_field: 0}
        )
        return FilmLikes(
            film_id=film_id, likes=likes.get("count"), dislikes=dislikes.get("count")
        )

    async def delete_film_score(self, user_id: UUID, film_id: UUID) -> None:
        await self.manager().delete(
            self.collection, {self.user_id_field: user_id, self.movie_id_field: film_id}
        )

    async def insert_film_score(self, user_id: UUID, film_id: UUID, score: int) -> None:
        await self.manager().upsert(
            self.collection,
            {self.user_id_field: user_id, self.movie_id_field: film_id},
            {
                self.user_id_field: user_id,
                self.movie_id_field: film_id,
                self.score_field: score,
            },
        )

    async def update_film_score(self, user_id: UUID, film_id: UUID, score: int) -> None:
        await self.manager().upsert(
            self.collection,
            {self.user_id_field: user_id, self.movie_id_field: film_id},
            {
                self.user_id_field: user_id,
                self.movie_id_field: film_id,
                self.score_field: score,
            },
        )
