# Исследование по выбору хранилища

# Адрес репозитория:
https://github.com/Izrekatel/ugc_sprint_1

# Авторы проекта:
- Гельруд Борис (https://github.com/Izrekatel/)
- Косянов Никита (https://github.com/4madeuz/)
- Холкин Сергей (https://github.com/Khosep/)

## Описание проекта:
"В исследовании реализован процесс загрузки 10 мил строк в хранилища Clickhouse и Vertica.
Произведена оценка времени записи/чтения в хранилище. Результаты приложены в лог. файлах.
Контейнеры с хранилищами разворачиваются из docker-compose-research.yml.
Скрипты расположены в файлах clickhouse.py и vertica.py соотвественно.
Итоговые значения на локальном ПК с 10 потоками по 1 млн записей, с вставками по 1000 записей:
Запись:
    - clickhouse 427 сек.
    - vertica 558 сек.
Чтение:
    - clickhouse 0,074 сек
    - vertica 0,865 сек.

При таких исходных данных выбор в пользу хранилища clickhouse.

## Стек:
- Python
- Fastapi
- Git
- Docker
- Poetry
- Pre-commit
- vertica
- clickhouse
