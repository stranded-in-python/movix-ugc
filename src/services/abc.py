from abc import ABC, abstractmethod
from uuid import UUID

from models.bookmarks import Bookmark, ShortBookmark
from models.likes import FilmAverageScore, FilmEditScore, FilmLikes
from models.reviews import Review, ReviewLikes


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
    @abstractmethod
    async def insert_bookmark(self, user_id: UUID, film_id: UUID) -> Bookmark:
        ...

    @abstractmethod
    async def delete_bookmark(self, user_id: UUID, film_id: UUID) -> Bookmark:
        ...

    @abstractmethod
    async def get_bookmarks(self, user_id: UUID) -> list[ShortBookmark] | None:
        ...


class ReviewServiceABC(ABC):
    @abstractmethod
    async def insert_review(
        self, user_id: UUID, film_id: UUID, text: str, score: int
    ) -> Review:
        ...

    @abstractmethod
    async def insert_review_score(
        self, user_id: UUID, review_id: UUID, score: int
    ) -> ReviewLikes:
        ...

    @abstractmethod
    async def get_reviews(self) -> list[Review] | None:
        ...
