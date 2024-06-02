from sqlalchemy import URL, create_engine
from typenv import Env


_env = Env()

db_url = URL.create(
    drivername="postgresql+asyncpg",
    database=_env.str("POSTGRES_DATABASE", default="aqua"),
    username=_env.str("POSTGRES_USERNAME", default="aqua"),
    password=_env.str("POSTGRES_PASSWORD", default="aqua"),
    host=_env.str("POSTGRES_HOST", default="localhost"),
    port=_env.int("POSTGRES_PORT", default=5432),
)

engine = create_engine(db_url, echo=_env.bool("POSTGRES_ECHO", default=False))
