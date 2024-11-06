from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Callable, Literal

from result import Err, Ok, Result

from auth.domain.framework.safe import SafeImmutable


@dataclass(kw_only=True, frozen=True, slots=True)
class Time(SafeImmutable):
    datetime_: datetime

    @classmethod
    def with_(
        cls, *, datetime_: datetime
    ) -> Result["Time", Literal["not_utc_time"]]:
        time = Time(datetime_=datetime_, is_safe=True)

        if time.datetime_.tzinfo is not UTC:
            return Err("not_utc_time")

        return Ok(time)

    def map(self, mapped: Callable[[datetime], datetime]) -> "Time":
        return Time(datetime_=mapped(self.datetime_), is_safe=True)
