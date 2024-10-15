from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Callable


@dataclass(kw_only=True, frozen=True, slots=True)
class Time:
    class Error(Exception): ...

    class NotUTCError(Error): ...

    datetime_: datetime

    def of(self, mapped: Callable[[datetime], datetime]) -> "Time":
        return Time(datetime_=mapped(self.datetime_))

    def __post_init__(self) -> None:
        if self.datetime_.tzinfo is not UTC:
            raise Time.NotUTCError
