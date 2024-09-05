from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Literal, TypeVar
from uuid import UUID

from shared.application.ports.transactions import Transaction


_TransactionT_contra = TypeVar(
    "_TransactionT_contra", bound=Transaction, contravariant=True
)


@dataclass(kw_only=True, frozen=True)
class RegisterUserOutput:
    user_id: UUID
    username: str
    session_id: UUID


@dataclass(kw_only=True, frozen=True)
class AuthenticateUserOutput:
    user_id: UUID
    session_id: UUID


@dataclass(kw_only=True, frozen=True)
class ReadUserOutput:
    user_id: UUID
    username: str


@dataclass(kw_only=True, frozen=True)
class AuthorizeUserOutput:
    user_id: UUID
    username: str
    session_id: UUID


@dataclass(kw_only=True, frozen=True)
class RenameUserOutput:
    user_id: UUID
    new_username: str
    previous_username: str


@dataclass(kw_only=True, frozen=True)
class ChangePasswordOutput:
    user_id: UUID
    username: str
    session_id: UUID


class Auth(Generic[_TransactionT_contra], ABC):
    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    async def register_user(
        self, name: str, password: str, *, transaction: _TransactionT_contra
    ) -> (
        RegisterUserOutput
        | Literal["auth_is_not_working"]
        | Literal["user_is_already_registered"]
        | Literal["empty_username"]
        | Literal["week_password"]
    ): ...

    @abstractmethod
    async def authenticate_user(
        self, session_id: UUID, *, transaction: _TransactionT_contra
    ) -> (
        AuthenticateUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_session"]
        | Literal["expired_session"]
        | Literal["cancelled_session"]
    ): ...

    @abstractmethod
    async def authorize_user(
        self, name: str, password: str, *, transaction: _TransactionT_contra
    ) -> (
        AuthorizeUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
        | Literal["incorrect_password"]
    ): ...

    @abstractmethod
    async def read_user(
        self, user_id: UUID, *, transaction: _TransactionT_contra
    ) -> (
        ReadUserOutput | Literal["auth_is_not_working"] | Literal["no_user"]
    ): ...

    @abstractmethod
    async def rename_user(
        self,
        user_id: UUID,
        new_username: str,
        *,
        transaction: _TransactionT_contra,
    ) -> (
        RenameUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
        | Literal["new_username_taken"]
        | Literal["empty_new_username"]
    ): ...

    @abstractmethod
    async def change_password(
        self,
        session_id: UUID,
        user_id: UUID,
        new_password: str,
        *,
        transaction: _TransactionT_contra,
    ) -> (
        ChangePasswordOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
        | Literal["week_password"]
    ): ...
