from uuid import UUID

from .base import Like


class LikeMovie(Like):
    movie_id: UUID
    user_id: UUID
