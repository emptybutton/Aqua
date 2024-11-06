from auth.application.usecases import (
    view_account_with_name_exists as _view_account,
)
from auth.infrastructure.adapters import repos
from auth.presentation.di.containers import async_container


async def perform(username: str) -> bool:
    async with async_container() as container:
        return await _view_account.view_account_with_name_exists(
            username,
            accounts=await container.get(repos.db.DBAccounts, "repos"),
        )
