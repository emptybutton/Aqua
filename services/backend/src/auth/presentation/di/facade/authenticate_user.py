from dataclasses import dataclass
from uuid import UUID

from result import is_ok
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from auth.application import ports
from auth.application.usecases import authenticate as _authenticate
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
    user_id: UUID
    session_id: UUID


class Error(Exception): ...


class NoSessionError(Error): ...


class ExpiredSessionError(Error): ...


class CancelledSessionError(Error): ...


class ReplacedSessionError(Error): ...


async def perform(
    session_id: UUID,
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
        result = await _authenticate.authenticate(
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

    if is_ok(result):
        value = result.ok()
        return Output(user_id=value.account_id, session_id=value.session_id)

    error = result.err()

    if error in {"no_account", "no_session_for_secondary_authentication"}:
        raise NoSessionError

    if error == "expired_session_for_secondary_authentication":
        raise ExpiredSessionError

    if error == "cancelled_session_for_secondary_authentication":
        raise CancelledSessionError

    if error == "replaced_session_for_secondary_authentication":
        raise ReplacedSessionError

    raise Error
