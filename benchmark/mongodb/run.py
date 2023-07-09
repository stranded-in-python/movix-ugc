from multiprocessing import Process
from pymongo import MongoClient, database

from utils import timing, generate_random_likes, generate_random_bookmarks, generate_random_reviews

class MongoTester:
    def __init__(self, client: MongoClient = MongoClient("localhost", 27017)):
        self.client = client
        self.db = self.client.test_database
        self.batch_size = 1000
        self.rows_number = 10_000_000
        self.collections_to_test = {
            "likes": generate_random_likes, 
            "bookmarks": generate_random_bookmarks, 
            "reviews": generate_random_reviews}
        
    def _after_testing(self):
        self.client.drop_database("test_database")

    def test(self):
        print(f"--Filling with {self.rows_number} docs each collection--")
        self._just_write_rows()
        print("--Done. Test begin--")
        print("--Write--")
        self._check_write()
        print("--Read--")
        self._check_read()
        print("--Read And Write While Write--")
        self.check_read_while_write()
        self._after_testing()

    @timing
    def check_write_likes(self, ):
        collection = self.db.likes
        batch = next(generate_random_likes())
        collection.insert_many(batch)
        print(f"Inserted {self.batch_size} rows")

    @timing
    def check_write_bookmarks(self, ):
        collection = self.db.bookmarks
        batch = next(generate_random_bookmarks())
        collection.insert_many(batch)
        print(f"Inserted {self.batch_size} rows")

    @timing
    def check_write_reviews(self, ):
        collection = self.db.reviews
        batch = next(generate_random_reviews())
        collection.insert_many(batch)
        print(f"Inserted {self.batch_size} rows")

    @timing
    def check_read_likes(self, ):
        collection = self.db.likes
        data = [doc for doc in collection.find(limit=self.batch_size)]
        print(f"Selected {self.batch_size} rows")
        # print(f"Sample Data: {data[0]}")

    @timing
    def check_read_bookmarks(self, ):
        collection = self.db.bookmarks
        data = [doc for doc in collection.find(limit=self.batch_size)]
        print(f"Selected {self.batch_size} rows")
        # print(f"Sample Data: {data[0]}")

    @timing
    def check_read_reviews(self, ):
        collection = self.db.reviews
        data = [doc for doc in collection.find(limit=self.batch_size)]
        print(f"Selected {self.batch_size} rows")
        # print(f"Sample Data: {data[0]}")

    def _just_write_rows(self,):
        client = MongoClient("localhost", 27017)
        db = client.test_database
        for coll, func in self.collections_to_test.items():
            collection = db[coll]
            for batch in func():
                collection.insert_many(batch)

    def _check_read(self,):
        self.check_read_likes()
        self.check_read_bookmarks()
        self.check_read_reviews()


    def _check_write(self,):
        self.check_write_likes()
        self.check_write_bookmarks()
        self.check_write_reviews()

    def _check_read_and_write(self,):
        self._check_read()
        self._check_write()

    @timing
    def check_read_while_write(self):
        noise = Process(target=self._just_write_rows)
        test = Process(target=self._check_read_and_write)
        noise.start()
        test.start()
        noise.join()
        test.join()

if __name__ == "__main__":
    tester = MongoTester()
    tester.test()

# Output

# --Filling with 10000000 docs each collection--
# --Done. Test begin--

# --Write--
# Inserted 1000 rows
# func:'check_write_likes' took: 0.1114 sec
# Inserted 1000 rows
# func:'check_write_bookmarks' took: 0.2343 sec
# Inserted 1000 rows
# func:'check_write_reviews' took: 1.9533 sec

# --Read--
# Selected 1000 rows
# func:'check_read_likes' took: 0.0039 sec
# Selected 1000 rows
# func:'check_read_bookmarks' took: 0.0033 sec
# Selected 1000 rows
# func:'check_read_reviews' took: 0.0149 sec

# --Read And Write While Write--
# Selected 1000 rows
# func:'check_read_likes' took: 0.0130 sec
# Selected 1000 rows
# func:'check_read_bookmarks' took: 0.0030 sec
# Selected 1000 rows
# func:'check_read_reviews' took: 0.0119 sec
# Inserted 1000 rows
# func:'check_write_likes' took: 0.1235 sec
# Inserted 1000 rows
# func:'check_write_bookmarks' took: 0.2437 sec
# Inserted 1000 rows
# func:'check_write_reviews' took: 1.9946 sec
