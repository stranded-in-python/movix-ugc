from multiprocessing import Process

from clickhouse_driver import Client

from .utils import generate_random_data, timing


class ClickHouseTester:
    def __init__(self, clickhouse: Client = Client(host="localhost")):
        self.ch = clickhouse
        self.ch2 = Client(host="localhost")
        self.batch_size = 1000
        self.rows_number = 10_000_000

    def _before_testing(self):
        self.ch.execute(
            "CREATE DATABASE IF NOT EXISTS test_db ON CLUSTER company_cluster"
        )
        self.ch.execute(
            """
        CREATE TABLE IF NOT EXISTS test_db.regular_table ON CLUSTER company_cluster
        (id Int64, user_id Int64, film_id Int64, timestamp DateTime64)
        Engine=MergeTree() ORDER BY id
        """
        )
        self.just_write(self.ch)

    def _after_testing(self):
        self.ch.execute("DROP DATABASE IF EXISTS test_db ON CLUSTER company_cluster")

    def test(self):
        self._before_testing()
        print(f"--Created database, table, inserted {self.rows_number} rows--")
        print("--Write--")
        self.check_write(self.ch)
        print("--Read--")
        self.check_read(self.ch2)
        print("--Read And Write While Write--")
        self.check_read_while_write()
        self._after_testing()

    @timing
    def check_write(self, ch: Client):
        print(f"Inserted {self.batch_size} rows")
        batch = next(generate_random_data())
        ch.execute(
            (
                "INSERT INTO test_db.regular_table "
                "(id, user_id, film_id, timestamp) VALUES"
            ),
            batch,
        )

    def just_write(self, ch: Client):
        for batch in generate_random_data():
            ch.execute(
                (
                    "INSERT INTO test_db.regular_table "
                    "(id, user_id, film_id, timestamp) VALUES"
                ),
                batch,
            )

    def _check_read_while_write(self):
        self.check_read(self.ch)
        self.check_write(self.ch)

    @timing
    def check_read(self, ch: Client):
        data = ch.execute(
            f"SELECT * from test_db.regular_table LIMIT 0,{self.batch_size}"
        )[0]
        print(f"Selected {self.batch_size} rows")
        print(f"Sample Data: {[str(col) for col in data]}")

    @timing
    def check_read_while_write(self):
        noise = Process(target=self.just_write, args=(self.ch2,))
        test = Process(target=self._check_read_while_write)
        noise.start()
        test.start()
        noise.join()
        test.join()


if __name__ == "__main__":
    tester = ClickHouseTester()
    tester.test()

# Output
# --Created database, table, inserted 10000000 rows--
# --Write--
# func:'check_write' took: 0.0220 sec
# --Read--
# Selected 1000 rows
# Sample Data: ['1509', '218846485', '6402693977', '2007-03-26 21:33:32']
# func:'check_read' took: 0.0809 sec
# --Read And Write While Write--
# Selected 1000 rows
# Sample Data: ['1509', '218846485', '6402693977', '2007-03-26 21:33:32']
# func:'check_read' took: 0.0135 sec
# func:'check_write' took: 0.0205 sec
# func:'check_read_while_write' took: 207.7469 sec
