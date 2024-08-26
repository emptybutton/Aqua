from datetime import UTC, datetime
from uuid import UUID, uuid4

from pytest import raises

from auth.domain import entities
from auth.domain import value_objects as vos


def test_user_id_on_creation() -> None:
    user_id = UUID(int=0)
    start_time = datetime(2000, 1, 1, tzinfo=UTC)
    lifetime = vos.SessionLifetime(_start_time=start_time)

    session = entities.Session(user_id=user_id, lifetime=lifetime)

    assert session.user_id == user_id


def test_failed_authentication_with_expired_lifetime() -> None:
    start_time = datetime(2000, 1, 1, tzinfo=UTC)
    lifetime = vos.SessionLifetime(_start_time=start_time)
    session = entities.Session(user_id=uuid4(), lifetime=lifetime)

    with raises(entities.Session.ExpiredLifetimeForAuthenticationError):
        session.authenticate()


def test_failed_authentication_with_ray_lifetime() -> None:
    start_time = datetime(2000, 1, 1, tzinfo=UTC)
    lifetime = vos.SessionLifetime(_end_time=start_time)
    session = entities.Session(user_id=uuid4(), lifetime=lifetime)

    with raises(entities.Session.ExpiredLifetimeForAuthenticationError):
        session.authenticate()


def test_lifetime_on_authentication_with_time_point() -> None:
    start_time = datetime(2000, 1, 1, tzinfo=UTC)
    lifetime = vos.SessionLifetime(_start_time=start_time)
    time_point = datetime(2000, 2, 15, tzinfo=UTC)
    expected_lifetime = vos.SessionLifetime(
        _start_time=datetime(2000, 1, 1, tzinfo=UTC),
        _end_time=datetime(2000, 4, 15, tzinfo=UTC),
    )
    session = entities.Session(user_id=uuid4(), lifetime=lifetime)

    session.authenticate(time_point=time_point)

    assert session.lifetime == expected_lifetime


def test_lifetime_on_authentication_with_timepoint_with_ray_lifetime() -> None:
    time_point = datetime(2000, 1, 5, tzinfo=UTC)
    lifetime = vos.SessionLifetime(_end_time=datetime(2025, 2, 5, tzinfo=UTC))
    expected_lifetime = vos.SessionLifetime(
        _end_time=datetime(2000, 3, 5, tzinfo=UTC)
    )
    session = entities.Session(user_id=uuid4(), lifetime=lifetime)

    session.authenticate(time_point=time_point)

    assert session.lifetime == expected_lifetime


def test_user_id_on_creation_for_user() -> None:
    start_time = datetime(2000, 1, 1, tzinfo=UTC)
    user_id = uuid4()
    username = vos.Username(text="username")
    password_hash = vos.PasswordHash(text="password_hash")
    user = entities.User(id=user_id, name=username, password_hash=password_hash)

    session = entities.Session.for_(user, start_time=start_time)

    assert session.user_id == user_id


def test_lifetime_on_creation_for_user() -> None:
    start_time = datetime(2000, 1, 1, tzinfo=UTC)
    user_id = uuid4()
    username = vos.Username(text="username")
    password_hash = vos.PasswordHash(text="password_hash")
    user = entities.User(id=user_id, name=username, password_hash=password_hash)
    expected_lifetime = vos.SessionLifetime(
        _start_time=start_time, _end_time=datetime(2000, 3, 1, tzinfo=UTC)
    )

    session = entities.Session.for_(user, start_time=start_time)

    assert session.lifetime == expected_lifetime
