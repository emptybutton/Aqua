from dataclasses import dataclass
from datetime import timedelta
from functools import cached_property
from typing import ClassVar, cast

from auth.domain.models.access.pure.vos import time as _time


@dataclass(kw_only=True, frozen=True, slots=True, eq=False)
class SessionLifetime:
    chunk: ClassVar[timedelta] = timedelta(days=60)

    class Error(Exception): ...

    class NoPointsError(Error): ...

    start_time: _time.Time | None = None
    _end_time: _time.Time | None = None

    @cached_property
    def end_time(self) -> _time.Time:
        if self._end_time is not None:
            return self._end_time

        return cast(_time.Time, self.start_time).of(
            lambda time: time + SessionLifetime.chunk
        )

    def is_expired_when(self, *, current_time: _time.Time) -> bool:
        if self.start_time is None:
            return not current_time.datetime_ <= self.end_time.datetime_

        start_datetime = self.start_time.datetime_
        end_datetime = self.end_time.datetime_
        current_datetime = current_time.datetime_

        return not start_datetime <= current_datetime <= end_datetime

    def __post_init__(self) -> None:
        if self.start_time is None and self._end_time is None:
            raise SessionLifetime.NoPointsError

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SessionLifetime):
            return False

        is_start_time_correct = self.start_time == other.start_time
        is_end_time_correct = self.end_time == other.end_time

        return is_start_time_correct and is_end_time_correct

    def __hash__(self) -> int:
        return hash(self.start_time) + hash(self.end_time)


def extended(
    lifetime: SessionLifetime,
    *,
    current_time: _time.Time,
) -> SessionLifetime:
    extended_end_time = current_time.of(
        lambda time: time + SessionLifetime.chunk
    )

    return SessionLifetime(
        start_time=lifetime.start_time, _end_time=extended_end_time
    )
