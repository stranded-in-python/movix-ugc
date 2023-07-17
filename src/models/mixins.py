from uuid import UUID

from pydantic import BaseModel


class UUIDMixin(BaseModel):
    id: UUID


class FilmIDMixin(BaseModel):
    film_id: UUID