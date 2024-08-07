from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC
from functools import cached_property
from string import digits
from uuid import UUID


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
        if len(self.text) < 8:  # noqa: PLR2004
            raise Password.TooShortError

        if self.text.upper() == self.text:
            raise Password.OnlyCapitalLettersError

        if self.text.lower() == self.text:
            raise Password.OnlySmallLettersError

        if self.__has_no_digits():
            raise Password.NoDigitsError

        if self.__has_only_digits():
            raise Password.OnlyDigitsError

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


@dataclass(kw_only=True, frozen=True)
class RefreshToken:
    class Error(Exception): ...

    class NotUTCExpirationDateError(Error): ...

    text: str
    expiration_date: datetime = field(
        default_factory=lambda: (datetime.now(UTC) + timedelta(days=60))
    )

    def __post_init__(self) -> None:
        if self.expiration_date.tzinfo is not UTC:
            raise RefreshToken.NotUTCExpirationDateError

    @cached_property
    def is_expired(self) -> bool:
        return self.expiration_date <= datetime.now(UTC)


@dataclass(kw_only=True, frozen=True)
class AccessToken:
    class Error(Exception): ...

    class NotUTCExpirationDateError(Error): ...

    user_id: UUID
    expiration_date: datetime = field(
        default_factory=lambda: (datetime.now(UTC) + timedelta(minutes=15))
    )

    def __post_init__(self) -> None:
        if self.expiration_date.tzinfo is not UTC:
            raise AccessToken.NotUTCExpirationDateError

    @cached_property
    def is_expired(self) -> bool:
        return self.expiration_date <= datetime.now(UTC)

    class AuthenticationError(Error): ...

    class ExpiredForAuthenticationError(AuthenticationError): ...

    def authenticate(self) -> None:
        if self.is_expired:
            raise AccessToken.ExpiredForAuthenticationError

    class RefreshingError(Error): ...

    class ExpiredRefreshTokenForRefreshingError(RefreshingError): ...

    def refresh(self, *, refresh_token: RefreshToken) -> "AccessToken":
        if refresh_token.is_expired:
            raise AccessToken.ExpiredRefreshTokenForRefreshingError

        return AccessToken(user_id=self.user_id)
