from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from auth.application import ports
from auth.application.usecases import create_account
from auth.domain.models.access import vos
from auth.domain.models.access.aggregates import account as _account
from auth.infrastructure.adapters import (
    gateways,
    mappers,
    repos,
)
from auth.presentation.di.containers import async_container
from shared.infrastructure.adapters import indexes
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


UserIsAlreadyRegisteredError: TypeAlias = _AccountName.TakenForCreationError

EmptyUsernameError: TypeAlias = _AccountName.EmptyError

WeekPasswordError: TypeAlias = vos.password.Password.WeekError

Error: TypeAlias = _AccountName.Error | vos.password.Password.Error


async def perform(
    session_id: UUID | None,
    username: str,
    password: str,
    *,
    session: AsyncSession | None,
    connection: AsyncConnection | None = None,
) -> Output:
    """Parameter `session` is deprecated, use `connection`."""

    request_container = async_container(context={
        AsyncSession | None: session, AsyncConnection | None: connection
    })
    async with request_container as container:
        result = await create_account.create_account(
            session_id,
            username,
            password,
            empty_index_factory=await container.get(
                indexes.EmptySortingIndexFactory, "indexes"
            ),
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

    return Output(
        user_id=result.account.id,
        username=result.account.current_name.text,
        session_id=result.session.id,
    )
