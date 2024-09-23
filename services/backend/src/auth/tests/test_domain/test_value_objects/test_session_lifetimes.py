from datetime import UTC, datetime

from dirty_equals import IsNow
from pytest import raises

from auth.domain import value_objects as vos


def test_creation_without_points() -> None:
    with raises(vos.SessionLifetime.NoPointsError):
        vos.SessionLifetime()


def test_end_time_on_creation_without_start_time() -> None:
    end_time = vos.Time(datetime_=datetime.now(UTC))
    lifetime = vos.SessionLifetime(_end_time=end_time)

    assert lifetime.end_time.datetime_ == IsNow(tz=UTC)


def test_start_time_on_creation_without_start_time() -> None:
    end_time = vos.Time(datetime_=datetime.now(UTC))
    lifetime = vos.SessionLifetime(_end_time=end_time)

    assert lifetime.start_time is None


def test_end_time_on_creation_without_end_time() -> None:
    start_time = vos.Time(datetime_=datetime(2000, 1, 1, tzinfo=UTC))
    lifetime = vos.SessionLifetime(start_time=start_time)
    expected_end_time = vos.Time(datetime_=datetime(2000, 3, 1, tzinfo=UTC))

    assert lifetime.end_time == expected_end_time


def test_start_time_on_creation_without_end_time() -> None:
    start_time = vos.Time(datetime_=datetime(2000, 1, 1, tzinfo=UTC))
    lifetime = vos.SessionLifetime(start_time=start_time)
    expected_end_time = vos.Time(datetime_=datetime(2000, 3, 1, tzinfo=UTC))

    assert lifetime.end_time == expected_end_time


def test_expired() -> None:
    current_time = vos.Time(datetime_=datetime.now(UTC))
    start_time = vos.Time(datetime_=datetime(2000, 1, 1, tzinfo=UTC))
    lifetime = vos.SessionLifetime(start_time=start_time)

    assert lifetime.expired(current_time=current_time)


def test_expired_with_active_current_time() -> None:
    current_time = vos.Time(datetime_=datetime(1991, 1, 1, tzinfo=UTC))
    start_time = vos.Time(datetime_=datetime(2000, 1, 1, tzinfo=UTC))
    lifetime = vos.SessionLifetime(start_time=start_time)

    assert lifetime.expired(current_time=current_time)


def test_expired_with_active_current_time_without_start_point() -> None:
    current_time = vos.Time(datetime_=datetime(1991, 1, 1, tzinfo=UTC))
    end_time = vos.Time(datetime_=datetime(2000, 3, 1, tzinfo=UTC))
    lifetime = vos.SessionLifetime(_end_time=end_time)

    assert not lifetime.expired(current_time=current_time)


def test_extend() -> None:
    current_time = vos.Time(datetime_=datetime(2000, 5, 5, tzinfo=UTC))
    lifetime = vos.SessionLifetime(
        start_time=vos.Time(datetime_=datetime(2000, 1, 1, tzinfo=UTC)),
        _end_time=vos.Time(datetime_=datetime(2000, 3, 1, tzinfo=UTC)),
    )
    expected_extended_lifetime = vos.SessionLifetime(
        start_time=vos.Time(datetime_=datetime(2000, 1, 1, tzinfo=UTC)),
        _end_time=vos.Time(datetime_=datetime(2000, 7, 4, tzinfo=UTC)),
    )

    extended_lifetime = lifetime.extend(current_time=current_time)

    assert extended_lifetime == expected_extended_lifetime


def test_extend_with_ray_lifetime() -> None:
    current_time = vos.Time(datetime_=datetime(2025, 7, 10, tzinfo=UTC))
    lifetime = vos.SessionLifetime(
        _end_time=vos.Time(datetime_=datetime(2000, 1, 1, tzinfo=UTC)),
    )
    expected_extended_lifetime = vos.SessionLifetime(
        _end_time=vos.Time(datetime_=datetime(2025, 9, 8, tzinfo=UTC)),
    )

    extended_lifetime = lifetime.extend(current_time=current_time)

    assert extended_lifetime == expected_extended_lifetime
