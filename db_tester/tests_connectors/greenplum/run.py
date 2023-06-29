import multiprocessing
import os

import psycopg2

from database_loader import DatabaseLoaderRead
from database_loader import DatabaseLoaderWrite
from logger import logger


params = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'test',
    'user': 'gpadmin',
    'password': '1'
}
select_sql = 'sql/agg.sql'
init_sql = 'sql/init.sql'
data_file_name = 'data.csv'
read_rows=10_000_000
read_batch_size=100_000
write_rows=10_000_000
write_batch_size=100_000


def drop_or_create(ini_sql_file):
    sql = open(ini_sql_file).read()
    try:
        with psycopg2.connect(**params) as conn:
            curs = conn.cursor()
            curs.execute(sql)
            conn.commit()
    except psycopg2.DatabaseError:
        conn.rollback()
    finally:
        conn.close()


def start_read(select_file, rows, batch_size):
    sql = open(select_file).read()
    reader = DatabaseLoaderRead(
        params=params,
        rows=rows,
        batch_size=batch_size,
        sql=sql,
    )
    reader.start()


def start_write(data_file_name, rows, batch_size):
    writer = DatabaseLoaderWrite(
        file_name=data_file_name,
        table_name='regular_table',
        params=params,
        rows=rows,
        batch_size=batch_size,
    )
    writer.start()


if __name__ == '__main__':
    drop_or_create(init_sql)
    logger.info('Бд очищена!')

    logger.info('Первичное наполнение БД!')
    start_write(data_file_name,write_rows,write_batch_size)

    # Создание процесса для функции start_write
    write_process = multiprocessing.Process(target=start_write, args=(data_file_name,write_rows,write_batch_size,))

    # Создание процесса для функции start_read
    read_process = multiprocessing.Process(target=start_read, args=(select_sql,read_rows,read_batch_size,))

    logger.info('Старт основных замеров!')

    # Запуск процессов
    write_process.start()
    read_process.start()

    # Ожидание завершения процессов
    write_process.join()
    read_process.join()
    os.remove(data_file_name)
