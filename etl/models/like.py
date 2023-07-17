from uuid import UUID

import pendulum
from pydantic import BaseModel


class Like(BaseModel):
    id: int
    movie_id: UUID
    user_id: UUID
    score: int
    timestamp: pendulum.DateTime
