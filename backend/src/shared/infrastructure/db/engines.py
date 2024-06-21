from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine

from src.shared.infrastructure.envs import Env, or_


db_url = URL.create(
    drivername="postgresql+asyncpg",
    database=Env.postgres_database.value,
    username=Env.postgres_username.value,
    password=Env.postgres_password.value,
    host=or_(Env.postgres_host.value, "localhost"),
    port=or_(Env.postgres_port.value, 5432),
)

_echo = or_(Env.postgres_echo.value, False)
postgres_engine = create_async_engine(db_url, echo=_echo)
