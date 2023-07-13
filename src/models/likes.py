from uuid import UUID

from pydantic import BaseModel

from .mixins import FilmIDMixin

class FilmLikes(FilmIDMixin):
    likes: int


class FilmAverageScore(FilmIDMixin):
    average_score: float


class FilmEditScore(FilmIDMixin):
    user_id: UUID
    score: int
