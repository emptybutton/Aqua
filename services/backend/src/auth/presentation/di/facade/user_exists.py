from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession

from auth.application.usecases import (
    view_account_with_name_exists as _view_account,
)
from auth.infrastructure.adapters import repos
from auth.presentation.di.containers import async_container


async def perform(
    username: str,
    *,
    session: AsyncSession | None,
    connection: AsyncConnection | None = None,
) -> bool:
    """Parameter `session` is deprecated, use `connection`."""

    request_container = async_container(
        context={
            AsyncSession | None: session,
            AsyncConnection | None: connection,
        }
    )
    async with request_container as container:
        return await _view_account.view_account_with_name_exists(
            username,
            accounts=await container.get(repos.db.DBAccounts, "repos"),
        )
