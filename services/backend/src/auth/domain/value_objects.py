from dataclasses import dataclass
from datetime import datetime, UTC, timedelta
from functools import cached_property
from string import digits
from typing import ClassVar


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

    class NotUTCStartTimeError(Error): ...

    class NotUTCEndTimeError(Error): ...

    _start_time: datetime | None = None
    _end_time: datetime | None = None

    @cached_property
    def start_time(self) -> datetime | None:
        return self._start_time

    @cached_property
    def end_time(self) -> datetime:
        if self._end_time is not None:
            return self._end_time

        return self.start_time + SessionLifetime.__chunk  # type: ignore[return-value, operator]

    def expired(self, *, time_point: datetime | None = None) -> bool:
        if time_point is None:
            time_point = datetime.now(UTC)

        if self.start_time is None:
            return not time_point <= self.end_time

        return not self.start_time <= time_point <= self.end_time

    def extend(
        self,
        *,
        time_point: datetime | None = None,
    ) -> "SessionLifetime":
        if time_point is None:
            time_point = datetime.now(UTC)

        extended_end_time = time_point + SessionLifetime.__chunk

        return SessionLifetime(
            _start_time=self._start_time,
            _end_time=extended_end_time,
        )

    def __post_init__(self) -> None:
        if self._start_time is None and self._end_time is None:
            raise SessionLifetime.NoPointsError

        if self._start_time is not None and self._start_time.tzinfo is not UTC:
            raise SessionLifetime.NotUTCStartTimeError

        if self._end_time is not None and self._end_time.tzinfo is not UTC:
            raise SessionLifetime.NotUTCEndTimeError

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SessionLifetime):
            return False

        is_start_time_correct = self.start_time == other.start_time
        is_end_time_correct = self.end_time == other.end_time

        return is_start_time_correct and is_end_time_correct
