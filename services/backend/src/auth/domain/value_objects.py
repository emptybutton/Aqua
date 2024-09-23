from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from functools import cached_property
from string import digits
from typing import Callable, ClassVar, cast


@dataclass(kw_only=True, frozen=True)
class Time:
    class Error(Exception): ...

    class NotUTCError(Error): ...

    datetime_: datetime

    def of(self, mapped: Callable[[datetime], datetime]) -> "Time":
        return Time(datetime_=mapped(self.datetime_))

    def __post_init__(self) -> None:
        if self.datetime_.tzinfo is not UTC:
            raise Time.NotUTCError


@dataclass(kw_only=True, frozen=True)
class Username:
    class Error(Exception): ...

    class EmptyError(Error): ...

    text: str

    def __post_init__(self) -> None:
        if len(self.text) == 0:
            raise Username.EmptyError


@dataclass(kw_only=True, frozen=True)
class Password:
    class Error(Exception): ...

    class WeekError(Error): ...

    class TooShortError(WeekError): ...

    class OnlySmallLettersError(WeekError): ...

    class OnlyCapitalLettersError(WeekError): ...

    class OnlyDigitsError(WeekError): ...

    class NoDigitsError(WeekError): ...

    text: str

    def __post_init__(self) -> None:
        if len(self.text) < 8:
            raise Password.TooShortError

        if self.__has_no_digits():
            raise Password.NoDigitsError

        if self.__has_only_digits():
            raise Password.OnlyDigitsError

        if self.text.upper() == self.text:
            raise Password.OnlyCapitalLettersError

        if self.text.lower() == self.text:
            raise Password.OnlySmallLettersError

    def __has_no_digits(self) -> bool:
        return set(digits) - set(self.text) == set(digits)

    def __has_only_digits(self) -> bool:
        return set(self.text) - set(digits) == set()


@dataclass(kw_only=True, frozen=True)
class PasswordHash:
    class Error(Exception): ...

    class EmptyError(Error): ...

    text: str

    def __post_init__(self) -> None:
        if len(self.text) == 0:
            raise PasswordHash.EmptyError


@dataclass(kw_only=True, frozen=True, eq=False)
class SessionLifetime:
    __chunk: ClassVar[timedelta] = timedelta(days=60)

    class Error(Exception): ...

    class NoPointsError(Error): ...

    start_time: Time | None = None
    _end_time: Time | None = None

    @cached_property
    def end_time(self) -> Time:
        if self._end_time is not None:
            return self._end_time

        return cast(Time, self.start_time).of(
            lambda time: time + SessionLifetime.__chunk
        )

    def expired(self, *, current_time: Time) -> bool:
        if self.start_time is None:
            return not current_time.datetime_ <= self.end_time.datetime_

        start_datetime = self.start_time.datetime_
        end_datetime = self.end_time.datetime_
        current_datetime = current_time.datetime_

        return not start_datetime <= current_datetime <= end_datetime

    def extend(self, *, current_time: Time) -> "SessionLifetime":
        extended_end_time = current_time.of(
            lambda time: time + SessionLifetime.__chunk
        )

        return SessionLifetime(
            start_time=self.start_time, _end_time=extended_end_time
        )

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
