from typing import TypeVar, Optional
import enum

import typenv


_env = typenv.Env()
_env.read_env(".env")


class Env(enum.Enum):
    jwt_secret = _env.str("JWT_SECRET")

    postgres_database = _env.str("POSTGRES_DATABASE")
    postgres_username = _env.str("POSTGRES_USERNAME")
    postgres_password = _env.str("POSTGRES_PASSWORD")
    postgres_host = _env.str("POSTGRES_HOST", default=None)
    postgres_port = _env.int("POSTGRES_PORT", default=None)
    postgres_echo = _env.bool("POSTGRES_ECHO", default=None)


_V = TypeVar("_V")
_D = TypeVar("_D")


def or_(value: Optional[_V], default_value: _D) -> _V | _D:
    return default_value if value is None else value


def existing(value: Optional[_V]) -> _V:
    assert value is not None
    return value
