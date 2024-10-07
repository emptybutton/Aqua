from typing import Iterable, TypeAlias

from auth.application.ports.gateway import (
    AccountAndPresenceOfAccountNameWithText,
    SessionAndPresenceOfAccountNameWithText,
)
from auth.application.ports.repos import Accounts
from auth.domain.models.access.aggregates.account.ports.specs import (
    is_account_name_text_taken,
)


class IsAccountNameTextTakenBasedOnCache(
    is_account_name_text_taken.IsAccountNameTextTaken
):
    class Error(Exception): ...

    class TakenAndNotTakenAccountNameTexts(Error): ...

    GatewayResult: TypeAlias = (
        AccountAndPresenceOfAccountNameWithText
        | SessionAndPresenceOfAccountNameWithText
    )

    def __init__(
        self,
        *,
        is_uncached_account_name_text_taken: (
            is_account_name_text_taken.IsAccountNameTextTaken
        ),
        taken_account_name_texts: Iterable[str] = tuple(),
        not_taken_account_name_texts: Iterable[str] = tuple(),
    ) -> None:
        self.__is_uncached_account_name_text_taken = (
            is_uncached_account_name_text_taken
        )
        self.__taken_account_name_texts = frozenset(taken_account_name_texts)
        self.__not_taken_account_name_texts = frozenset(
            not_taken_account_name_texts
        )

        taken_and_not_taken_account_name_texts = (
            self.__taken_account_name_texts
            & self.__not_taken_account_name_texts
        )

        if taken_and_not_taken_account_name_texts:
            raise (
                IsAccountNameTextTakenBasedOnCache
                .TakenAndNotTakenAccountNameTexts
            )

    async def __call__(self, name_text: str) -> bool:
        if name_text in self.__taken_account_name_texts:
            return True

        if name_text in self.__not_taken_account_name_texts:
            return False

        return await self.__is_uncached_account_name_text_taken(name_text)

    @classmethod
    def of(
        cls,
        gateway_result: GatewayResult,
        *,
        name_text: str,
        is_account_name_text_taken: (
            is_account_name_text_taken.IsAccountNameTextTaken
        ),
    ) -> "IsAccountNameTextTakenBasedOnCache":
        if gateway_result.contains_account_name_with_text:
            return IsAccountNameTextTakenBasedOnCache(
                taken_account_name_texts=[name_text],
                is_uncached_account_name_text_taken=(
                    is_account_name_text_taken
                ),
            )

        return IsAccountNameTextTakenBasedOnCache(
            not_taken_account_name_texts=[name_text],
            is_uncached_account_name_text_taken=(
                is_account_name_text_taken
            ),
        )


class IsAccountNameTextTakenInRepo(
    is_account_name_text_taken.IsAccountNameTextTaken
):
    def __init__(self, accounts: Accounts) -> None:
        self.__accounts = accounts

    async def __call__(self, name_text: str) -> bool:
        return await self.__accounts.contains_account_with_name(
            name_text=name_text
        )
