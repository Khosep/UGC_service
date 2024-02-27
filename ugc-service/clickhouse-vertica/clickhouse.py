from clickhouse_driver import Client
import time
import csv

client = Client(host="localhost")

# Создание таблицы в ClickHouse
client.execute("CREATE DATABASE IF NOT EXISTS test_db")
client.execute("USE test_db")
client.execute(
    "CREATE TABLE IF NOT EXISTS test_table (id UUID, name String, age String) ENGINE = MergeTree ORDER BY id"
)

# Измерение скорости вставки
start_time = time.time()
with open("data.csv", "r") as file:
    csv_reader = csv.DictReader(file)
    data = list(csv_reader)
    client.execute("INSERT INTO test_db.test_table VALUES", data)
insert_time = time.time() - start_time

# Измерение скорости чтения
start_time = time.time()
result = client.execute("SELECT COUNT(*) FROM test_db.test_table")
select_time = time.time() - start_time

# Вывод результатов
print(f"ClickHouse Insert Time: {insert_time:.2f} seconds")
print(f"ClickHouse Select Time: {select_time:.2f} seconds")
