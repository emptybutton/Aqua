from aqua.application import output as aqua
from aqua.application.ports.loggers import Logger
from aqua.application.ports.mappers import DayMapper, RecordMapper, UserMapeper
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from shared.application import output as shared
from shared.domain.framework.effects.searchable import SearchableEffect


async def output_effect(
    effect: SearchableEffect,
    *,
    user_mapper: UserMapeper,
    day_mapper: DayMapper,
    record_mapper: RecordMapper,
    logger: Logger,
) -> None:
    await aqua.log_effect.log_effect(effect, logger)
    await aqua.map_effect.map_effect(effect, user_mapper)
    await shared.map_effect.map_effect(effect, shared.map_effect.Mappers(
        (Day, day_mapper),
        (Record, record_mapper),
    ))
