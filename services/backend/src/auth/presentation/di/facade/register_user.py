from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from result import Err, Ok
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from auth.application import ports
from auth.application.usecases import create_account
from auth.domain.models.access.aggregates import account as _account
from auth.infrastructure.adapters import (
    gateways,
    mappers,
    repos,
)
from auth.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import (
    DBConnectionTransactionFactory,
)


_Account: TypeAlias = _account.root.Account
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    user_id: UUID
    username: str
    session_id: UUID


class Error(Exception): ...


class UserIsAlreadyRegisteredError(Error): ...


class EmptyUsernameError(Error): ...


class WeekPasswordError(Error): ...


async def perform(
    session_id: UUID | None,
    username: str,
    password: str,
    *,
    session: AsyncSession | None,
    connection: AsyncConnection | None = None,
) -> Output:
    """Parameter `session` is deprecated, use `connection`."""

    request_container = async_container(
        context={
            AsyncSession | None: session,
            AsyncConnection | None: connection,
        }
    )
    async with request_container as container:
        result = await create_account.create_account(
            session_id,
            username,
            password,
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
            gateway_to=await container.get(
                gateways.db.DBGatewayFactory, "gateways"
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
        case Err("account_name_text_is_empty"):
            raise EmptyUsernameError
        case Err("account_name_is_taken"):
            raise UserIsAlreadyRegisteredError
        case Err(_):
            raise WeekPasswordError
