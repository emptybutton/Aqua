from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator
from uuid import UUID

from result import is_ok

from auth.application import ports
from auth.application.usecases.authenticate import authenticate as _authenticate
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
    user_id: UUID
    session_id: UUID


class Error(Exception): ...


class NoSessionError(Error): ...


class ExpiredSessionError(Error): ...


class CancelledSessionError(Error): ...


class ReplacedSessionError(Error): ...


@asynccontextmanager
async def perform(session_id: UUID) -> AsyncIterator[Output]:
    async with async_container() as container, _authenticate(
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
    ) as result:
        if is_ok(result):
            value = result.ok()
            yield Output(user_id=value.account_id, session_id=value.session_id)
            return

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
