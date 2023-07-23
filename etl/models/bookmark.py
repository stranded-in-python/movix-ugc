from uuid import UUID

from .base import Base


class Bookmark(Base):
    movie_id: UUID
    user_id: UUID
