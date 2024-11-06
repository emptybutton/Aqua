from dataclasses import dataclass
from uuid import UUID

from result import Err, Ok

from auth.application import ports
from auth.application.usecases import (
    change_account_password as _change_password,
)
from auth.infrastructure.adapters import (
    mappers,
    repos,
)
from auth.infrastructure.adapters.transactions import (
    DBConnectionTransactionFactory,
)
from auth.presentation.di.containers import async_container


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    session_id: UUID
    user_id: UUID
    username: str


class Error(Exception): ...


class NoSessionError(Error): ...


class NoUserError(Error): ...


class WeekPasswordError(Error): ...


async def perform(
    session_id: UUID,
    user_id: UUID,
    new_password: str,
) -> Output:
    async with async_container() as container:
        result = await _change_password.change_account_password(
            user_id,
            new_password,
            session_id,
            accounts=await container.get(repos.db.DBAccounts, "repos"),
            account_mapper_in=await container.get(
                mappers.db.account.DBAccountMapperFactory, "mappers"
            ),
            account_name_mapper_in=await container.get(
                mappers.db.account_name.DBAccountNameMapperFactory, "mappers"
            ),
            session_mapper_in=await container.get(
                mappers.db.session.DBSessionMapperFactory, "mappers"
            ),
            transaction_for=await container.get(
                DBConnectionTransactionFactory, "transactions"
            ),
            logger=await container.get(ports.loggers.Logger, "loggers"),
        )

    match result:
        case Ok(output):
            return Output(
                user_id=output.account.id,
                username=output.account.current_name.text,
                session_id=output.session.id,
            )
        case Err("no_account"):
            raise NoUserError
        case Err("no_session_for_password_change"):
            raise NoSessionError
        case Err(_):
            raise WeekPasswordError
