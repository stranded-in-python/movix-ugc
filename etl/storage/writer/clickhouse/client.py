from contextlib import contextmanager
from typing import Generator, Union

import clickhouse_connect
from clickhouse_connect.driver import Client
from clickhouse_connect.driver.exceptions import ClickHouseError
from clickhouse_connect.driver.tools import insert_file
from storage.writer import BaseWriter
from utils import logger, on_exception

from models import Like


class ClickhouseWriter(BaseWriter):
    """Управление процессом ETL из Kafka в Clickhouse."""

    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password,
        db: str,
        table: str,
        model: Union[type[Like], None],
    ):
        self._column_names = tuple(model.__fields__.keys())
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._db = db
        self._table = table
        self.client = None

    def _set_client_db(self):
        """Иницализация клиента clickhouse."""
        self.client = clickhouse_connect.get_client(
            host=self._host,
            port=self._port,
            database=self._db,
            username=self._username,
            password=self._password,
        )

    @contextmanager
    def _get_client_db(self) -> Generator[Client, None, None]:
        """Обработка правильного завершения клиента clickhouse."""
        self._set_client_db()
        try:
            yield self.client
        finally:
            self.client.close()

    @on_exception(exception=ClickHouseError, logger=logger)
    def save(self, data_filepath: str):
        """Сохраняем сообщения в clickhouse."""
        with self._get_client_db():
            insert_file(
                self.client,
                self._table,
                data_filepath,
                column_names=self._column_names,
                database=self._db,
            )
