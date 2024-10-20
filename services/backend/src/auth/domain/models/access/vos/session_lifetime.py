from dataclasses import dataclass
from datetime import timedelta
from typing import ClassVar

from auth.domain.models.access.vos import time as _time


@dataclass(kw_only=True, frozen=True, slots=True)
class SessionLifetime:
    chunk: ClassVar[timedelta] = timedelta(days=60)

    start_time: _time.Time | None
    end_time: _time.Time

    @classmethod
    def starting_from(cls, start_time: _time.Time) -> "SessionLifetime":
        end_time = start_time.map(lambda time: time + SessionLifetime.chunk)

        return SessionLifetime(
            start_time=start_time,
            end_time=end_time,
        )

    def is_expired_when(self, *, current_time: _time.Time) -> bool:
        if self.start_time is None:
            return not current_time.datetime_ <= self.end_time.datetime_

        start_datetime = self.start_time.datetime_
        end_datetime = self.end_time.datetime_
        current_datetime = current_time.datetime_

        return not start_datetime <= current_datetime <= end_datetime


def extended(
    lifetime: SessionLifetime,
    *,
    current_time: _time.Time,
) -> SessionLifetime:
    extended_end_time = current_time.map(
        lambda time: time + SessionLifetime.chunk
    )

    return SessionLifetime(
        start_time=lifetime.start_time,
        end_time=extended_end_time,
    )
