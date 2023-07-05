from pydantic import BaseModel
import pendulum
from uuid import UUID


class Message(BaseModel):
    id: int
    user_id: UUID
    film_id: UUID
    frameno: int
    timestamp: pendulum.DateTime
