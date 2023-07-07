from functools import wraps
from random import getrandbits
from time import time

from faker import Faker

fake = Faker()


async def generate_random_data_async(
    rows: int = 10_000_000, batch_size: int = 1000
) -> list[dict]:
    for _ in range(int(rows / batch_size)):
        random_batch = []
        for _ in range(batch_size):
            random_batch.append(
                {
                    "id": getrandbits(33),
                    "user_id": getrandbits(33),
                    "film_id": getrandbits(33),
                    "timestamp": fake.date_time_between(),
                }
            )
        yield random_batch


def generate_random_data(rows: int = 10_000_000, batch_size: int = 1000) -> list[dict]:
    for _ in range(int(rows / batch_size)):
        random_batch = []
        for _ in range(batch_size):
            random_batch.append(
                {
                    "id": getrandbits(33),
                    "user_id": getrandbits(33),
                    "film_id": getrandbits(33),
                    "timestamp": fake.date_time_between(),
                }
            )
        yield random_batch


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print(f"func:{f.__name__!r} took: {te - ts:2.4f} sec")
        return result

    return wrap
