import random
import time
import uuid
from datetime import datetime
from threading import Thread, Lock

import vertica_python

lock = Lock()

connection_info = {
    "host": "127.0.0.1",
    "port": 5433,
    "user": "dbadmin",
    "password": "",
    "database": "docker",
    "autocommit": True,
    "use_prepared_statements": False,
}


def generate_random_data(butch_size: int):
    data_to_insert = []
    for _ in range(butch_size):
        user_id = str(uuid.uuid4())
        film_id = str(uuid.uuid4())
        timestamp_sec = random.randint(1, 9999999999)
        event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = [
            user_id,
            film_id,
            timestamp_sec,
            event_time,
        ]
        data_to_insert.append(data)
    return data_to_insert


def insert_bulk_data(i, connection, butch_size):
    cursor = connection.cursor()
    start_time = time.time()
    print(f"Thread {i} - Insertion started\n")
    try:
        data_to_insert = generate_random_data(butch_size)
        print(f"Thread {i} - Generated data for insertion\n")
        cursor.executemany(
            """INSERT INTO views (user_id, film_id, film_timestamp_sec, event_time)
            VALUES (%s, %s, %s, %s);""",
            data_to_insert,
            use_prepared_statements=False,
        )
        print(f"Thread {i} - Inserted {butch_size} rows\n")
    except Exception as e:
        print(f"Thread {i} - Error occurred: {str(e)}\n")
        print(f"Data Thread {i} {data_to_insert}\n")

    finally:
        end_time = time.time()
        print(f"Thread {i} - Completed in {end_time - start_time} seconds\n")


if __name__ == "__main__":
    num_threads = 10  # Количество потоков
    butch_size = 100  # Количество строк данных для каждого потока
    threads = []

    with vertica_python.connect(**connection_info) as connection:
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
        start_input_time = time.time()
        print("Start input\n")
        for i in range(num_threads):
            thread = Thread(
                target=insert_bulk_data, args=(i, connection, butch_size)
            )
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        end_input_time = time.time()
        print(
            f"Total input time {end_input_time - start_input_time} seconds\n"
        )
        with open("operations.log", "a") as file:
            file.write(
                f"Result vertica with {num_threads} threads by {butch_size} rows\n"
            )
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
        cursor.execute("""SELECT * FROM views;""")
        for row in cursor.iterate():
            print(row)
        end_read_time = time.time()
        print(f"Total read time {end_read_time - start_read_time} seconds\n")
        with open("operations.log", "a") as file:
            file.write(
                f"Read started at {datetime.fromtimestamp(start_read_time)}\n"
            )
            file.write(
                f"Read finished at {datetime.fromtimestamp(end_read_time)}\n"
            )
            file.write(
                f"Total read time {end_read_time - start_read_time} seconds\n"
            )
