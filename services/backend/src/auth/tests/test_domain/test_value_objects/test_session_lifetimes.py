from datetime import datetime, UTC

from dirty_equals import IsNow
from pytest import raises

from auth.domain import value_objects as vos


def test_creation_without_points() -> None:
    with raises(vos.SessionLifetime.NoPointsError):
        vos.SessionLifetime()


def test_end_time_on_creation_without_start_time() -> None:
    lifetime = vos.SessionLifetime(_end_time=datetime.now(UTC))

    assert lifetime.end_time == IsNow(tz=UTC)


def test_start_time_on_creation_without_start_time() -> None:
    lifetime = vos.SessionLifetime(_end_time=datetime.now(UTC))

    assert lifetime.start_time is None


def test_end_time_on_creation_without_end_time() -> None:
    start_time = datetime(2000, 1, 1, tzinfo=UTC)
    lifetime = vos.SessionLifetime(_start_time=start_time)

    assert lifetime.end_time == datetime(2000, 3, 1, tzinfo=UTC)


def test_start_time_on_creation_without_end_time() -> None:
    start_time = datetime(2000, 1, 1, tzinfo=UTC)
    lifetime = vos.SessionLifetime(_start_time=start_time)

    assert lifetime.end_time == datetime(2000, 3, 1, tzinfo=UTC)


def test_creation_with_not_utc_end_time() -> None:
    with raises(vos.SessionLifetime.NotUTCEndTimeError):
        vos.SessionLifetime(_end_time=datetime(2000, 1, 1))


def test_creation_with_not_utc_start_time() -> None:
    with raises(vos.SessionLifetime.NotUTCStartTimeError):
        vos.SessionLifetime(_start_time=datetime(2000, 1, 1))


def test_expired() -> None:
    start_time = datetime(2000, 1, 1, tzinfo=UTC)
    lifetime = vos.SessionLifetime(_start_time=start_time)

    assert lifetime.expired()


def test_expired_with_active_time_point() -> None:
    start_time = datetime(2000, 1, 1, tzinfo=UTC)
    lifetime = vos.SessionLifetime(_start_time=start_time)

    assert not lifetime.expired(time_point=datetime(2000, 3, 1, tzinfo=UTC))


def test_expired_with_active_time_point_without_start_point() -> None:
    lifetime = vos.SessionLifetime(_end_time=datetime(2000, 3, 1, tzinfo=UTC))

    assert not lifetime.expired(time_point=datetime(1991, 1, 1, tzinfo=UTC))


def test_extend() -> None:
    time_point = datetime(2000, 5, 5, tzinfo=UTC)
    lifetime = vos.SessionLifetime(
        _start_time=datetime(2000, 1, 1, tzinfo=UTC),
        _end_time=datetime(2000, 3, 1, tzinfo=UTC),
    )
    expected_extended_lifetime = vos.SessionLifetime(
        _start_time=datetime(2000, 1, 1, tzinfo=UTC),
        _end_time=datetime(2000, 7, 4, tzinfo=UTC),
    )

    extended_lifetime = lifetime.extend(time_point=time_point)

    assert extended_lifetime == expected_extended_lifetime


def test_extend_with_ray_lifetime() -> None:
    time_point = datetime(2025, 7, 10, tzinfo=UTC)
    lifetime = vos.SessionLifetime(
        _end_time=datetime(2000, 1, 1, tzinfo=UTC),
    )
    expected_extended_lifetime = vos.SessionLifetime(
        _end_time=datetime(2025, 9, 8, tzinfo=UTC),
    )

    extended_lifetime = lifetime.extend(time_point=time_point)

    assert extended_lifetime == expected_extended_lifetime
