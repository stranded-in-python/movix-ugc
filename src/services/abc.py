from abc import ABC, abstractmethod
from uuid import UUID

from models.likes import FilmLikes, FilmAverageScore, FilmEditScore, DeletedFilm

class LikeServiceABC(ABC):
    @abstractmethod
    async def get_likes_by_id(self, film_id: UUID) -> FilmLikes | None:
        ...

    @abstractmethod
    async def get_average_score_by_id(self, film_id: UUID) -> FilmAverageScore:
        ...

    @abstractmethod
    async def edit_film_score(self, user_id: UUID, film_id: UUID, score: int) -> FilmEditScore:
        ...

    @abstractmethod
    async def delete_film_score(self, user_id: UUID, film_id: UUID) -> DeletedFilm:
        ...
# и здесь пошли другие