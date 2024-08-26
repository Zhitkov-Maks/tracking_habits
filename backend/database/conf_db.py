from config import DB_USER, DB_PASS, DB_NAME



"""We describe the connection to the database."""
from typing import AsyncGenerator


from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

DATABASE_URL: str = "postgresql+asyncpg://{0}:{1}@localhost:5432/{2}".format(
    DB_USER,
    DB_PASS,
    DB_NAME,
)

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Function to get a session."""
    async with async_session_maker() as session:
        yield session
