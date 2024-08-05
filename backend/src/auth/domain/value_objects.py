from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC
from functools import cached_property
from string import digits
from uuid import UUID

from auth.domain import errors


@dataclass(frozen=True)
class Username:
    text: str

    def __post_init__(self) -> None:
        if len(self.text) == 0:
            raise errors.EmptyUsername()


@dataclass(frozen=True)
class Password:
    text: str

    def __post_init__(self) -> None:
        if len(self.text) < 8:  # noqa: PLR2004
            raise errors.WeekPassword()

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
        if len(self.text) == 0:
            raise errors.EmptyPasswordHash()


@dataclass(frozen=True)
class RefreshToken:
    text: str
    expiration_date: datetime = field(
        default_factory=lambda: (datetime.now(UTC) + timedelta(days=60))
    )

    def __post_init__(self) -> None:
        if self.expiration_date.tzinfo is not UTC:
            raise errors.NotUTCExpirationDate()

    @cached_property
    def is_expired(self) -> bool:
        return self.expiration_date <= datetime.now(UTC)


@dataclass(frozen=True)
class AccessToken:
    user_id: UUID
    username: Username
    expiration_date: datetime = field(
        default_factory=lambda: (datetime.now(UTC) + timedelta(minutes=15))
    )

    def __post_init__(self) -> None:
        if self.expiration_date.tzinfo is not UTC:
            raise errors.NotUTCExpirationDate()

    @cached_property
    def is_expired(self) -> bool:
        return self.expiration_date <= datetime.now(UTC)


def refreshed(access_token: AccessToken) -> AccessToken:
    return AccessToken(access_token.user_id, access_token.username)
