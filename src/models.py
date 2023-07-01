from typing import Annotated

from fastapi import Query
from pydantic import BaseModel, ValidationError, validator

from config import settings


class BasicViewEvent(BaseModel):

    value: Annotated[
        int, Query(title="Value.", description="Unix timestamp")
    ] = b"1688229214"
    key: Annotated[
        str, Query(title="Key.", description="Partitioning key like 'user_id+movie_id")
    ] = "UUID+UUID"
    topic: Annotated[
        str, Query(title="Topic.", description="Topic name to save to.")
    ] = settings.view_event

    @validator("key")
    def check_key(v):
        if len(v.split("+")) != 2:
            raise ValidationError
        else:
            return v
