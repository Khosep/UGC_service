# Сервис UGC
# Сервис контента генерируемого пользователем в онлайн-кинотеатре

# Адрес репозитория:
https://github.com/Izrekatel/Auth_sprint_2

# Авторы проекта:
- Гельруд Борис (https://github.com/Izrekatel/)
- Косянов Никита (https://github.com/4madeuz/)
- Холкин Сергей (https://github.com/Khosep/)

## Описание проекта:
"Сервис UGC (User Generated Content)" позволяет сохранять для дальнейшей
 обработки пользовательские данные. Для этого на Factapi реализован эндпоинт,
 при обращении на который происходит сохранение данных в брокер сообщиний на
 базе кластера Kaffka, после чего компонент ETL извлекает данные из Kaffka и
 пачками сохраняет их в хранилище на базе кластера Clickhouse. Дополнительно к
 сервису написаны тесты на базе Pytest.

## Стек:
- Python
- Fastapi
- Git
- Docker
- Poetry
- Pre-commit
- Pydantic
- Uvicorn
- Pytest
- aiohttp
- nginx
- swagger
- kaffka
- clickhouse

### 1. Запуск основного проекта в контейнерах Docker

#### 1. Создать .env файл из env.example (в корневой папке)

#### 2. Запустить Docker

#### 3. Поднимаем сеть контейнеров:
```bash
docker-compose -f docker-compose-ugc.yml up -d
```
#### 4. Просмотр основного проекта

```
Документация сервиса доступна по адресу:
http://localhost:60/ugc/openapi

Также можно ее скачать в виде json:
http://localhost:60/ugc/openapi.json

```
#### 5. Результат:
```
После прохождения тестов результат можно посмотреть к логах контейнера тестов.
```

### 2. Установка для локальной разработки

1. Установите Poetry

Для Linux, macOS, Windows (WSL):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Для Windows (Powershell):
```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```
Чтобы скрипты выполнялись, PowerShell может попросить у вас поменять политики.

В macOS и Windows сценарий установки предложит добавить папку с исполняемым файлом poetry в переменную PATH. Сделайте это, выполнив следующую команду:

macOS (не забудьте поменять borisgelrud на имя вашего пользователя)
```bash
export PATH="/Users/borisgelrud/.local/bin:$PATH"
```

Windows
```bash
$Env:Path += ";C:\Users\borisgelrud\AppData\Roaming\Python\Scripts"; setx PATH "$Env:Path"
```

Для проверки установки выполните следующую команду:
```bash
poetry --version
```
Опционально! Изменить местонахождение окружения в папке проекта
```bash
poetry config virtualenvs.in-project true
```

Установка автодополнений bash (опцонально)
```bash
poetry completions bash >> ~/.bash_completion
```

Создание виртуально окружения
```bash
poetry env use python3.11
```

2. Установите виртуальное окружение
Важно: poetry ставится и запускается для каждого сервиса отдельно.

Перейти в одну из папок сервиса, например:
```bash
cd tests
```

Установка зависимостей (для разработки)
```bash
poetry install
```

Запуск оболочки и активация виртуального окружения

```bash
your@device:~/your_project_pwd/your_service$ poetry shell
```

Проверка активации виртуального окружения
```bash
poetry env list
```


* Полная документация: https://python-poetry.org/docs/#installation
* Настройка для pycharm: https://www.jetbrains.com/help/pycharm/poetry.html


3. Установка pre-commit

Модуль pre-commit уже добавлен в lock, таким образом после настройки виртуального окружения, должен установится автоматически.
Проверить установку pre-commit можно командой (при активированном виртуальном окружении):
```bash
pre-commit --version
```

Если pre-commit не найден, то его нужно установить по документации https://pre-commit.com/#install

```bash
poetry add pre-commit
```

4. Установка hook

Установка осуществляется hook командой
```bash
pre-commit install --all
```

В дальнейшем при выполнении команды `git commit` будут выполняться проверки перечисленные в файле `.pre-commit-config.yaml`.
