import datetime
from json import JSONEncoder


class JSNEncoder(JSONEncoder):
    """JSONEncoder for date type."""

    def default(self, obj):
        if isinstance(obj, datetime.date):
            return str(obj)
        return JSONEncoder.default(self, obj)
