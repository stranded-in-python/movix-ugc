import json

import pendulum
import storage
from storage.mongo import Reader
from utils import MyEncoder

from core import Settings


class LikesLoader:
    def __init__(
        self,
        settings: Settings,
        offset_storage: storage.BaseStorage,
        model,
        reader,
        writer,
    ):
        """Инициализация стартовых параметров."""
        self._settings = settings
        # Объект, для доступа к сохранению и извлечению из хранилища состояния процесса ETL.
        self.offset_storage = offset_storage
        self._model = model
        self._reader = reader
        self._writer = writer
        self._table = settings.ch_tablelikes
        self._insert_sql

    def load(self):
        query_dest = open(self.dest_query_path, encoding='utf-8').read()

        pg_conn = self._get_pg_conn(self.dest_con_id)

        mongo_conn = self._get_mongo_conn()
        mongo_reader = Reader(mc=mongo_conn, collection=self.collection)

        try:
            while True:
                wf_setting = self.wf_storage.retrieve_state()
                last_loaded = pendulum.parse(
                    wf_setting.workflow_settings[self.LAST_LOADED_KEY]
                )

                # проблема:
                # Если у нас n документов по одной какой-то дате.
                # Если в Mongo при filter по дате и limit
                # больше чем limit документов, т.е. n > limit.
                # То мы n - limit документов упустим.
                # Поэтому нужен еще один цикл, для перебора всех документов по одной дате при n > len(limit & filter).
                # Или по другому говоря потому, что за один цикл мы можеи не получить все документы.
                # Решаем её еще одни циклом.
                checked_infinity = True
                skip = 0
                limit = self.BATCH_LIMIT
                while True:

                    load_queue = mongo_reader.get(
                        load_threshold=last_loaded, limit=limit, skip=skip
                    )

                    for d in load_queue:
                        obj = {
                            'object_id': str(d['_id']),
                            'update_ts': d['update_ts'],
                            'object_value': json.dumps(
                                d, cls=MyEncoder, sort_keys=True, ensure_ascii=False
                            ),
                        }
                        self._insert_dest(pg_conn, query_dest, self.model(**obj))

                    if len(load_queue) > 0:
                        self.log.info(f"Found {len(load_queue)} models to load.")
                        checked_infinity = False
                    else:
                        break

                    skip += limit

                    pg_conn.commit()

                    # Сохраняем прогресс.
                    wf_setting.workflow_settings[self.LAST_LOADED_KEY] = max(
                        d["update_ts"] for d in load_queue
                    )
                    self.wf_storage.save_state(wf_setting)
                    self.log.info(
                        f"Load finished on {wf_setting.workflow_settings[self.LAST_LOADED_KEY]}"
                    )

                if checked_infinity:
                    break
        except Exception as e:
            pg_conn.rollback()
            raise e
        finally:
            pg_conn.close()

        self.log.info("Quitting.")


if __name__ == '__main__':
    pass
    # settings = Settings()
    # loader = Loader(
    #     settings=settings,
    #     offset_storage=storage.RedisStorage(
    #         settings.redis_key_prefix, settings.redis_host, settings.redis_port
    #     ),
    #     reader= Reader(
    #         MongoConnect(
    #             host=settings.mongo_host,
    #             port=settings.mongo_port,
    #             user=settings.mongo_user,
    #             pw=settings.mongo_password,
    #             rs=settings.mongo_rs,
    #             auth_db=settings.mongo_authdb,
    #             main_db=settings.mongo_db,
    #             cert_path=settings.mongo_certpath
    #         ),
    #         collection=settings.collections['likes']
    #     ),
    #     writer
    #
    # )
    # loader.run()
