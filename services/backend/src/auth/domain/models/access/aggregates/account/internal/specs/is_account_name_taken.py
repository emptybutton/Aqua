from typing import TYPE_CHECKING, TypeAlias

from auth.domain.models.access.aggregates.account.ports.specs import (
    is_account_name_text_taken as _is_account_name_text_taken,
)
from shared.domain.framework.high_level_spec import HighLevelSpec


if TYPE_CHECKING:
    from auth.domain.models.access.aggregates.account.internal.entities import (
        account_name as _account_name,
    )


_IsAccountNameTextTaken: TypeAlias = (
    _is_account_name_text_taken.IsAccountNameTextTaken
)


class IsAccountNameTaken(HighLevelSpec["_account_name.AccountName"]):
    def __init__(
        self,
        is_account_name_text_taken: _IsAccountNameTextTaken,
    ) -> None:
        self.__is_account_name_text_taken = is_account_name_text_taken

    async def __call__(self, account_name: "_account_name.AccountName") -> bool:
        return await self.__is_account_name_text_taken(account_name.text)
