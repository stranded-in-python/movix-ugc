from uuid import UUID

from pydantic import BaseModel


class UUIDMixin(BaseModel):
    id: UUID


class FilmIDMixin(BaseModel):
    film_id: UUID  # = Field(alias='movie_id')


class ReviewIDMixin(BaseModel):
    review_id: UUID
