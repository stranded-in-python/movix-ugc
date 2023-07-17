# import storage
#
# from core import Settings

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
