from datetime import datetime
from uuid import UUID

from .mixins import FilmIDMixin, UUIDMixin


class User(UUIDMixin, FilmIDMixin):
    user_id: UUID
    access_rights: list[str] | None = None
    auth_timeout: bool = False


class UserViewEvent(User):
    timestamp: datetime
    frameno: int


class BasicViewEvent(UUIDMixin, FilmIDMixin):
    timestamp: datetime
    frameno: int
