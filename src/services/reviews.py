from functools import lru_cache
from uuid import UUID

from managers.mongodb import get_mongo_manager
from models.reviews import Review, ReviewLikes
# from models.likes import FilmAverageScore, FilmEditScore, FilmLikes

from storages.abc import StorageABC
from storages.reviews import ReviewStorage

from .abc import ReviewServiceABC


class ReviewService(ReviewServiceABC):
    def __init__(self, storage: StorageABC):
        self.storage = storage

    # async def get_likes(self, film_id: UUID) -> FilmLikes:
    #     return await self.storage.get_likes(film_id)

    async def insert_review(self, user_id: UUID, film_id: UUID, text: str, score: int) -> Review:
        return await self.storage.insert_review(user_id, film_id, text, score)
    
    async def insert_review_score(self, user_id: UUID, review_id: UUID, score: int) -> ReviewLikes:
        return await self.manager.insert_review_score(user_id, review_id, score)
    
    async def get_reviews(self):
        pass


@lru_cache
def get_like_service() -> ReviewService:
    return ReviewService(storage=ReviewStorage(get_mongo_manager))
