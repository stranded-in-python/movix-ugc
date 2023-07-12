from functools import wraps
from random import getrandbits, randint
from time import time
from uuid import uuid4

from faker import Faker

fake = Faker()

def generate_random_data(rows: int = 10_000_000, batch_size: int = 1000) -> list[dict]:
    for _ in range(int(rows / batch_size)):
        random_batch = []
        for _ in range(batch_size):
            random_batch.append(
                {
                    "id": str(uuid4()),
                    "user_id": str(uuid4()),
                    "film_id": str(uuid4()),
                    "timestamp": fake.date_time_between(),
                }
            )
        yield random_batch

def generate_random_likes(rows: int = 10_000_000, batch_size: int = 10000) -> list[dict]:
    for _ in range(int(rows / batch_size)):
        random_batch = []
        for _ in range(batch_size):
            random_batch.append(
                {
                    "user_id": str(uuid4()), 
                    "movie_id": str(uuid4()), 
                    "score": randint(0, 10)
                }
            )
        yield random_batch

def generate_random_bookmarks(rows: int = 10_000_000, batch_size: int = 10000) -> list[dict]:
    for _ in range(int(rows / batch_size)):
        random_batch = []
        for _ in range(batch_size):
            random_batch.append(
                {"user_id": str(uuid4()), "movie_id": str(uuid4()), "timestamp": fake.date_time_between()}
            )
        yield random_batch

def generate_random_reviews(rows: int = 10_000_000, batch_size: int = 10000) -> list[dict]:
    for _ in range(int(rows / batch_size)):
        random_batch = []
        for _ in range(batch_size):
            random_batch.append(
                {
                    "author": str(uuid4()), 
                    "movie": str(uuid4()), 
                    "text": fake.paragraph(nb_sentences=50), 
                    "timestamp": fake.date_time_between(), 
                    "score": randint(0, 10),  
                    "likes": randint(0, 300), "dislikes": randint(0, 300)}
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
