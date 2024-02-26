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


def generate_random_data():
    user_id = str(uuid.uuid4())
    film_id = str(uuid.uuid4())
    timestamp_sec = random.randint(1, 9999999999)
    roles = random.choice(["admin", "user", "moderator", "guest"])
    email = f"user_{random.randint(1, 1000000)}@example.com"
    username = f"user_{random.randint(1, 1000000)}"
    first_name = f"First_{random.randint(1, 1000000)}"
    last_name = f"Last_{random.randint(1, 1000000)}"
    event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return [
        user_id,
        film_id,
        timestamp_sec,
        roles,
        email,
        username,
        first_name,
        last_name,
        event_time,
    ]


def insert_bulk_data(i, cursor, num_rows):
    start_time = time.time()
    print(f"Thread {i} - Insertion started\n")
    data_to_insert = []
    try:
        for _ in range(num_rows):
            data = generate_random_data()
            data_to_insert.append(data)
        print(f"Thread {i} - Generated data for insertion\n")
        cursor.executemany(
            """INSERT INTO views (user_id, film_id, film_timestamp_sec, roles,
            email, username, first_name, last_name, event_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            data_to_insert,
            use_prepared_statements=False,
        )
        print(f"Thread {i} - Inserted {num_rows} rows\n")
    except Exception as e:
        print(f"Thread {i} - Error occurred: {str(e)}\n")
    finally:
        end_time = time.time()
        print(f"Thread {i} - Completed in {end_time - start_time} seconds\n")


if __name__ == "__main__":
    num_threads = 10  # Количество потоков
    num_rows_per_thread = 100  # Количество строк данных для каждого потока
    threads = []

    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS views (
                id IDENTITY(1, 1),
                user_id UUID NOT NULL,
                film_id UUID NOT NULL,
                film_timestamp_sec INTEGER NOT NULL,
                roles VARCHAR(255),
                email VARCHAR(255) NOT NULL,
                username VARCHAR(255) NULL,
                first_name VARCHAR(255) NULL,
                last_name VARCHAR(255) NULL,
                event_time TIMESTAMP WITH TIME ZONE NULL
            );"""
        )
        cursor.execute("DELETE FROM views;")
        start_input_time = time.time()
        print("Start input\n")
        for i in range(num_threads):
            lock.acquire()
            thread = Thread(
                target=insert_bulk_data, args=(i, cursor, num_rows_per_thread)
            )
            thread.start()
            lock.release()
            threads.append(thread)
        for thread in threads:
            thread.join()
        end_input_time = time.time()
        print(
            f"Total input time {end_input_time - start_input_time} seconds\n"
        )
        with open("operations.log", "a") as file:
            file.write(
                f"Result vertica with {num_threads} threads by {num_rows_per_thread} rows\n"
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
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
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
