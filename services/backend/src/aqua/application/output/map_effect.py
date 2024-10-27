from aqua.application.ports.mappers import DayMapper, RecordMapper, UserMapper
from aqua.domain.framework.effects.searchable import SearchableEffect
from aqua.domain.framework.entity import Created, Mutated
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import (
    TranslatedFromAccess,
    User,
)


async def map_effect(
    effect: SearchableEffect,
    *,
    user_mapper: UserMapper,
    day_mapper: DayMapper,
    record_mapper: RecordMapper,
) -> None:
    translated_users = effect.entities_that(User).with_event(
        TranslatedFromAccess
    )
    await user_mapper.add_all(translated_users)

    days = effect.entities_that(Day)
    await day_mapper.add_all(days.with_event(Created))
    await day_mapper.update_all(days.with_event(Mutated).without_event(Created))

    records = effect.entities_that(Record)
    await record_mapper.add_all(records.with_event(Created))
    await record_mapper.update_all(
        records.with_event(Mutated).without_event(Created)
    )
