import io
from random import getrandbits
from functools import wraps
from time import time
from typing import Any, AsyncGenerator, Generator
from faker import Faker
import csv


fake = Faker()


async def generate_random_data_async(
    rows: int = 10_000, batch_size: int = 1000
) -> AsyncGenerator[list[dict], None]:
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


def generate_random_data(
    rows: int = 10_000, batch_size: int = 1000
) -> Generator[list[dict[str, Any]], None, None]:
    for _ in range(int(rows/batch_size)):
        random_batch = []
        for _ in range(batch_size):
            random_batch.append(
                {
                    "id": getrandbits(33),
                    "user_id": getrandbits(33),
                    "film_id": getrandbits(33),
                    "timestamp": fake.date_time_between()
                }
            )
        yield random_batch

def generate_random_data_for_csv(
    rows: int = 10_000_000, batch_size: int = 100_000
) -> Generator[list[tuple[Any, ...]], None, None]:
    columns = ("id", "user_id", "film_id", "timestamp")
    for _ in range(int(rows / batch_size)):
        random_batch: list[tuple[Any, ...]] = [columns]

        for _ in range(batch_size):
            random_batch.append(
                (
                    getrandbits(33),
                    getrandbits(33),
                    getrandbits(33),
                    fake.date_time_between(),
                )
            )
        yield random_batch

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print("func:%r took: %2.4f sec" % (f.__name__, te - ts))
        return result

    return wrap


def generate_csv_string(data):
    csv_string = io.StringIO()
    writer = csv.writer(csv_string, delimiter=',')
    writer.writerows(data)
    csv_string.seek(0)
    return csv_string
