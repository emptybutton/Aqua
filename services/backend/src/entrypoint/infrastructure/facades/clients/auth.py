from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator, Literal
from uuid import UUID

from auth.presentation.periphery import facade as auth
from entrypoint.infrastructure.periphery.error_wrapper import ErrorWrapper


@dataclass(kw_only=True, frozen=True, slots=True)
class Error:
    unexpected_error: Exception


async def close() -> None:
    await auth.close.perform()


@dataclass(kw_only=True, frozen=True, slots=True)
class RegisterUserOutputData:
    user_id: UUID
    username: str
    new_session_id: UUID


@asynccontextmanager
async def register_user(
    session_id: UUID | None,
    name: str,
    password: str,
) -> AsyncIterator[
    RegisterUserOutputData
    | Error
    | Literal["taken_username"]
    | Literal["empty_username"]
    | Literal["week_password"]
]:
    register_user = auth.register_user.perform(session_id, name, password)
    try:
        async with register_user as result:
            try:
                yield RegisterUserOutputData(
                    user_id=result.user_id,
                    username=result.username,
                    new_session_id=result.session_id,
                )
            except Exception as error:
                raise ErrorWrapper(error) from None
    except auth.register_user.TakenUsernameError:
        yield "taken_username"
    except auth.register_user.EmptyUsernameError:
        yield "empty_username"
    except auth.register_user.WeekPasswordError:
        yield "week_password"
    except ErrorWrapper as wrapper:
        raise wrapper.error from wrapper.error
    except Exception as error:
        yield Error(unexpected_error=error)


@dataclass(kw_only=True, frozen=True, slots=True)
class AuthenticateUserOutputData:
    user_id: UUID
    session_id: UUID


@asynccontextmanager
async def authenticate_user(
    session_id: UUID,
) -> AsyncIterator[
    AuthenticateUserOutputData
    | Error
    | Literal["no_session"]
    | Literal["expired_session"]
    | Literal["cancelled_session"]
    | Literal["replaced_session"]
]:
    try:
        async with auth.authenticate_user.perform(session_id) as result:
            try:
                yield AuthenticateUserOutputData(
                    user_id=result.user_id, session_id=result.session_id
                )
            except Exception as error:
                raise ErrorWrapper(error) from None
    except auth.authenticate_user.NoSessionError:
        yield "no_session"
    except auth.authenticate_user.ExpiredSessionError:
        yield "expired_session"
    except auth.authenticate_user.CancelledSessionError:
        yield "cancelled_session"
    except auth.authenticate_user.ReplacedSessionError:
        yield "replaced_session"
    except ErrorWrapper as wrapper:
        raise wrapper.error from wrapper.error
    except Exception as error:
        yield Error(unexpected_error=error)


@dataclass(kw_only=True, frozen=True, slots=True)
class ReadUserOutputData:
    user_id: UUID
    username: str


async def read_user(
    user_id: UUID,
) -> ReadUserOutputData | Error | Literal["no_user"]:
    try:
        result = await auth.read_user.perform(user_id)
    except Exception as error:
        return Error(unexpected_error=error)

    if result is None:
        return "no_user"

    return ReadUserOutputData(user_id=result.user_id, username=result.username)


@dataclass(kw_only=True, frozen=True, slots=True)
class AuthorizeUserOutputData:
    user_id: UUID
    username: str
    new_session_id: UUID


@asynccontextmanager
async def authorize_user(
    session_id: UUID | None,
    name: str,
    password: str,
) -> AsyncIterator[
    AuthorizeUserOutputData
    | Error
    | Literal["no_user"]
    | Literal["incorrect_password"]
]:
    authorize_user = auth.authorize_user.perform(session_id, name, password)
    try:
        async with authorize_user as result:
            try:
                yield AuthorizeUserOutputData(
                    user_id=result.user_id,
                    username=result.username,
                    new_session_id=result.session_id,
                )
            except Exception as error:
                raise ErrorWrapper(error) from None
    except auth.authorize_user.NoUserError:
        yield "no_user"
    except auth.authorize_user.IncorrectPasswordError:
        yield "incorrect_password"
    except ErrorWrapper as wrapper:
        raise wrapper.error from wrapper.error
    except Exception as error:
        yield Error(unexpected_error=error)


@dataclass(kw_only=True, frozen=True, slots=True)
class RenameUserOutputData:
    user_id: UUID
    new_username: str
    previous_username: str


@asynccontextmanager
async def rename_user(
    user_id: UUID,
    new_username: str,
) -> AsyncIterator[
    RenameUserOutputData
    | Error
    | Literal["no_user"]
    | Literal["new_username_taken"]
    | Literal["empty_new_username"]
]:
    rename_user = auth.rename_user.perform(user_id, new_username)
    try:
        async with rename_user as result:
            try:
                yield RenameUserOutputData(
                    user_id=result.user_id,
                    new_username=result.new_username,
                    previous_username=result.previous_username,
                )
            except Exception as error:
                raise ErrorWrapper(error) from None
    except auth.rename_user.NoUserError:
        yield "no_user"
    except auth.rename_user.NewUsernameTakenError:
        yield "new_username_taken"
    except auth.rename_user.EmptyUsernameError:
        yield "empty_new_username"
    except ErrorWrapper as wrapper:
        raise wrapper.error from wrapper.error
    except Exception as error:
        yield Error(unexpected_error=error)


@dataclass(kw_only=True, frozen=True, slots=True)
class ChangePasswordOutputData:
    user_id: UUID
    username: str
    session_id: UUID


@asynccontextmanager
async def change_password(
    session_id: UUID,
    user_id: UUID,
    new_password: str,
) -> AsyncIterator[
    ChangePasswordOutputData
    | Error
    | Literal["no_user"]
    | Literal["week_password"]
]:
    change_password = auth.change_password.perform(
        session_id,
        user_id,
        new_password,
    )
    try:
        async with change_password as result:
            try:
                yield ChangePasswordOutputData(
                    user_id=result.user_id,
                    username=result.username,
                    session_id=result.session_id,
                )
            except Exception as error:
                raise ErrorWrapper(error) from None
    except auth.change_password.NoUserError:
        yield "no_user"
    except auth.change_password.WeekPasswordError:
        yield "week_password"
    except ErrorWrapper as wrapper:
        raise wrapper.error from wrapper.error
    except Exception as error:
        yield Error(unexpected_error=error)


async def user_exists(username: str) -> bool | Error:
    try:
        try:
            return await auth.user_exists.perform(username)
        except Exception as error:
            raise ErrorWrapper(error) from None
    except ErrorWrapper as wrapper:
        raise wrapper.error from wrapper.error
    except Exception as error:
        return Error(unexpected_error=error)
