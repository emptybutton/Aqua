from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine

from shared.infrastructure.envs import Env


db_url = URL.create(
    drivername="postgresql+asyncpg",
    database=Env.postgres_database,
    username=Env.postgres_username,
    password=Env.postgres_password,
    host=Env.postgres_host,
    port=Env.postgres_port,
)

postgres_engine = create_async_engine(db_url, echo=Env.postgres_echo)
