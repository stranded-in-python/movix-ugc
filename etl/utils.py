from json import JSONEncoder
from uuid import UUID
from datetime import datetime


class UUIDEncoder(JSONEncoder):
    """JSONEncoder for UUID type."""
    def default(self, obj):
        if isinstance(obj, UUID) or isinstance(obj, datetime):
            return str(obj)
        return JSONEncoder.default(self, obj)