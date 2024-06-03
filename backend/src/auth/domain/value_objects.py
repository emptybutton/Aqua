from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import cached_property
from typing import Optional
from string import digits

from src.auth.domain import errors


@dataclass(frozen=True)
class Username:
    text: str

    def __post_init__(self) -> None:
        if len(self.text) <= 0 or len(self.text) > 64:  # noqa: PLR2004
            raise errors.ExtremeUsernameLength()


@dataclass(frozen=True)
class Password:
    text: str

    def __post_init__(self) -> None:
        if len(self.text) < 8:  # noqa: PLR2004
            raise errors.WeekPassword()

        if len(self.text) > 128:  # noqa: PLR2004
            raise errors.TooLongPassword()

        if self.text.upper() == self.text:
            raise errors.WeekPassword()

        if self.text.lower() == self.text:
            raise errors.WeekPassword()

        if self.__has_no_digits():
            raise errors.WeekPassword()

        if self.__has_only_digits():
            raise errors.WeekPassword()

    def __has_no_digits(self) -> bool:
        return set(digits) - set(self.text) == set(digits)

    def __has_only_digits(self) -> bool:
        return set(self.text) - set(digits) == set()


@dataclass(frozen=True)
class PasswordHash:
    text: str

    def __post_init__(self) -> None:
        if len(self.text) <= 0 or len(self.text) > 512:  # noqa: PLR2004
            raise errors.ExtremePasswordHashLength()


@dataclass(frozen=True)
class RefreshToken:
    text: str
    expiration_date: datetime = field(
        default_factory=lambda: (datetime.now() + timedelta(days=60))
    )

    @cached_property
    def is_expired(self) -> bool:
        return self.expiration_date <= datetime.now()


@dataclass(frozen=True)
class AccessToken:
    user_id: Optional[int]
    username: Username
    expiration_date: datetime = field(
        default_factory=lambda: (datetime.now() + timedelta(minutes=15))
    )

    @cached_property
    def is_expired(self) -> bool:
        return self.expiration_date <= datetime.now()
