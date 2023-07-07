from uuid import UUID

import pendulum
from pydantic import BaseModel


class Message(BaseModel):
    id: int
    user_id: UUID
    film_id: UUID
    frameno: int
    timestamp: pendulum.DateTime
