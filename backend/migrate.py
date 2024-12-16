from alembic.config import Config
from alembic import command
from sqlalchemy.ext.asyncio import create_async_engine

from config import DB_USER, DB_PASS, DB_NAME

DATABASE_URL: str = "postgresql+asyncpg://{0}:{1}@bot_db/{2}".format(
    DB_USER,
    DB_PASS,
    DB_NAME,
)


def run_migrations():
    engine = create_async_engine(DATABASE_URL, echo=False)
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.attributes["connection"] = engine
    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    run_migrations()
