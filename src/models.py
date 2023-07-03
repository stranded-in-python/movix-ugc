from typing import Annotated
from uuid import UUID

from pydantic import BaseModel


class BasicViewEvent(BaseModel):

    id: UUID
    user_id: UUID
    film_id: UUID
    timestamp: UUID
    frameno: float
