from typing import Any, Mapping
from urllib.parse import quote_plus as quote

from pymongo.database import Database
from pymongo.mongo_client import MongoClient


class MongoConnect:
    def __init__(
        self,
        host: str,
        port: str,
        user: str | None,
        pw: str | None,
        rs: str | None,
        auth_db: str,
        main_db: str,
        cert_path: str | None,
    ) -> None:
        self.user = user
        self.pw = pw
        self.host = host
        self.port = port
        self.replica_set = rs
        self.auth_db = auth_db
        self.main_db = main_db
        self.cert_path = cert_path

    def url(self) -> str:
        res = 'mongodb://'
        if self.user and self.pw:
            res += f'{quote(self.user)}:{quote(self.pw)}@'
        res += '{hosts}:{port}/?authSource={auth_src}'.format(
            hosts=self.host, port=self.port, auth_src=self.auth_db
        )
        if self.replica_set:
            res += f'&replicaSet={self.replica_set}'
        return res

    def client(self) -> Database[Mapping[str, Any] | Any]:
        return MongoClient(self.url(), tlsCAFile=self.cert_path)[self.main_db]
