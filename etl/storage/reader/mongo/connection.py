from typing import Any, Mapping
from urllib.parse import quote_plus as quote

from pymongo.database import Database
from pymongo.mongo_client import MongoClient


class MongoConnect:
    def __init__(
        self,
        host: str,
        port: str,
        user: str,
        pw: str,
        rs: str,
        auth_db: str,
        main_db: str,
        cert_path: str | None,
    ) -> None:
        self.user = user
        self.pw = pw
        self.host = host
        self.port = (port,)
        self.replica_set = rs
        self.auth_db = auth_db
        self.main_db = main_db
        self.cert_path = cert_path

    def url(self) -> str:
        return 'mongodb://{user}:{pw}@{hosts}:{port}/?replicaSet={rs}&authSource={auth_src}'.format(
            user=quote(self.user),
            pw=quote(self.pw),
            hosts=self.host,
            port=self.port,
            rs=self.replica_set,
            auth_src=self.auth_db,
        )

    def client(self) -> Database[Mapping[str, Any] | Any]:
        return MongoClient(self.url(), tlsCAFile=self.cert_path)[self.main_db]
