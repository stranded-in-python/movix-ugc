from abc import ABC, abstractmethod
from uuid import UUID

from models.likes import FilmAverageScore, FilmEditScore, FilmLikes
from models.bookmarks import Bookmark, ShortBookmark

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


class BookmarkServiceABC(ABC):
    async def insert_bookmark(
            self, user_id: UUID, film_id: UUID 
    ) -> Bookmark:
        ...

    async def delete_bookmark(
            self, user_id: UUID, film_id: UUID
    ) -> Bookmark:
        ...
    
    async def get_bookmarks(
            self, user_id: UUID
    ) -> list[ShortBookmark]:
        ...
