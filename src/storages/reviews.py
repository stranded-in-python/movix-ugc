from datetime import datetime
from typing import Callable
from uuid import UUID, uuid4

from managers.mongodb import MongoDBManager
from models.reviews import Review, ReviewLikes

from .abc import StorageABC


class ReviewStorage(StorageABC):
    def __init__(self, manager: Callable[[], MongoDBManager]):
        self.manager = manager
        self.review_collection = 'rv'
        self.review_score_collection = 'review_likes'
        self.score_field = 'score'
        self.text_field = 'text'
        self.timestamp_field = 'timestamp'
        self.likes_field = 'likes'
        self.dislikes_field = 'dislikes'
        self.movie_id_field = 'film_id'
        self.user_id_field = 'user_id'
        self.review_id_field = 'review_id'

    async def get_reviews(self, *args) -> list[Review] | None:
        reviews: list | None = await self.manager().get(*args)
        if not reviews:
            return None
        return [Review(**doc) for doc in reviews]

    async def insert_review(self, user_id: UUID, film_id: UUID, text: str, score: int) -> Review:
        old_review = await self.get_reviews(self.review_collection, {self.user_id_field: {"$eq": user_id}, self.movie_id_field: {"$eq": film_id}})
        if not old_review:
            new_review = {
                    self.review_id_field: uuid4(),
                    self.user_id_field: user_id,
                    self.movie_id_field: film_id,
                    self.text_field: text,
                    self.score_field: score,
                    self.dislikes_field: 0,
                    self.likes_field: 0,
                    self.timestamp_field: datetime.now()
            }
            await self.manager().insert(
                self.review_collection,
                new_review
            )
            return Review(**new_review)
        return old_review[0]

    async def insert_review_score(self, user_id: UUID, review_id: UUID, score: int) -> ReviewLikes:
        await self.manager().upsert(
            self.review_score_collection,
            {self.user_id_field: user_id, self.review_id_field: review_id},
            {
                self.user_id_field: user_id,
                self.review_id_field: review_id,
                self.score_field: score,
            },
        )
        return ReviewLikes(user_id=user_id, review_id=review_id, score=score)



    # async def get_reviews(self,):
    #     pass


#     async def get_average_score(self, film_id: UUID) -> FilmAverageScore:
#         result = await self.manager().get_average(
#             self.collection, self.score_field, self.movie_id_field, film_id
#         )
#         if not result:
#             return None
#         return FilmAverageScore(film_id=film_id, average_score=result.get('avg_val'))

#     async def get_likes(self, film_id: UUID) -> FilmLikes:
#         likes = await self.manager().get_count(
#             self.collection, {self.movie_id_field: film_id, self.score_field: 10}
#         )
#         dislikes = await self.manager().get_count(
#             self.collection, {self.movie_id_field: film_id, self.score_field: 0}
#         )
#         return FilmLikes(
#             film_id=film_id, likes=likes.get("count"), dislikes=dislikes.get("count")
#         )

#     async def delete_film_score(self, user_id: UUID, film_id: UUID) -> None:
#         await self.manager().delete(
#             self.collection, {self.user_id_field: user_id, self.movie_id_field: film_id}
#         )

#     async def insert_film_score(self, user_id: UUID, film_id: UUID, score: int):
#         await self.manager().upsert(
#             self.collection,
#             {self.user_id_field: user_id, self.movie_id_field: film_id},
#             {
#                 self.user_id_field: user_id,
#                 self.movie_id_field: film_id,
#                 self.score_field: score,
#             },
#         )

#     async def update_film_score(self, user_id: UUID, film_id: UUID, score: int):
#         await self.manager().upsert(
#             self.collection,
#             {self.user_id_field: user_id, self.movie_id_field: film_id},
#             {
#                 self.user_id_field: user_id,
#                 self.movie_id_field: film_id,
#                 self.score_field: score,
#             },
#         )


# # аггрегация лайков И дислайков. Пока отказываюсь, так как хз как реализовать по ООПшному
# # next(likes.aggregate([{"$facet": {"likes": [{"$match": {"movie_id": "bb1a3666-dac1-4f7c-bcdd-95df42609d48", "score": 7}}, {"$count": "count"}], "dislikes": [{"$match": {"movie_id": "bb1a3666-dac1-4f7c-bcdd-95df42609d48", "score": 7}}, {"$count": "count"}]}}]))
