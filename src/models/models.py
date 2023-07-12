from datetime import datetime
from uuid import UUID

from .mixins import UUIDMixin


class User(UUIDMixin):
    user_id: UUID
    access_rights: list[str] | None = None
    auth_timeout: bool = False


class UserViewEvent(User):
    film_id: UUID
    timestamp: datetime
    frameno: int


class BasicViewEvent(UUIDMixin):
    film_id: UUID
    timestamp: datetime
    frameno: int
