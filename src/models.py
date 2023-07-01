from typing import Annotated

from pydantic import BaseModel, ValidationError, validator
from fastapi import Query
from config import settings


class BasicViewEvent(BaseModel):

    value: Annotated[bytes | int, Query(title="Value.", description="Unix timestamp")] = b'1688229214'
    key: Annotated[bytes | str, Query(title="Key.", description="Partitioning key like 'user_id+movie_id")] = "UUID+UUID"
    topic: Annotated[bytes | str, Query(title="Topic.", description="Topic name to save to.")] = settings.view_event

    @validator("key")
    def check_key(key):
        key = str(key)
        if len(key.split("+")) != 2:
            raise ValidationError
