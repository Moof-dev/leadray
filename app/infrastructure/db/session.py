from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings


engine = create_async_engine(
    settings.db_url,
    echo=False,        # Включаем логирование SQL-запросов (полезно при разработке)
    future=True,      # Используем синтаксис SQLAlchemy 2.0
    pool_size=10,     # Максимум 10 активных соединений
    max_overflow=20   # Дополнительные соединения при нагрузке
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db_session():
    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()