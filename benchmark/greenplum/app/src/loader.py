from abc import ABC, abstractmethod
from contextlib import contextmanager

import psycopg2
from logger import logger
from timer import Timer

from utils import generate_random_data


class DatabaseLoader(ABC):
    def __init__(
            self,
            name: str,
            params: dict,
            rows: int = 10_000_000,
            batch_size: int = 100_000,
            decorate: bool = True
    ):
        self.batch_size = batch_size
        self.rows = rows
        self.params = params

        # Декорируем наблюдаемый метод
        self.timer = None
        if decorate:
            self.timer = Timer(name=name, logger=logger.info)
            self._observed = self.timer(self._observed)


    @contextmanager
    def _connection(self):
        """Контекстный менеджер подключения к БД."""
        conn = psycopg2.connect(**self.params)

        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @abstractmethod
    def _exec(self, conn, curs):
        """Основная логика нагрузки."""
        pass

    @abstractmethod
    def _observed(self):
        """Измеряемая нагрузка."""
        pass

    def start(self):
        with self._connection() as conn:
            curs = conn.cursor()
            self._exec(conn, curs)

        if self.timer:
            self.timer.logging_summary()


class Reader(DatabaseLoader):
    """Класс тестирования нагрузки на чтения."""
    def __init__(
        self,
        sql: str,
        name: str,
        params: dict,
        rows: int = 10_000_000,
        batch_size: int = 100_000,
        decorate: bool = True,
    ):
        self.sql = sql
        self.params_sql = {"offset": 0, "limit": batch_size}
        super().__init__(name, params, rows, batch_size, decorate)

    def _observed(self, curs):
        curs.execute(self.sql, self.params_sql)
        curs.fetchall()

    def _exec(self, conn, curs):
        offset = 0
        for _ in range(int(self.rows / self.batch_size)):
            self.params_sql["offset"] = offset
            self._observed(curs)
            offset += self.batch_size


class Writer(DatabaseLoader):
    """Класс тестирования нагрузки на запись."""
    def __init__(
        self,
        file_name: str,
        table_name: str,
        name: str,
        params: dict,
        rows: int = 10_000_000,
        batch_size: int = 100_000,
        decorate: bool = True,
    ):
        self.file_name = file_name
        self.table_name = table_name
        super().__init__(name, params, rows, batch_size, decorate)

    def _to_csv(self, file_name, batch):
        with open(file_name, "w") as f:
            f.write("id,user_id,film_id,timestamp\n")
            lines = [",".join([str(v) for _, v in row.items()]) for row in batch]
            f.writelines("\n".join(lines))

    def _observed(self, conn, curs, copy_statement, file):
        curs.copy_expert(copy_statement, file)
        conn.commit()

    def _exec(self, conn, curs):
        copy_statement = f"COPY public.{self.table_name} FROM STDIN WITH CSV HEADER DELIMITER ',' NULL '\\N'"
        for batch in generate_random_data(rows=self.rows, batch_size=self.batch_size):
            self._to_csv(self.file_name, batch)
            with open(self.file_name) as file:
                self._observed(conn, curs, copy_statement, file)
