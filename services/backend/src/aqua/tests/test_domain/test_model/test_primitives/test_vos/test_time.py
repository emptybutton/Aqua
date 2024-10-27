from datetime import UTC, datetime

from result import Err

from aqua.domain.model.primitives.vos.time import (
    NotUTCTimeError,
    Time,
)


def test_not_utc_time() -> None:
    result = Time.with_(datetime_=datetime(2006, 1, 1))

    assert result == Err(NotUTCTimeError())


def test_utc_time() -> None:
    Time.with_(datetime_=datetime(2006, 1, 1, tzinfo=UTC)).unwrap()
