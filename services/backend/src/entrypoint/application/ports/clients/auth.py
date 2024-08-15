from abc import abstractmethod, ABC
from dataclasses import dataclass
from datetime import datetime
from typing import TypeVar, Generic, Literal
from uuid import UUID

from shared.application.ports.transactions import Transaction


_TransactionT_contra = TypeVar(
    "_TransactionT_contra",
    bound=Transaction,
    contravariant=True,
)


@dataclass(kw_only=True, frozen=True)
class RegisterUserOutput:
    user_id: UUID
    username: str
    refresh_token: str
    refresh_token_expiration_date: datetime
    jwt: str


@dataclass(kw_only=True, frozen=True)
class AuthenticateUserOutput:
    user_id: UUID


@dataclass(kw_only=True, frozen=True)
class ReadUserOutput:
    user_id: UUID
    username: str


@dataclass(kw_only=True, frozen=True)
class AuthorizeUserOutput:
    user_id: UUID
    username: str
    jwt: str
    refresh_token: str
    refresh_token_expiration_date: datetime


@dataclass(kw_only=True, frozen=True)
class RefreshTokenOutput:
    jwt: str
    refresh_token: str
    refresh_token_expiration_date: datetime


class Auth(Generic[_TransactionT_contra], ABC):
    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    async def register_user(
        self,
        name: str,
        password: str,
        *,
        transaction: _TransactionT_contra,
    ) -> (
        RegisterUserOutput
        | Literal["auth_is_not_working"]
        | Literal["user_is_already_registered"]
        | Literal["empty_username"]
        | Literal["week_password"]
    ): ...

    @abstractmethod
    async def authenticate_user(self, jwt: str) -> (
        AuthenticateUserOutput
        | Literal["auth_is_not_working"]
        | Literal["invalid_jwt"]
        | Literal["expired_jwt"]
    ): ...

    @abstractmethod
    async def authorize_user(
        self,
        name: str,
        password: str,
        *,
        transaction: _TransactionT_contra,
    ) -> (
        AuthorizeUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
        | Literal["incorrect_password"]
    ): ...

    @abstractmethod
    async def read_user(
        self,
        user_id: UUID,
        *,
        transaction: _TransactionT_contra,
    ) -> (
        ReadUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
    ): ...

    @abstractmethod
    async def refresh_token(
        self,
        jwt: str,
        refresh_token: str,
        refresh_token_expiration_date: datetime,
        *,
        transaction: _TransactionT_contra,
    ) -> (
        RefreshTokenOutput
        | Literal["auth_is_not_working"]
        | Literal["invalid_jwt"]
        | Literal["not_utc_refresh_token_expiration_date"]
        | Literal["expired_refresh_token"]
    ): ...
