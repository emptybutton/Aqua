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

    class NotUTCStartTimeError(Error): ...

    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    __start_time: datetime | None = field(
        default_factory=lambda: datetime.now(UTC)
    )
    __end_time: datetime = field(
        default_factory=lambda: Session.__create_end_time()
    )

    @property
    def start_time(self) -> datetime | None:
        return self.__start_time

    @start_time.setter
    def start_time(self, start_time: datetime | None) -> None:
        if start_time is not None and start_time.tzinfo is not UTC:
            raise Session.NotUTCStartTimeError

        self.__start_time = start_time

    @property
    def end_time(self) -> datetime:
        return self.__end_time

    @end_time.setter
    def end_time(self, end_time: datetime) -> None:
        if end_time.tzinfo is not UTC:
            raise Session.NotUTCExpirationDateError

        self.__end_time = end_time

    @property
    def is_expired(self) -> bool:
        return self.__end_time <= datetime.now(UTC)

    class AuthenticationError(Error): ...

    class ExpiredForAuthenticationError(AuthenticationError): ...

    def authenticate(self) -> None:
        if self.is_expired:
            raise Session.ExpiredForAuthenticationError

        self.__end_time = self.__extended_end_time

    @classmethod
    def for_(cls, user: User) -> "Session":
        return Session(user_id=user.id)

    def __post_init__(self) -> None:
        self.end_time = self.__end_time
        self.start_time = self.__start_time

    @property
    def __extended_end_time(self) -> datetime:
        return self.__create_end_time()

    @classmethod
    def __create_end_time(cls) -> datetime:
        return datetime.now(UTC) + Session.lifespan
