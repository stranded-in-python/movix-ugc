from multiprocessing import Process

from utils import generate_csv_string, generate_random_data_for_csv, timing
from vertica_python import Connection, connect

connection_info = {
    "host": "vertica",
    "port": "5433",
    "user": "dbadmin",
    "database": "docker",
    "autocommit": True,
}


class NO_DATA(Exception):
    pass


class VerticaTester:
    def __init__(self, connection_info: dict) -> None:
        self.connection_info = connection_info
        self.batch_size = 100_000
        self.rows_number = 10_000_000

    def _before_testing(self):
        with connect(**self.connection_info) as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS regular_table (
                    id INTEGER,
                    user_id INTEGER NOT NULL,
                    film_id  INTEGER NOT NULL,
                    timestamp TIMESTAMP NOT NULL
                );
                """
            )
            # connection.commit()

    def _after_testing(self):
        with connect(**self.connection_info) as connection:
            cursor = connection.cursor()

            cursor.execute(
                """
                DROP TABLE regular_table;
                """
            )
            # connection.commit()

    def test(self):
        self._before_testing()
        print("--Write--")
        with connect(**self.connection_info) as connection:
            self.check_write(connection)
        print("--Read--")
        with connect(**self.connection_info) as connection:
            self.chech_read(connection)
        print("--Read And Write While Write--")
        self.chech_read_while_write()
        self._after_testing()

    @timing
    def check_write(self, connection: Connection):
        cursor = connection.cursor()
        for batch in generate_random_data_for_csv():
            cursor.copy(
                """COPY regular_table(id, user_id, film_id, timestamp)
                FROM stdin DELIMITER ','""",
                generate_csv_string(batch),
            )

    def just_write(self):
        with connect(**self.connection_info) as connection:
            cursor = connection.cursor()
            for batch in generate_random_data_for_csv():
                cursor.copy(
                    """COPY regular_table(id, user_id, film_id, timestamp)
                    FROM stdin DELIMITER ','""",
                    generate_csv_string(batch),
                )

    def _chech_read_while_write(self):
        with connect(**self.connection_info) as connection:
            self.chech_read(connection)
        with connect(**self.connection_info) as connection:
            self.check_write(connection)

    @timing
    def chech_read(self, vertica: Connection):
        cursor = vertica.cursor()
        data = cursor.execute("SELECT * from regular_table").fetchone()
        if data is None:
            raise NO_DATA
        print("Selected %s rows" % self.rows_number)
        print("Sample Data: %s" % [str(col) for col in data])

    @timing
    def chech_read_while_write(self):
        noise = Process(target=self.just_write)
        test = Process(target=self._chech_read_while_write)
        noise.start()
        test.start()
        noise.join()
        test.join()


if __name__ == "__main__":
    tester = VerticaTester(connection_info)
    tester.test()


# 2023-06-28 12:03:39 --Write--
# 2023-06-28 12:11:31 func:'check_write' took: 472.5615 sec
# 2023-06-28 12:11:31 --Read--
# 2023-06-28 12:11:31 Selected 10000000 rows
# 2023-06-28 12:11:31 Sample Data:
# ['1698400264', '6350138181', '2329006959', '1997-01-21 15:24:22']
# 2023-06-28 12:11:31 func:'chech_read' took: 0.3870 sec
# 2023-06-28 12:11:31 --Read And Write While Write--
# 2023-06-28 12:11:32 Selected 10000000 rows
# 2023-06-28 12:11:32 Sample Data:
# ['8497188662', '2435800366', '5013646629', '2015-12-13 04:44:03']
# 2023-06-28 12:11:32 func:'chech_read' took: 0.0625 sec
