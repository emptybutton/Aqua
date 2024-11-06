from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal
from uuid import UUID


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


class Auth(ABC):
    @abstractmethod
    async def register_user(
        self,
        session_id: UUID | None,
        name: str,
        password: str,
    ) -> (
        RegisterUserOutput
        | Literal["auth_is_not_working"]
        | Literal["user_is_already_registered"]
        | Literal["empty_username"]
        | Literal["week_password"]
    ): ...

    @abstractmethod
    async def authenticate_user(
        self, session_id: UUID
    ) -> (
        AuthenticateUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_session"]
        | Literal["expired_session"]
        | Literal["cancelled_session"]
        | Literal["replaced_session"]
    ): ...

    @abstractmethod
    async def authorize_user(
        self,
        session_id: UUID | None,
        name: str,
        password: str,
    ) -> (
        AuthorizeUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
        | Literal["incorrect_password"]
    ): ...

    @abstractmethod
    async def read_user(
        self, user_id: UUID
    ) -> (
        ReadUserOutput | Literal["auth_is_not_working"] | Literal["no_user"]
    ): ...

    @abstractmethod
    async def rename_user(
        self,
        user_id: UUID,
        new_username: str,
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
    ) -> (
        ChangePasswordOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
        | Literal["week_password"]
    ): ...

    @abstractmethod
    async def user_exists(
        self,
        username: str,
    ) -> bool | Literal["auth_is_not_working"]: ...
