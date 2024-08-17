from dataclasses import dataclass, field
from datetime import datetime, timedelta, UTC
from uuid import uuid4, UUID
from typing import ClassVar

from auth.domain.value_objects import Username, PasswordHash


@dataclass(kw_only=True)
class User:
    class Error(Exception): ...

    id: UUID = field(default_factory=uuid4)
    name: Username
    password_hash: PasswordHash

    class AuthorizationError(Error): ...

    class IncorrectPasswordHashForAuthorizationError(AuthorizationError): ...

    def authorize(self, *, password_hash: PasswordHash) -> None:
        if self.password_hash != password_hash:
            raise User.IncorrectPasswordHashForAuthorizationError


@dataclass(kw_only=True)
class Session:
    lifespan: ClassVar[timedelta] = timedelta(days=60)

    class Error(Exception): ...

    class NotUTCExpirationDateError(Error): ...

    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    __expiration_date: datetime = field(
        default_factory=lambda: Session.__create_expiration_date()
    )

    @property
    def expiration_date(self) -> datetime:
        return self.__expiration_date

    @expiration_date.setter
    def expiration_date(self, expiration_date: datetime) -> None:
        if expiration_date.tzinfo is not UTC:
            raise Session.NotUTCExpirationDateError

        self.__expiration_date = expiration_date

    @property
    def is_expired(self) -> bool:
        return self.__expiration_date <= datetime.now(UTC)

    class AuthenticationError(Error): ...

    class ExpiredForAuthenticationError(AuthenticationError): ...

    def authenticate(self) -> None:
        if self.is_expired:
            raise Session.ExpiredForAuthenticationError

        self.__expiration_date = self.__extended_expiration_date

    @classmethod
    def for_(cls, user: User) -> "Session":
        return Session(user_id=user.id)

    def __post_init__(self) -> None:
        self.expiration_date = self.__expiration_date

    @property
    def __extended_expiration_date(self) -> datetime:
        return self.__create_expiration_date()

    @classmethod
    def __create_expiration_date(cls) -> datetime:
        return datetime.now(UTC) + Session.lifespan
