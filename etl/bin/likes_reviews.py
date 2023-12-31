import loader
import pendulum
from runner import run

import models
from core import Settings

DATA_FILENAME = 'data_likes_reviews.csv'
WRITE_TABELNAME = 'likes_reviews'
KEY_STATESTORAGE = 'movix:ugc:etl:likes_reviews'
COLLECTION = 'review_likes'
STATE_DEFVALUE = {
    'timestamp': pendulum.parse('2023-07-01T00:0:01.965Z'),
    'limit': 1,
    'skip': 0,
}
MODEL = models.ReviewScore

if __name__ == '__main__':
    run(
        name='likes reviews',
        settings=Settings(),
        loader=loader.Loader,
        model=MODEL,
        data_filename=DATA_FILENAME,
        key_statestorage=KEY_STATESTORAGE,
        state_defvalue=STATE_DEFVALUE,
        collection=COLLECTION,
        write_tabelname=WRITE_TABELNAME,
    )
