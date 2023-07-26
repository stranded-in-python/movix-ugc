from datetime import datetime
from uuid import UUID

from .mixins import FilmIDMixin


class Bookmark(FilmIDMixin):
    user_id: UUID
    timestamp: datetime


class ShortBookmark(FilmIDMixin):
    timestamp: datetime
