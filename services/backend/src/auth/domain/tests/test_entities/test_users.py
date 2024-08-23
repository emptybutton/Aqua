from uuid import UUID

from pytest import raises

from auth.domain import entities, value_objects as vos


def test_equality() -> None:
    user_id = UUID(int=0)
    name = vos.Username(text="username")
    password_hash = vos.PasswordHash(text="password_hash")

    user1 = entities.User(id=user_id, name=name, password_hash=password_hash)
    user2 = entities.User(id=user_id, name=name, password_hash=password_hash)

    assert user1 == user2


def test_successful_authorization() -> None:
    user_id = UUID(int=0)
    name = vos.Username(text="username")
    password_hash = vos.PasswordHash(text="password_hash")
    user = entities.User(id=user_id, name=name, password_hash=password_hash)

    user.authorize(password_hash=password_hash)


def test_authorization_with_invalid_password_hash() -> None:
    user_id = UUID(int=0)
    name = vos.Username(text="username")
    password_hash = vos.PasswordHash(text="password_hash")
    invalid_password_hash = vos.PasswordHash(text="invalid_password_hash")
    user = entities.User(id=user_id, name=name, password_hash=password_hash)

    with raises(entities.User.IncorrectPasswordHashForAuthorizationError):
        user.authorize(password_hash=invalid_password_hash)

