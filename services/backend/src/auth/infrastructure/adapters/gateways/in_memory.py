from typing import TypeAlias
from uuid import UUID

from auth.application.ports import gateway as _gateway
from auth.domain.models.access.aggregates import account as _account
from auth.infrastructure.adapters.repos.in_memory import InMemoryAccounts


_Account: TypeAlias = _account.root.Account
_Session: TypeAlias = _account.internal.entities.session.Session


class InMemoryGateway(_gateway.Gateway):
    def __init__(self, in_memory_accounts: InMemoryAccounts) -> None:
        self.__in_memory_accounts = in_memory_accounts

    async def session_with_id_and_contains_account_name_with_text(
        self,
        *,
        session_id: UUID,
        account_name_text: str,
    ) -> _gateway.SessionAndPresenceOfAccountNameWithText:
        presence = await self.__in_memory_accounts.contains_account_with_name(
            name_text=account_name_text,
        )
        session = self.__in_memory_accounts.storage.sessions_with_id(session_id)

        return _gateway.SessionAndPresenceOfAccountNameWithText(
            session=session, contains_account_name_with_text=presence
        )

    async def session_with_id_and_account_with_name(
        self, *, session_id: UUID, account_name_text: str
    ) -> _gateway.SessionAndAccount:
        account = await self.__in_memory_accounts.account_with_name(
            name_text=account_name_text
        )
        session = self.__in_memory_accounts.storage.sessions_with_id(session_id)

        return _gateway.SessionAndAccount(session=session, account=account)

    async def session_with_id(self, session_id: UUID) -> _Session | None:
        return self.__in_memory_accounts.storage.sessions_with_id(session_id)

    async def account_with_id_and_contains_account_name_with_text(
        self,
        *,
        account_id: UUID,
        account_name_text: str,
    ) -> _gateway.AccountAndPresenceOfAccountNameWithText:
        account = await self.__in_memory_accounts.account_with_id(account_id)
        presence = await self.__in_memory_accounts.contains_account_with_name(
            name_text=account_name_text,
        )

        return _gateway.AccountAndPresenceOfAccountNameWithText(
            account=account, contains_account_name_with_text=presence
        )


class InMemoryGatewayFactory(_gateway.GatewayFactory[InMemoryAccounts]):
    def __call__(self, in_memory_accounts: InMemoryAccounts) -> InMemoryGateway:
        return InMemoryGateway(in_memory_accounts)
