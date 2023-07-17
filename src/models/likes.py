from uuid import UUID

from .mixins import FilmIDMixin


class FilmLikes(FilmIDMixin):
    likes: int
    dislikes: int


class FilmAverageScore(FilmIDMixin):
    average_score: float


class FilmEditScore(FilmIDMixin):
    user_id: UUID
    score: int


class DeletedFilm(FilmIDMixin):
    pass
