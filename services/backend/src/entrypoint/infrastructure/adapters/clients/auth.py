from contextlib import asynccontextmanager
from typing import AsyncIterator, Literal
from uuid import UUID

from auth.presentation.periphery import facade as auth
from entrypoint.application.ports import clients


class AuthFacade(clients.auth.Auth):
    def __init__(self) -> None:
        self.__errors: list[Exception] = list()

    @property
    def errors(self) -> tuple[Exception, ...]:
        return tuple(self.__errors)

    async def close(self) -> None:
        await auth.close.perform()

    @asynccontextmanager
    async def register_user(
        self,
        session_id: UUID | None,
        name: str,
        password: str,
    ) -> AsyncIterator[
        clients.auth.RegisterUserOutput
        | Literal["auth_is_not_working"]
        | Literal["user_is_already_registered"]
        | Literal["empty_username"]
        | Literal["week_password"]
    ]:
        register_user = auth.register_user.perform(session_id, name, password)
        try:
            async with register_user as result:
                yield clients.auth.RegisterUserOutput(
                    user_id=result.user_id,
                    username=result.username,
                    session_id=result.session_id,
                )
        except auth.register_user.UserIsAlreadyRegisteredError:
            yield "user_is_already_registered"
        except auth.register_user.EmptyUsernameError:
            yield "empty_username"
        except auth.register_user.WeekPasswordError:
            yield "week_password"
        except Exception as error:
            self.__errors.append(error)
            yield "auth_is_not_working"

    @asynccontextmanager
    async def authenticate_user(
        self, session_id: UUID
    ) -> AsyncIterator[
        clients.auth.AuthenticateUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_session"]
        | Literal["expired_session"]
        | Literal["cancelled_session"]
        | Literal["replaced_session"]
    ]:
        try:
            async with auth.authenticate_user.perform(session_id) as result:
                yield clients.auth.AuthenticateUserOutput(
                    user_id=result.user_id, session_id=result.session_id
                )
        except auth.authenticate_user.NoSessionError:
            yield "no_session"
        except auth.authenticate_user.ExpiredSessionError:
            yield "expired_session"
        except auth.authenticate_user.CancelledSessionError:
            yield "cancelled_session"
        except auth.authenticate_user.ReplacedSessionError:
            yield "replaced_session"
        except Exception as error:
            self.__errors.append(error)
            yield "auth_is_not_working"

    @asynccontextmanager
    async def authorize_user(
        self,
        session_id: UUID | None,
        name: str,
        password: str,
    ) -> AsyncIterator[
        clients.auth.AuthorizeUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
        | Literal["incorrect_password"]
    ]:
        authorize_user = auth.authorize_user.perform(session_id, name, password)
        try:
            async with authorize_user as result:
                yield clients.auth.AuthorizeUserOutput(
                    user_id=result.user_id,
                    username=result.username,
                    session_id=result.session_id,
                )
        except auth.authorize_user.NoUserError:
            yield "no_user"
        except auth.authorize_user.IncorrectPasswordError:
            yield "incorrect_password"
        except Exception as error:
            self.__errors.append(error)
            yield "auth_is_not_working"

    async def read_user(
        self, user_id: UUID
    ) -> (
        clients.auth.ReadUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
    ):
        try:
            result = await auth.read_user.perform(user_id)
        except Exception as error:
            self.__errors.append(error)
            return "auth_is_not_working"

        if result is None:
            return "no_user"

        return clients.auth.ReadUserOutput(
            user_id=result.user_id, username=result.username
        )

    @asynccontextmanager
    async def rename_user(
        self,
        user_id: UUID,
        new_username: str,
    ) -> AsyncIterator[
        clients.auth.RenameUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
        | Literal["new_username_taken"]
        | Literal["empty_new_username"]
    ]:
        rename_user = auth.rename_user.perform(user_id, new_username)
        try:
            async with rename_user as result:
                yield clients.auth.RenameUserOutput(
                    user_id=result.user_id,
                    new_username=result.new_username,
                    previous_username=result.previous_username,
                )
        except auth.rename_user.NoUserError:
            yield "no_user"
        except auth.rename_user.NewUsernameTakenError:
            yield "new_username_taken"
        except auth.rename_user.EmptyUsernameError:
            yield "empty_new_username"
        except Exception as error:
            self.__errors.append(error)
            yield "auth_is_not_working"

    @asynccontextmanager
    async def change_password(
        self,
        session_id: UUID,
        user_id: UUID,
        new_password: str,
    ) -> AsyncIterator[
        clients.auth.ChangePasswordOutput
        | Literal["auth_is_not_working"]
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
                yield clients.auth.ChangePasswordOutput(
                    user_id=result.user_id,
                    username=result.username,
                    session_id=result.session_id,
                )
        except auth.change_password.NoUserError:
            yield "no_user"
        except auth.change_password.WeekPasswordError:
            yield "week_password"
        except Exception as error:
            self.__errors.append(error)
            yield "auth_is_not_working"

    async def user_exists(
        self,
        username: str,
    ) -> bool | Literal["auth_is_not_working"]:
        try:
            return await auth.user_exists.perform(username)
        except Exception as error:
            self.__errors.append(error)
            return "auth_is_not_working"
