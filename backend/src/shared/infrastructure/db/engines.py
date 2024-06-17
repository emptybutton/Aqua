from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine

from src.shared.infrastructure.envs import env


db_url = URL.create(
    drivername="postgresql+asyncpg",
    database=env.str("POSTGRES_DATABASE", default="aqua"),
    username=env.str("POSTGRES_USERNAME", default="aqua"),
    password=env.str("POSTGRES_PASSWORD", default="aqua"),
    host=env.str("POSTGRES_HOST", default="localhost"),
    port=env.int("POSTGRES_PORT", default=5432),
)

_echo = env.bool("POSTGRES_ECHO", default=False)
postgres_engine = create_async_engine(db_url, echo=_echo)
