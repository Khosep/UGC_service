import random
import time
import uuid
from datetime import datetime
from threading import Thread, Lock

import vertica_python

lock = Lock()

NUM_THREADS = 20  # Количество потоков
BUTCH_SIZE = 500  # Количество строк для одномоментной вставки
THREAD_SIZE = 500000  # общее количество строк в потоке

connection_info = {
    "host": "127.0.0.1",
    "port": 5433,
    "user": "dbadmin",
    "password": "",
    "database": "docker",
    "autocommit": True,
    "use_prepared_statements": False,
}


def create_connection():
    return vertica_python.connect(**connection_info)


def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS views (
            id IDENTITY(1, 1),
            user_id UUID NOT NULL,
            film_id UUID NOT NULL,
            film_timestamp_sec INTEGER NOT NULL,
            event_time TIMESTAMP WITH TIME ZONE NULL
        );"""
    )
    cursor.execute("DELETE FROM views;")


def output_rows(connection):
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM views WHERE film_timestamp_sec < 1000;""")
    for row in cursor.iterate():
        print(row)


def generate_random_data(butch_size: int):
    data_to_insert = []
    for _ in range(butch_size):
        user_id = str(uuid.uuid4())
        film_id = str(uuid.uuid4())
        film_timestamp_sec = random.randint(1, 9999999999)
        event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = [
            user_id,
            film_id,
            film_timestamp_sec,
            event_time,
        ]
        data_to_insert.append(data)
    return data_to_insert


def insert_data(i, connection, data_to_insert, size):
    cursor = connection.cursor()
    cursor.executemany(
        """INSERT INTO views (user_id, film_id, film_timestamp_sec, event_time)
        VALUES (%s, %s, %s, %s);""",
        data_to_insert,
    )
    print(f"Thread {i} - Inserted {size} rows\n")


def insert_bulk_data(i, butch_size, tread_size):
    start_time = time.time()
    print(f"Thread {i} - Insertion started\n")
    try:
        print(f"Thread {i} - Generated data for insertion\n")
        with create_connection() as connection:
            create_table(connection)  # Создание таблицы для каждого соединения
            cursor = connection.cursor()
            while tread_size >= butch_size:
                tread_size -= butch_size
                data_to_insert = generate_random_data(butch_size)
                cursor.executemany(
                    """INSERT INTO views (user_id, film_id, film_timestamp_sec, event_time)
                    VALUES (%s, %s, %s, %s);""",
                    data_to_insert,
                )
                print(f"Thread {i} - Inserted {butch_size} rows\n")
            if tread_size > 0:
                data_to_insert = generate_random_data(tread_size)
                cursor.executemany(
                    """INSERT INTO views (user_id, film_id, film_timestamp_sec, event_time)
                    VALUES (%s, %s, %s, %s);""",
                    data_to_insert,
                )
                print(f"Thread {i} - Inserted {tread_size} rows\n")
    except Exception as e:
        print(f"Thread {i} - Error occurred: {str(e)}\n")
        with open("error_vertica.log", "a") as file:
            file.write(f"Thread {i} - Error occurred: {str(e)}\n")
            file.write(f"Data Thread {i} {data_to_insert}\n")
    finally:
        end_time = time.time()
        print(f"Thread {i} - Completed in {end_time - start_time} seconds\n")


if __name__ == "__main__":
    threads = []
    with vertica_python.connect(**connection_info) as connection:
        create_table(connection)
        start_input_time = time.time()
        print("Start input\n")
        for i in range(NUM_THREADS):
            thread = Thread(
                target=insert_bulk_data,
                args=(i, BUTCH_SIZE, THREAD_SIZE),
            )
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        end_input_time = time.time()
        print(f"Total input row {THREAD_SIZE}.\n")
        print(
            f"Total input time {end_input_time - start_input_time} seconds\n"
        )
        with open("vertica.log", "a") as file:
            file.write(
                f"Result vertica with {NUM_THREADS} threads with tread size {THREAD_SIZE} insert by {BUTCH_SIZE} rows\n"
            )
            file.write(f"Total input size: {NUM_THREADS*THREAD_SIZE} rows.\n")
            file.write(
                f"Input started at {datetime.fromtimestamp(start_input_time)}\n"
            )
            file.write(
                f"Input finished at {datetime.fromtimestamp(end_input_time)}\n"
            )
            file.write(
                f"Total time taken for input: {end_input_time - start_input_time} seconds\n"
            )
        start_read_time = time.time()
        output_rows(connection)
        end_read_time = time.time()
        print(f"Total read time {end_read_time - start_read_time} seconds\n")
        with open("vertica.log", "a") as file:
            file.write(
                f"Read started at {datetime.fromtimestamp(start_read_time)}\n"
            )
            file.write(
                f"Read finished at {datetime.fromtimestamp(end_read_time)}\n"
            )
            file.write(
                f"Total read time {end_read_time - start_read_time} seconds\n"
            )
