from auth.application.ports.gateway import (
    SessionAndPresenceOfAccountNameWithText,
)
from auth.application.ports.repos import Accounts
from auth.domain.model.access.aggregates.account.ports.specs import (
    is_account_name_text_taken,
)


class IsAccountNameTextTakenBasedOnGatewayResult(
    is_account_name_text_taken.IsAccountNameTextTaken
):
    def __init__(
        self, gateway_result: SessionAndPresenceOfAccountNameWithText
    ) -> None:
        self.__gateway_result = gateway_result

    async def __call__(self, _: str) -> bool:
        return self.__gateway_result.contains_account_name_with_text


class IsAccountNameTextTakenInRepo(
    is_account_name_text_taken.IsAccountNameTextTaken
):
    def __init__(self, accounts: Accounts) -> None:
        self.__accounts = accounts

    async def __call__(self, name_text: str) -> bool:
        return await self.__accounts.contains_account_with_name(
            name_text=name_text
        )
