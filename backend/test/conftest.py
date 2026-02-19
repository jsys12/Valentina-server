# backend/tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from backend.data.database import Base, get_db   # ← подкорректируй путь если нужно
from backend.data.models import User, Valentine  # предполагаем, что модели там


# Используем чистую in-memory БД для тестов
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine
    # engine.dispose() будет вызвано автоматически при завершении


@pytest.fixture(scope="session", autouse=True)
async def create_tables(test_engine):
    """Создаём все таблицы один раз перед всеми тестами"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Опционально: можно дропнуть после, но для in-memory не обязательно


@pytest.fixture(scope="function")
async def db_session(test_engine) -> AsyncSession:
    """Чистая транзакция + сессия на КАЖДЫЙ тест → полная изоляция"""
    connection = await test_engine.connect()
    transaction = await connection.begin()

    session_maker = async_sessionmaker(
        bind=connection,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    session = session_maker()

    yield session

    await session.close()
    await transaction.rollback()
    await connection.close()
