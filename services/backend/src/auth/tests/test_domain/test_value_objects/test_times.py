from datetime import UTC, datetime

from pytest import raises

from auth.domain import value_objects as vos


def test_quality() -> None:
    datetime_ = datetime.now(UTC)
    time1 = vos.Time(datetime_=datetime_)
    time2 = vos.Time(datetime_=datetime_)

    assert time1 == time2


def test_creation_with_not_utc_datetime() -> None:
    with raises(vos.Time.NotUTCError):
        vos.Time(datetime_=datetime.now())
