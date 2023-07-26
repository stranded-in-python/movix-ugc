from uuid import UUID

from .base import Score


class Review(Score):
    review_id: UUID
    user_id: UUID
    movie_id: UUID
    text: str
