from functools import lru_cache
from uuid import UUID

from core.pagination import PaginateQueryParams
from managers.mongodb import get_mongo_manager
from models.reviews import Review, ReviewLikes
from storages.abc import StorageABC
from storages.reviews import ReviewStorage

from .abc import ReviewServiceABC


class ReviewService(ReviewServiceABC):
    def __init__(self, storage: StorageABC):
        self.storage = storage

    async def insert_review(
        self, user_id: UUID, film_id: UUID, text: str, score: int
    ) -> Review:
        return await self.storage.insert(user_id, film_id, text, score)

    async def insert_review_score(
        self, user_id: UUID, review_id: UUID, score: int
    ) -> ReviewLikes:
        return await self.storage.insert_review_score(user_id, review_id, score)

    async def get_reviews(
        self, film_id: UUID, sort: str | None, pagination: PaginateQueryParams | None
    ) -> list[Review] | None:
        return await self.storage.get_sorted_reviews(film_id, sort, pagination)


@lru_cache
def get_review_service() -> ReviewService:
    return ReviewService(storage=ReviewStorage(get_mongo_manager))
