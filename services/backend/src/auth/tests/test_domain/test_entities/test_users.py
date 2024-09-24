from datetime import UTC, datetime
from uuid import UUID

from pytest import raises

from auth.domain import entities
from auth.domain import value_objects as vos


def test_equality() -> None:
    user_id = UUID(int=0)
    name = vos.Username(text="username")
    password_hash = vos.PasswordHash(text="password_hash")

    user1 = entities.User(id=user_id, name=name, password_hash=password_hash)
    user2 = entities.User(id=user_id, name=name, password_hash=password_hash)

    assert user1 == user2


def test_successful_authorization() -> None:
    current_time = vos.Time(datetime_=datetime.now(UTC))
    user_id = UUID(int=0)
    name = vos.Username(text="username")
    password_hash = vos.PasswordHash(text="password_hash")
    user = entities.User(id=user_id, name=name, password_hash=password_hash)

    user.authorize(password_hash=password_hash, current_time=current_time)


def test_authorization_with_invalid_password_hash() -> None:
    current_time = vos.Time(datetime_=datetime.now(UTC))
    user_id = UUID(int=0)
    name = vos.Username(text="username")
    password_hash = vos.PasswordHash(text="password_hash")
    invalid_password_hash = vos.PasswordHash(text="invalid_password_hash")
    user = entities.User(id=user_id, name=name, password_hash=password_hash)

    with raises(entities.User.IncorrectPasswordHashForAuthorizationError):
        user.authorize(
            password_hash=invalid_password_hash, current_time=current_time
        )


def test_user_on_register() -> None:
    current_time = vos.Time(datetime_=datetime.now(UTC))
    username = vos.Username(text="username")
    password_hash = vos.PasswordHash(text="password_hash")

    result = entities.User.register(
        username, password_hash, current_time=current_time
    )

    assert result.user.name == username
    assert result.user.password_hash == password_hash


def test_session_on_register() -> None:
    current_time = vos.Time(datetime_=datetime(2000, 1, 1, tzinfo=UTC))
    end_time = vos.Time(datetime_=datetime(2000, 3, 1, tzinfo=UTC))
    username = vos.Username(text="username")
    password_hash = vos.PasswordHash(text="password_hash")
    lifetime = vos.SessionLifetime(start_time=current_time, _end_time=end_time)

    result = entities.User.register(
        username, password_hash, current_time=current_time
    )

    assert result.current_session.user_id == result.user.id
    assert result.current_session.lifetime == lifetime
