from typing import Literal
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

    async def register_user(
        self,
        session_id: UUID | None,
        name: str,
        password: str,
    ) -> (
        clients.auth.RegisterUserOutput
        | Literal["auth_is_not_working"]
        | Literal["user_is_already_registered"]
        | Literal["empty_username"]
        | Literal["week_password"]
    ):
        try:
            result = await auth.register_user.perform(
                session_id, name, password
            )
        except auth.register_user.UserIsAlreadyRegisteredError:
            return "user_is_already_registered"
        except auth.register_user.EmptyUsernameError:
            return "empty_username"
        except auth.register_user.WeekPasswordError:
            return "week_password"
        except Exception as error:
            self.__errors.append(error)
            return "auth_is_not_working"

        return clients.auth.RegisterUserOutput(
            user_id=result.user_id,
            username=result.username,
            session_id=result.session_id,
        )

    async def authenticate_user(
        self, session_id: UUID
    ) -> (
        clients.auth.AuthenticateUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_session"]
        | Literal["expired_session"]
        | Literal["cancelled_session"]
        | Literal["replaced_session"]
    ):
        try:
            result = await auth.authenticate_user.perform(session_id)
        except auth.authenticate_user.NoSessionError:
            return "no_session"
        except auth.authenticate_user.ExpiredSessionError:
            return "expired_session"
        except auth.authenticate_user.CancelledSessionError:
            return "cancelled_session"
        except auth.authenticate_user.ReplacedSessionError:
            return "replaced_session"
        except Exception as error:
            self.__errors.append(error)
            return "auth_is_not_working"

        return clients.auth.AuthenticateUserOutput(
            user_id=result.user_id, session_id=result.session_id
        )

    async def authorize_user(
        self,
        session_id: UUID | None,
        name: str,
        password: str,
    ) -> (
        clients.auth.AuthorizeUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
        | Literal["incorrect_password"]
    ):
        try:
            result = await auth.authorize_user.perform(
                session_id, name, password
            )
        except auth.authorize_user.NoUserError:
            return "no_user"
        except auth.authorize_user.IncorrectPasswordError:
            return "incorrect_password"
        except Exception as error:
            self.__errors.append(error)
            return "auth_is_not_working"

        return clients.auth.AuthorizeUserOutput(
            user_id=result.user_id,
            username=result.username,
            session_id=result.session_id,
        )

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

    async def rename_user(
        self,
        user_id: UUID,
        new_username: str,
    ) -> (
        clients.auth.RenameUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
        | Literal["new_username_taken"]
        | Literal["empty_new_username"]
    ):
        try:
            result = await auth.rename_user.perform(
                user_id,
                new_username,
            )
        except auth.rename_user.NoUserError:
            return "no_user"
        except auth.rename_user.NewUsernameTakenError:
            return "new_username_taken"
        except auth.rename_user.EmptyUsernameError:
            return "empty_new_username"
        except Exception as error:
            self.__errors.append(error)
            return "auth_is_not_working"

        return clients.auth.RenameUserOutput(
            user_id=result.user_id,
            new_username=result.new_username,
            previous_username=result.previous_username,
        )

    async def change_password(
        self,
        session_id: UUID,
        user_id: UUID,
        new_password: str,
    ) -> (
        clients.auth.ChangePasswordOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
        | Literal["week_password"]
    ):
        try:
            result = await auth.change_password.perform(
                session_id,
                user_id,
                new_password,
            )
        except auth.change_password.NoUserError:
            return "no_user"
        except auth.change_password.WeekPasswordError:
            return "week_password"
        except Exception as error:
            self.__errors.append(error)
            return "auth_is_not_working"

        return clients.auth.ChangePasswordOutput(
            user_id=result.user_id,
            username=result.username,
            session_id=result.session_id,
        )

    async def user_exists(
        self,
        username: str,
    ) -> bool | Literal["auth_is_not_working"]:
        try:
            return await auth.user_exists.perform(username)
        except Exception as error:
            self.__errors.append(error)
            return "auth_is_not_working"
