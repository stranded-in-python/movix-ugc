import multiprocessing
import os
import logging
import sys
import time

import psycopg2
from backoff import on_exception
from loader import Reader
from loader import Writer
from logger import logger


params = {
    "host": "greenplum",
    "port": 5432,
    "dbname": "test",
    "user": "gpadmin",
    # "password": "1",
}
select_sql = "sql/select.sql"
init_sql = "sql/init.sql"
data_file_name1 = "data1.csv"
data_file_name2 = "data2.csv"
read_rows = 10_000_000
read_batch_size = 100_000
write_rows = 10_000_000
write_batch_size = 100_000


@on_exception(exception=psycopg2.OperationalError, logger=logger)
def drop_or_create(ini_sql_file):
    sql = open(ini_sql_file).read()
    conn: psycopg2.connection = psycopg2.connect(**params)
    try:
        with conn:
            with conn.cursor() as curs:
                curs.execute(sql)
                conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
    finally:
        conn.close()


def start_read(sql_file, rows, batch_size, decorate: bool = True):
    sql = open(sql_file).read()
    reader = Reader(
        sql,
        'read',
        params,
        rows=rows,
        batch_size=batch_size,
        decorate=decorate,
    )
    reader.start()


def start_write(data_file_name, rows, batch_size, decorate: bool = True):
    writer = Writer(
        data_file_name,
        'regular_table',
        'write',
        params,
        rows=rows,
        batch_size=batch_size,
        decorate=decorate,
    )
    writer.start()


if __name__ == "__main__":
    drop_or_create(init_sql)
    logger.info("Бд очищена!")

    logger.info(f"Запись в БД без нагрузки [batch={write_batch_size}, rows={write_rows}] ...")
    benchmark_write_process = multiprocessing.Process(
        target=start_write, args=(data_file_name1, write_rows, write_batch_size)
    )
    benchmark_write_process.start()
    benchmark_write_process.join()

    # Дадим время на передышку
    time.sleep(5)

    logger.info(f"Чтение из БД без нагрузки [batch={read_batch_size}, rows={read_rows}] ...")
    benchmark_read_process = multiprocessing.Process(
        target=start_read, args=(select_sql, read_rows, read_batch_size)
    )
    benchmark_read_process.start()
    benchmark_read_process.join()

    logger.info(f"Старт нагрузки [batch={write_batch_size}]!")
    write_process = multiprocessing.Process(
        target=start_write, args=(data_file_name2, sys.maxsize, write_batch_size, False)
    )
    write_process.start()

    logger.info(f"Запись в БД под нагрузкой [batch={write_batch_size}, rows={write_rows}] ...")
    benchmark_write_process = multiprocessing.Process(
        target=start_write, args=(data_file_name1, write_rows, write_batch_size)
    )
    benchmark_write_process.start()
    benchmark_write_process.join()

    logger.info(f"Чтение из БД под нагрузкой [batch={read_batch_size}, rows={read_rows}] ...")
    benchmark_read_process = multiprocessing.Process(
        target=start_read, args=(select_sql, read_rows, read_batch_size)
    )
    benchmark_read_process.start()
    benchmark_read_process.join()

    logger.info("Останавливаем нагрузку...")
    write_process.terminate()

    os.remove(data_file_name1)
    os.remove(data_file_name2)
    logger.info("End")


# 2023-07-10 00:36:43 Бд очищена!
# 2023-07-10 00:36:43 Запись в БД без нагрузки [batch=100000, rows=10000000] ...
# 2023-07-10 00:40:10 Total time for write is 30.00055645898101
# 2023-07-10 00:40:15 Чтение из БД без нагрузки [batch=100000, rows=10000000] ...
# 2023-07-10 00:52:07 Total time for read is 711.9872343900206
# 2023-07-10 00:52:07 Старт нагрузки [batch=100000]!
# 2023-07-10 00:52:07 Запись в БД под нагрузкой [batch=100000, rows=10000000] ...
# 2023-07-10 00:59:37 Total time for write is 262.6463361330825
# 2023-07-10 00:59:37 Чтение из БД под нагрузкой [batch=100000, rows=10000000] ...
# 2023-07-10 01:48:09 Total time for read is 2911.972169139961
# 2023-07-10 01:48:09 Останавливаем нагрузку...
# 2023-07-10 01:48:09 End