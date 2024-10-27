from aqua.application.ports.loggers import Logger
from aqua.domain.framework.effects.searchable import SearchableEffect
from aqua.domain.framework.entity import Created, Mutated
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Cancelled,
    Record,
)
from aqua.domain.model.core.aggregates.user.root import (
    TranslatedFromAccess,
    User,
)


async def log_effect(effect: SearchableEffect, logger: Logger) -> None:
    translated_users = effect.entities_that(User).with_event(
        TranslatedFromAccess
    )

    days = effect.entities_that(Day)
    created_days = days.with_event(Created)
    mutated_days = days.with_event(Mutated).without_event(Created)

    records = effect.entities_that(Record)
    created_records = records.with_event(Created)
    cancelled_records = records.with_event(Cancelled).without_event(Created)

    for translated_user in translated_users:
        await logger.log_registered_user(translated_user)

    for created_day in created_days:
        await logger.log_new_day(created_day)

    for mutated_day in mutated_days:
        await logger.log_new_day_state(mutated_day)

    for created_record in created_records:
        await logger.log_new_record(created_record)

    for cancelled_record in cancelled_records:
        await logger.log_record_cancellation(record=cancelled_record)
