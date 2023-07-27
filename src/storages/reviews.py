from datetime import datetime
from typing import Callable
from uuid import UUID, uuid4

import pymongo

from core.pagination import PaginateQueryParams
from managers.mongodb import MongoDBManager
from models.reviews import Review, ReviewLikes

from .abc import StorageABC


class ReviewStorage(StorageABC):
    def __init__(self, manager: Callable[[], MongoDBManager]):
        self.manager = manager
        self.review_collection = 'reviews'
        self.review_score_collection = 'reviews_likes'
        self.score_field = 'score'
        self.text_field = 'text'
        self.timestamp_field = 'timestamp'
        self.likes_field = 'likes'
        self.dislikes_field = 'dislikes'
        self.movie_id_field = 'film_id'
        self.user_id_field = 'user_id'
        self.review_id_field = 'review_id'

    def _sort_2_order(self, sort: str | None) -> tuple(str, int):
        if not sort:
            return self.review_id_field, pymongo.ASCENDING

        match sort[0]:
            case "+":
                return sort[1:], pymongo.ASCENDING
            case "-":
                return sort[1:], pymongo.DESCENDING
            case _:
                return self.review_id_field, pymongo.ASCENDING

    def _pagination_2_query_args(
        self, pagination: None | PaginateQueryParams
    ) -> tuple(int, int):
        if not pagination:
            return 0, 50
        return (
            (pagination.page_number - 1) * pagination.page_size
            if pagination.page_number > 0
            else 0,
            pagination.page_size,
        )

    async def get(self, *args) -> list[Review] | None:
        reviews: list | None = await self.manager().get(*args)
        if not reviews:
            return None
        return reviews

    async def insert(
        self, user_id: UUID, film_id: UUID, text: str, score: int
    ) -> Review:
        old_review = await self.get(
            self.review_collection,
            {
                self.user_id_field: {"$eq": user_id},
                self.movie_id_field: {"$eq": film_id},
            },
        )
        if old_review:
            old_review = [Review(**doc) for doc in old_review]
            return old_review[0]
        new_review = {
            self.review_id_field: uuid4(),
            self.user_id_field: user_id,
            self.movie_id_field: film_id,
            self.text_field: text,
            self.score_field: score,
            self.dislikes_field: 0,
            self.likes_field: 0,
            self.timestamp_field: datetime.now(),
        }
        await self.manager().insert(self.review_collection, new_review)
        return Review(**new_review)

    async def insert_review_score(
        self, user_id: UUID, review_id: UUID, score: int
    ) -> ReviewLikes:
        upsert_result = await self.manager().upsert(
            self.review_score_collection,
            {self.user_id_field: user_id, self.review_id_field: review_id},
            {
                "$set": {
                    self.user_id_field: user_id,
                    self.review_id_field: review_id,
                    self.score_field: score,
                    self.timestamp_field: datetime.now(),
                }
            },
        )
        if upsert_result.modified_count != 0:
            field_to_inc = self.likes_field if score == 10 else self.dislikes_field
            field_to_dec = self.dislikes_field if score == 10 else self.likes_field
            await self.manager().upsert(
                self.review_collection,
                {self.user_id_field: user_id, self.review_id_field: review_id},
                {'$inc': {field_to_inc: +1, field_to_dec: -1}},
            )
        return ReviewLikes(user_id=user_id, review_id=review_id, score=score)

    async def get_sorted_reviews(
        self, film_id: UUID, sort: str | None, pagination: PaginateQueryParams
    ) -> list[Review] | None:
        sort_field, order = self._sort_2_order(sort)
        page_number, page_size = self._pagination_2_query_args()
        reviews = await self.manager().get_and_sort(
            self.review_collection,
            sort_field,
            order,
            page_number,
            page_size,
            {self.movie_id_field: film_id},
        )
        if not reviews:
            return None
        return [Review(**doc) for doc in reviews]

    async def delete(*args, **kwargs):
        raise NotImplementedError
