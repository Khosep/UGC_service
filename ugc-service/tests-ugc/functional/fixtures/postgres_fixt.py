import pytest
import asyncpg
from asyncpg import Connection
from functional.settings import test_settings


@pytest.fixture(scope="session")
async def db_conn() -> Connection:
    conn = await asyncpg.connect(test_settings.postgres_dsn)
    yield conn
    await conn.close()


@pytest.fixture(autouse=True)
async def recreate_bd(db_conn: Connection):
    """Фикстура для отчистки таблиц в БД, чтобы тесты с нуля начинать."""
    await db_conn.execute("TRUNCATE public.user_film_review CASCADE;")


@pytest.fixture
async def db_fetchone(db_conn: Connection):
    async def inner(sql):
        result = await db_conn.fetchrow(sql)
        return result

    return inner


@pytest.fixture
async def db_fetch(db_conn: Connection):
    async def inner(sql):
        result = await db_conn.fetch(sql)
        return result

    return inner
