from aqua.application.output.log_effect import log_effect
from aqua.application.output.map_effect import map_effect
from aqua.application.ports.loggers import Logger
from aqua.application.ports.mappers import DayMapper, RecordMapper, UserMapper
from aqua.domain.framework.effects.searchable import SearchableEffect


async def output_effect(
    effect: SearchableEffect,
    *,
    user_mapper: UserMapper,
    day_mapper: DayMapper,
    record_mapper: RecordMapper,
    logger: Logger,
) -> None:
    await log_effect(effect, logger)
    await map_effect(
        effect,
        user_mapper=user_mapper,
        day_mapper=day_mapper,
        record_mapper=record_mapper,
    )
