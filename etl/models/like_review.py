from uuid import UUID

from .base import Like


class LikeReview(Like):
    review_id: UUID
    user_id: UUID
