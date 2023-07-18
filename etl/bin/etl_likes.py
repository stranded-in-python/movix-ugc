import loader
import pendulum
import storage
from utils import logger

import models
from core import Settings

if __name__ == '__main__':
    settings = Settings()
    loader = loader.LikesLoader(
        model=models.Like,
        data_filename='data_likes.csv',
        settings=settings,
        state_storage=storage.state.RedisState(
            key='movix:ugc:etl:likes',
            def_value={
                'timestamp': pendulum.parse('2023-07-01T00:0:01.965Z'),
                'limit': 1,
                'skip': 0,
            },
            host=settings.redis_host,
            port=settings.redis_port,
        ),
        reader=storage.reader.MongoReader(
            storage.reader.MongoConnect(
                host=settings.mongo_host,
                port=settings.mongo_port,
                user=settings.mongo_user,
                pw=settings.mongo_password,
                rs=settings.mongo_rs,
                auth_db=settings.mongo_authdb,
                main_db=settings.mongo_db,
                cert_path=settings.mongo_certpath,
            ),
            collection='likes',
        ),
        writer=storage.writer.ClickhouseWriter(
            host=settings.ch_host,
            port=settings.ch_port,
            username=settings.ch_username,
            password=settings.ch_password,
            db=settings.ch_db,
            table='likes_movies',
            model=models.Like,
        ),
        logger=logger,
    )
    while True:
        loader.load()
