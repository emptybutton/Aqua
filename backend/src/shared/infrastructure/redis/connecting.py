from enum import Enum

from redis.asyncio.connection import ConnectionPool, ConnectKwargs

from src.shared.infrastructure.envs import env


default_connection_data = ConnectKwargs(
    username=env.str("REDIS_USERNAME", default="aqua"),
    password=env.str("REDIS_PASSWORD", default="aqua"),
    host=env.str("REDIS_HOST", default="localhost"),
    port=env.int("REDIS_PORT", default=6379),
)


class Pool(Enum):
    users = ConnectionPool(**default_connection_data, db=0)
    records = ConnectionPool(**default_connection_data, db=1)
