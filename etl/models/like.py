from uuid import UUID

import pendulum
from pydantic import BaseModel, validator


class Like(BaseModel):
    # id: int
    movie_id: UUID
    user_id: UUID
    score: int
    timestamp: pendulum.DateTime

    @validator('timestamp', pre=True)
    def ensure_date_range(cls, v):
        return pendulum.parse(v)
