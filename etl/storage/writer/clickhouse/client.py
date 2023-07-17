from contextlib import contextmanager
from typing import Generator, Union

import clickhouse_connect
from clickhouse_connect.driver import Client
from clickhouse_connect.driver.exceptions import ClickHouseError
from clickhouse_connect.driver.tools import insert_file
from utils import logger, on_exception
from writer import BaseWriter

from core import Settings
from models import Like


class ClickhouseWriter(BaseWriter):
    """Управление процессом ETL из Kafka в Clickhouse."""

    def __init__(self, settings: Settings, model: Union[type[Like], None]):
        self._settings = settings
        self._column_names = tuple(model.__fields__.keys())
        self._table = settings.ch_table

    @on_exception(exception=ClickHouseError, logger=logger)
    def _set_client_db(self):
        """Иницализация клиента clickhouse."""
        self.client = clickhouse_connect.get_client(
            host=self._settings.ch_host,
            port=self._settings.ch_port,
            database=self._settings.ch_db,
            username=self._settings.ch_username,
            password=self._settings.ch_password,
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
        insert_file(
            self.client,
            self._table,
            data_filepath,
            column_names=self._column_names,
            database=self._settings.ch_db,
        )
