from .base import BaseLoader
from .csv_mixin import CSVMixin


class LikesLoader(BaseLoader, CSVMixin):
    def load(self):
        state = self._state_storage.retrieve()
        last_loaded = state['timestamp']

        load_queue = self._reader.get(
            field_threshold='timestamp',
            load_threshold=last_loaded,
            limit=state['limit'],
            skip=state['skip'],
        )

        models = []
        for doc in load_queue:
            model = self._get_validated({k: str(v) for k, v in doc.items()})
            if model:
                models.append(model)

        if models:
            self._to_csv(models)
            self._writer.save(self._data_filename)

            self._logger.info(f"Found {len(models)} models to load.")

            state['skip'] += state['limit']
            state['timestamp'] = last_loaded
            self._state_storage.save(state)


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
