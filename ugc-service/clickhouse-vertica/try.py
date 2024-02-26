import random
import time
import uuid
from datetime import datetime
from threading import Lock

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


if __name__ == "__main__":
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
