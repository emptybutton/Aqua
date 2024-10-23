from dataclasses import dataclass
from datetime import UTC, datetime

from result import Err, Ok, Result

from shared.domain.framework.safe import SafeImmutable


@dataclass(kw_only=True, frozen=True, slots=True)
class NotUTCTimeError: ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Time(SafeImmutable):
    datetime_: datetime

    @classmethod
    def with_(cls, *, datetime_: datetime) -> Result["Time", NotUTCTimeError]:
        time = Time(datetime_=datetime_, is_safe=True)

        if time.datetime_.tzinfo is not UTC:
            return Err(NotUTCTimeError())

        return Ok(time)
