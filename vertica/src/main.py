"""
1. Запустите Vertica на локальной машине.
2. Создайте тестовую таблицу в базе данных.
3. Запишите данные в таблицу.
4. Считайте данные из таблицы и выведите их в стандартный поток вывода.
5. Удалите созданную таблицу по окончании работ.
6. Ответьте на вопрос: примете ли вы решение о покупке коробочного решения
   Vertica для использования в онлайн-кинотеатре? Почему?
"""

import vertica_python


connection_info = {
    "host": "vertica",
    "port": "5433",
    "user": "dbadmin",
    "database": "docker",
}


# Подключились к серверу Vertica с использованием выражения with.
# Контекстный менеджер автоматически закроет соединение после выхода из этого блока кода.
with vertica_python.connect(**connection_info) as connection:
    # Открыли курсор для работы с базой данных.
    cursor = connection.cursor()

    # Выполнили запрос на создание таблицы. Как можно заметить,
    # синтаксис очень похож на обычный SQL.
    cursor.execute(
        """
        CREATE TABLE views (
            id IDENTITY,
            user_id INTEGER NOT NULL,
            movie_id VARCHAR(256) NOT NULL,
            viewed_frame INTEGER NOT NULL
        );
    """
    )

    """`viewed_frame` это временна́я метка, которая показывает,
    какой момент (фрейм) фильма был отсмотрен. """
    cursor = connection.cursor()
    cursor.execute(
        """
        INSERT INTO views (user_id, movie_id, viewed_frame) VALUES (
            500271,
            'tt0120338',
            1611902873
        );
        """
    )

    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT * from views;
        """
    )

    for row in cursor.iterate():
        print(row)

    cursor = connection.cursor()
    cursor.execute(
        """
        DROP TABLE views;
        """
    )
