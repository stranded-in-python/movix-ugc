from datetime import datetime

import pymongo
import utils
from bson.codec_options import CodecOptions
from storage.reader import BaseReader

from .connection import MongoConnect


class MongoReader(BaseReader):
    def __init__(self, mc: MongoConnect, collection: str) -> None:
        self.dbs = mc.client()
        self.collection = collection

    @utils.backoff.on_exception(
        exception=pymongo.errors.ConnectionFailure,
        start_sleep_time=1,
        factor=2,
        border_sleep_time=15,
        max_retries=15,
        logger=utils.logger,
    )
    def get(
        self, field_threshold: str, load_threshold: datetime, limit: int, skip: int
    ) -> list[dict]:
        # Формируем фильтр: больше чем дата последней загрузки
        filter = {field_threshold: {'$gte': load_threshold}}

        # Формируем сортировку по update_ts. Сортировка обязательна при инкрементальной загрузке.
        sort = [(field_threshold, 1), ('_id', 1)]

        options = CodecOptions(tz_aware=True, uuid_representation=4)
        # Вычитываем документы из MongoDB с применением фильтра и сортировки.
        docs = list(
            self.dbs.get_collection(self.collection, codec_options=options).find(
                filter=filter, sort=sort, limit=limit, skip=skip
            )
        )
        return docs
