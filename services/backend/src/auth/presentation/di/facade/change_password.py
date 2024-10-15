from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from auth.application import ports
from auth.application.usecases import (
    change_account_password as _change_password,
)
from auth.domain.models.access import vos
from auth.domain.models.access.aggregates.account.root import Account
from auth.infrastructure.adapters import (
    mappers,
    repos,
)
from auth.presentation.di.containers import async_container
from shared.infrastructure.adapters import indexes
from shared.infrastructure.adapters.transactions import (
    DBConnectionTransactionFactory,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    session_id: UUID
    user_id: UUID
    username: str


NoSessionError: TypeAlias = Account.NoSessionForPasswordChangeError

NoUserError: TypeAlias = _change_password.NoAccountError

WeekPasswordError: TypeAlias = vos.password.Password.WeekError

Error: TypeAlias = (
    _change_password.Error
    | vos.password.Password.WeekError
    | Account.NoSessionForPasswordChangeError
)


async def perform(
    session_id: UUID,
    user_id: UUID,
    new_password: str,
    *,
    session: AsyncSession | None,
    connection: AsyncConnection | None = None,
) -> Output:
    """Parameter `session` is deprecated, use `connection`."""

    request_container = async_container(context={
        AsyncSession | None: session, AsyncConnection | None: connection
    })
    async with request_container as container:
        result = await _change_password.change_account_password(
            user_id,
            new_password,
            session_id,
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
            logger=await container.get(ports.loggers.Logger, "loggers"),
        )

    return Output(
        user_id=result.account.id,
        username=result.account.current_name.text,
        session_id=result.session.id,
    )
