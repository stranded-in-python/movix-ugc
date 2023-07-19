from uuid import UUID

from .base import Like


class Review(Like):
    review_id: UUID
    user_id: UUID
    movie_id: UUID
    text: str
