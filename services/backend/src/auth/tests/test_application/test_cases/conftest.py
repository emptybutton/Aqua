from datetime import UTC, datetime, timedelta

from pytest import fixture

from auth.domain import entities
from auth.domain import value_objects as vos


@fixture
def user1() -> entities.User:
    return entities.User(
        name=vos.Username(text="username1"),
        password_hash=vos.PasswordHash(text="pAssword1_hash"),
    )


@fixture
def user2() -> entities.User:
    return entities.User(
        name=vos.Username(text="username2"),
        password_hash=vos.PasswordHash(text="pAssword2_hash"),
    )


@fixture
def expired_session(user1: entities.User) -> entities.Session:
    lifetime = vos.SessionLifetime(_start_time=datetime(2000, 1, 1, tzinfo=UTC))

    return entities.Session(user_id=user1.id, lifetime=lifetime)


@fixture
def not_expired_session(user1: entities.User) -> entities.Session:
    lifetime = vos.SessionLifetime(
        _start_time=datetime.now(UTC) - timedelta(days=2)
    )

    return entities.Session(user_id=user1.id, lifetime=lifetime)
