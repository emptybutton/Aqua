from sqlalchemy import URL, create_engine

from src.shared.infrastructure.envs import env


db_url = URL.create(
    drivername="postgresql+asyncpg",
    database=env.str("POSTGRES_DATABASE", default="aqua"),
    username=env.str("POSTGRES_USERNAME", default="aqua"),
    password=env.str("POSTGRES_PASSWORD", default="aqua"),
    host=env.str("POSTGRES_HOST", default="localhost"),
    port=env.int("POSTGRES_PORT", default=5432),
)

engine = create_engine(db_url, echo=env.bool("POSTGRES_ECHO", default=False))
