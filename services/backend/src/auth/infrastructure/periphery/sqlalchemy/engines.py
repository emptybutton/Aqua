from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from auth.infrastructure.periphery import envs


db_url = URL.create(
    drivername="postgresql+asyncpg",
    database=envs.postgres_database,
    username=envs.postgres_username,
    password=envs.postgres_password,
    host=envs.postgres_host,
    port=envs.postgres_port,
)

if envs.is_dev:
    postgres_engine = create_async_engine(
        db_url, echo=envs.postgres_echo, poolclass=NullPool
    )
else:
    postgres_engine = create_async_engine(db_url, echo=envs.postgres_echo)
