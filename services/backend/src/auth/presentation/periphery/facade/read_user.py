from dataclasses import dataclass
from uuid import UUID

from auth.application.usecases import view_account
from auth.infrastructure.adapters import repos, views
from auth.presentation.di.containers import async_container


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    user_id: UUID
    username: str


async def perform(user_id: UUID) -> Output | None:
    async with async_container() as container:
        view = await view_account.view_account(
            user_id,
            accounts=await container.get(repos.db.DBAccounts, "repos"),
            account_view_from=await container.get(
                views.db.DBAccountViewFrom, "views"
            ),
        )

    if view is None:
        return None

    return Output(
        user_id=view.account_id,
        username=view.account_current_name_text,
    )
