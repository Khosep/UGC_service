import random
import time
import uuid
from datetime import datetime, timezone
from threading import Thread, Lock

from clickhouse_driver import Client

lock = Lock()

NUM_THREADS = 10  # Количество потоков
BUTCH_SIZE = 1000  # Количество строк для одномоментной вставки
THREAD_SIZE = 1000000  # общее количество строк в потоке


def create_client():
    return Client(host="localhost")


def create_table(client):
    client.execute(
        """CREATE TABLE IF NOT EXISTS views (
            id UUID,
            user_id UUID,
            film_id UUID,
            film_timestamp_sec UInt64,
            event_time DateTime
        ) ENGINE = MergeTree() ORDER BY id;"""
    )
    client.execute("TRUNCATE TABLE views;")


def output_rows(client):
    rows = client.execute(
        "SELECT * FROM views WHERE film_timestamp_sec < 1000;"
    )
    for row in rows:
        print(row)


def generate_random_data(butch_size: int):
    data_to_insert = []
    for _ in range(butch_size):
        user_id = str(uuid.uuid4())
        film_id = str(uuid.uuid4())
        timestamp_sec = random.randint(1, 9999999999)
        event_time = datetime.now(timezone.utc)
        data = (str(uuid.uuid4()), user_id, film_id, timestamp_sec, event_time)
        data_to_insert.append(data)
    return data_to_insert


def insert_data(i, client, data_to_insert, size):
    client.execute(
        """INSERT INTO views (id, user_id, film_id, film_timestamp_sec,
        event_time) VALUES""",
        data_to_insert,
    )
    print(f"Thread {i} - Inserted {size} rows\n")


def insert_bulk_data(i, butch_size, tread_size):
    start_time = time.time()
    print(f"Thread {i} - Insertion started\n")
    try:
        print(f"Thread {i} - Generated data for insertion\n")
        client = create_client()
        while tread_size >= butch_size:
            tread_size -= butch_size
            data_to_insert = generate_random_data(butch_size)
            insert_data(i, client, data_to_insert, butch_size)
        if tread_size > 0:
            data_to_insert = generate_random_data(tread_size)
            insert_data(i, client, data_to_insert, tread_size)
    except Exception as e:
        print(f"Thread {i} - Error occurred: {str(e)}\n")
        with open("error_clickhouse.log", "a") as file:
            file.write(f"Thread {i} - Error occurred: {str(e)}\n")
            file.write(f"Data Thread {i} {data_to_insert}\n")
    finally:
        end_time = time.time()
        print(f"Thread {i} - Completed in {end_time - start_time} seconds\n")


if __name__ == "__main__":
    threads = []
    create_table(create_client())
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
    print(f"Total input time {end_input_time - start_input_time} seconds\n")

    with open("clickhouse.log", "a") as file:
        file.write(
            f"Result ClickHouse with {NUM_THREADS} threads with tread size "
            f"{THREAD_SIZE} insert by {BUTCH_SIZE} rows\n"
        )
        file.write(f"Total input size: {NUM_THREADS * THREAD_SIZE} rows.\n")
        file.write(
            f"Input started at {datetime.fromtimestamp(start_input_time)}\n"
        )
        file.write(
            f"Input finished at {datetime.fromtimestamp(end_input_time)}\n"
        )
        file.write(
            f"Total time taken for input: {end_input_time - start_input_time} "
            f"seconds\n"
        )

    start_read_time = time.time()
    output_rows(create_client())
    end_read_time = time.time()
    print(f"Total read time {end_read_time - start_read_time} seconds\n")

    with open("clickhouse.log", "a") as file:
        file.write(
            f"Read started at {datetime.fromtimestamp(start_read_time)}\n"
        )
        file.write(
            f"Read finished at {datetime.fromtimestamp(end_read_time)}\n"
        )
        file.write(
            f"Total read time {end_read_time - start_read_time} seconds\n"
        )
