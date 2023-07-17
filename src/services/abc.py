from abc import ABC, abstractmethod
from uuid import UUID

from models.likes import DeletedFilm, FilmAverageScore, FilmEditScore, FilmLikes


class LikeServiceABC(ABC):
    @abstractmethod
    async def get_average_score_by_id(self, film_id: UUID) -> FilmAverageScore:
        ...

    @abstractmethod
    async def insert_film_score(
        self, user_id: UUID, film_id: UUID, score: int
    ) -> FilmEditScore:
        ...

    @abstractmethod
    async def update_film_score(
        self, user_id: UUID, film_id: UUID, score: int
    ) -> FilmEditScore:
        ...

    @abstractmethod
    async def delete_film_score(self, user_id: UUID, film_id: UUID) -> None:
        ...

    @abstractmethod
    async def get_likes(self, film_id: UUID) -> FilmLikes | None:
        ...


# и здесь пошли другие
