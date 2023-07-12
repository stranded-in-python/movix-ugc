from multiprocessing import Process
from contextlib import closing

import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import execute_batch

from utils import timing, generate_random_likes, generate_random_bookmarks, generate_random_reviews


dsl = {
    'dbname': "testdb",
    'user': "postgres",
    'password': "postgres",
    "host": "localhost",
    "port": 5434,
}

class PSQLTester:
    def __init__(self, dsl: dict, pg_conn: connection):
        self.dsl = dsl
        self.conn = pg_conn
        self.curs = self.conn.cursor()
        self.batch_size = 1000
        self.rows_number = 10_000_000
        self.tables_to_test = {
            "likes": generate_random_likes, 
            "bookmarks": generate_random_bookmarks, 
            "reviews": generate_random_reviews
        }
        self.tables_inserts = {
            "likes": "INSERT INTO likes (user_id, movie_id, score) VALUES (%(user_id)s, %(movie_id)s, %(score)s)",
            "bookmarks": "INSERT INTO bookmarks (user_id, movie_id, timestamp) VALUES (%(user_id)s, %(movie_id)s, %(timestamp)s)",
            "reviews": "INSERT INTO reviews (author, movie, text, timestamp, score, likes) VALUES (%(author)s, %(movie)s, %(text)s, %(timestamp)s, %(score)s, %(likes)s)"
        }
        
    def _before_testing(self):
        self.curs.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')
        self.curs.execute("""CREATE TABLE IF NOT EXISTS likes (
            id uuid DEFAULT uuid_generate_v4(),
            user_id uuid,
            movie_id uuid,
            score int,
            PRIMARY KEY (id));
            """)
        self.curs.execute("""CREATE TABLE IF NOT EXISTS bookmarks (
            id uuid DEFAULT uuid_generate_v4(),
            user_id uuid,
            movie_id uuid,
            timestamp timestamp,
            PRIMARY KEY (id));
            """)
        self.curs.execute("""CREATE TABLE IF NOT EXISTS reviews(
            id uuid DEFAULT uuid_generate_v4 (),
            author uuid,
            movie uuid,
            text text,
            timestamp timestamp,
            score int,
            likes int,
            dislikes int,
            PRIMARY KEY (id));
            """)
        self.conn.commit()
    
    def _after_testing(self):
        self.curs.execute("DROP TABLE likes; DROP TABLE bookmarks; DROP TABLE reviews;")
        self.conn.commit()

    @timing
    def check_write_likes(self, ):
        batch = next(generate_random_likes())
        execute_batch(self.curs, self.tables_inserts["likes"], batch)
        self.conn.commit()
        print(f"Inserted {self.batch_size} rows")

    @timing
    def check_write_bookmarks(self, ):
        batch = next(generate_random_bookmarks())
        execute_batch(self.curs, self.tables_inserts["bookmarks"], batch)
        self.conn.commit()
        print(f"Inserted {self.batch_size} rows")

    @timing
    def check_write_reviews(self, ):
        batch = next(generate_random_reviews())
        execute_batch(self.curs, self.tables_inserts["reviews"], batch)
        self.conn.commit()
        print(f"Inserted {self.batch_size} rows")

    def _check_write(self):
        self.check_write_likes()
        self.check_write_bookmarks()
        self.check_write_reviews()

    @timing
    def check_read_likes(self):
        self.curs.execute(
            self.curs.mogrify("select * from likes limit %s;" % self.batch_size)
        )
        data = self.curs.fetchmany(self.batch_size)
        print(f"Selected {self.batch_size} rows")
        # print(f"Sample Data: {data[0]}")

    @timing
    def check_read_bookmarks(self):
        self.curs.execute(
            self.curs.mogrify("select * from bookmarks limit %s;" % self.batch_size)
        )
        data = self.curs.fetchmany(self.batch_size)
        print(f"Selected {self.batch_size} rows")
        # print(f"Sample Data: {data[0]}")

    @timing
    def check_read_reviews(self):
        self.curs.execute(
            self.curs.mogrify("select * from reviews limit %s;" % self.batch_size)
        )
        data = self.curs.fetchmany(self.batch_size)
        print(f"Selected {self.batch_size} rows")
        # print(f"Sample Data: {data[0]}")

    def _check_read(self,):
        self.check_read_likes()
        self.check_read_bookmarks()
        self.check_read_reviews()

    def _just_write(self):
        with closing(psycopg2.connect(**dsl)) as pg_conn:
            curs = pg_conn.cursor()
            for table, query in self.tables_inserts.items():
                func = self.tables_to_test[table]
                for batch in func():
                    execute_batch(curs, query, batch)
                    pg_conn.commit()

    def _check_read_and_write(self,):
        self._check_read()
        self._check_write()

    @timing
    def check_read_while_write(self):
        noise = Process(target=self._just_write)
        test = Process(target=self._check_read_and_write)
        noise.start()
        test.start()
        noise.join()
        test.join()

    def test(self):
        print(f"--Filling with {self.rows_number} rows each table--")
        self._just_write()
        print("--Done. Test begin--")   
        print("--Write--")
        self._check_write()   
        print("--Read--")
        self._check_read()
        print("--Read And Write While Write--")
        self.check_read_while_write()
        self._after_testing()

if __name__ == "__main__":
    with closing(psycopg2.connect(**dsl)) as pg_conn:
        psqltester = PSQLTester(dsl, pg_conn)
        psqltester.test()

# Output
# --Filling with 10000000 rows each table--
# --Done. Test begin--
# --Write--
# Inserted 1000 rows
# func:'check_write_likes' took: 4.6993 sec
# Inserted 1000 rows
# func:'check_write_bookmarks' took: 4.9062 sec
# Inserted 1000 rows
# func:'check_write_reviews' took: 4.6401 sec
# --Read--
# Selected 1000 rows
# func:'check_read_likes' took: 0.0504 sec
# Selected 1000 rows
# func:'check_read_bookmarks' took: 0.0102 sec
# Selected 1000 rows
# func:'check_read_reviews' took: 0.0626 sec
# --Read And Write While Write--
# Selected 1000 rows
# func:'check_read_likes' took: 0.0064 sec
# Selected 1000 rows
# func:'check_read_bookmarks' took: 0.0047 sec
# Selected 1000 rows
# func:'check_read_reviews' took: 0.0377 sec
# Inserted 1000 rows
# func:'check_write_likes' took: 2.4458 sec
# Inserted 1000 rows
# func:'check_write_bookmarks' took: 2.9509 sec
# Inserted 1000 rows
# func:'check_write_reviews' took: 3.6189 sec