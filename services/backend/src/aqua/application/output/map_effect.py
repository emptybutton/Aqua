from aqua.application.ports.mappers import UserMapper
from aqua.domain.model.core.aggregates.user.root import (
    TranslatedFromAccess,
    User,
)
from shared.domain.framework.effects.searchable import SearchableEffect


async def map_effect(
    effect: SearchableEffect, user_mapper: UserMapper
) -> None:
    translated_users = effect.entities_that(User).with_event(
        TranslatedFromAccess
    )

    await user_mapper.add_all(translated_users)
