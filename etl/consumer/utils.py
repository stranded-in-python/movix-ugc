import json


def json_decoder(value):
    return json.loads(value.decode())
