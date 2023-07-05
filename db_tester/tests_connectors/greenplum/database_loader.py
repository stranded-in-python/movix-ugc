from abc import ABC, abstractmethod
from contextlib import contextmanager

import psycopg2
from db_tester.utils import generate_random_data
from logger import logger
from timer import Timer


class DatabaseLoader(ABC):
    def __init__(self, params: dict, rows: int = 10_000_000, batch_size: int = 100_000):
        self.batch_size = batch_size
        self.rows = rows
        self.params = params

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
        pass

    def start(self):
        with self._connection() as conn:
            curs = conn.cursor()
            self._exec(conn, curs)


class DatabaseLoaderRead(DatabaseLoader):
    def __init__(
        self, sql, params: dict, rows: int = 10_000_000, batch_size: int = 100_000
    ):
        self.sql = sql
        self.params_sql = {"offset": 0, "limit": batch_size}
        super().__init__(params, rows, batch_size)

    @Timer(name="read", logger=logger.info)
    def _select(self, curs):
        curs.execute(self.sql, self.params_sql)
        result = curs.fetchall()
        # logger.info(f"Count read rows: {len(result)}")

    def _exec(self, conn, curs):
        offset = 0
        for _ in range(int(self.rows / self.batch_size)):
            self.params_sql["offset"] = offset
            self._select(curs)
            offset += self.batch_size


class DatabaseLoaderWrite(DatabaseLoader):
    def __init__(
        self,
        file_name,
        table_name,
        params: dict,
        rows: int = 10_000_000,
        batch_size: int = 100_000,
    ):
        self.file_name = file_name
        self.table_name = table_name
        super().__init__(params, rows, batch_size)

    def _gen_csv(self, file_name, batch):
        with open(file_name, "w") as f:
            f.write("id,user_id,filem_id,timestamp\n")
            lines = [",".join([str(v) for _, v in row.items()]) for row in batch]
            f.writelines("\n".join(lines))

    @Timer(name="write", logger=logger.info)
    def _insert(self, conn, curs, copy_statement, file):
        curs.copy_expert(copy_statement, file)
        conn.commit()

    def _exec(self, conn, curs):
        copy_statement = f"COPY public.{self.table_name} FROM STDIN WITH CSV HEADER DELIMITER ',' NULL '\\N'"
        for batch in generate_random_data(rows=self.rows, batch_size=self.batch_size):
            self._gen_csv(self.file_name, batch)
            with open(self.file_name) as file:
                self._insert(conn, curs, copy_statement, file)
