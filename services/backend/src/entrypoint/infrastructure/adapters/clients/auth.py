from typing import Literal
from uuid import UUID

from auth.presentation.di import facade as auth
from entrypoint.application.ports import clients
from shared.infrastructure.adapters.transactions import DBTransaction


class AuthFacade(clients.auth.Auth[DBTransaction]):
    def __init__(self) -> None:
        self.__errors: list[Exception] = list()

    @property
    def errors(self) -> tuple[Exception, ...]:
        return tuple(self.__errors)

    async def close(self) -> None:
        await auth.close.perform()

    async def register_user(
        self, name: str, password: str, *, transaction: DBTransaction
    ) -> (
        clients.auth.RegisterUserOutput
        | Literal["auth_is_not_working"]
        | Literal["empty_username"]
        | Literal["week_password"]
    ):
        try:
            result = await auth.register_user.perform(
                name, password, session=transaction.session
            )
        except auth.register_user.EmptyUsernameError:
            return "empty_username"
        except auth.register_user.WeekPasswordError:
            return "week_password"

        return clients.auth.RegisterUserOutput(
            user_id=result.user_id,
            username=result.username,
            session_id=result.session_id,
        )

    async def authenticate_user(
        self, session_id: UUID, *, transaction: DBTransaction
    ) -> (
        clients.auth.AuthenticateUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_session"]
        | Literal["expired_session"]
    ):
        try:
            result = await auth.authenticate_user.perform(
                session_id, session=transaction.session
            )
        except auth.authenticate_user.NoSessionError:
            return "no_session"
        except auth.authenticate_user.ExpiredSessionError:
            return "expired_session"
        except Exception as error:
            self.__errors.append(error)
            return "auth_is_not_working"

        return clients.auth.AuthenticateUserOutput(
            user_id=result.user_id, session_id=result.session_id
        )

    async def authorize_user(
        self, name: str, password: str, *, transaction: DBTransaction
    ) -> (
        clients.auth.AuthorizeUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
        | Literal["incorrect_password"]
    ):
        try:
            result = await auth.authorize_user.perform(
                name, password, session=transaction.session
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
        self, user_id: UUID, *, transaction: DBTransaction
    ) -> (
        clients.auth.ReadUserOutput
        | Literal["auth_is_not_working"]
        | Literal["no_user"]
    ):
        try:
            session = transaction.session
            result = await auth.read_user.perform(user_id, session=session)
        except Exception as error:
            self.__errors.append(error)
            return "auth_is_not_working"

        if result is None:
            return "no_user"

        return clients.auth.ReadUserOutput(
            user_id=result.user_id, username=result.username
        )
