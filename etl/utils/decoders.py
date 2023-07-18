import datetime
import json
import uuid


def json_decoder(value):
    return json.loads(value.decode())


def decode_uuid(binary):
    return uuid.UUID(bytes=binary)


class MyEncoder(json.JSONEncoder):
    """JSONEncoder for date type."""

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
