from uuid import UUID

from .base import Score


class ReviewScore(Score):
    review_id: UUID
    user_id: UUID
