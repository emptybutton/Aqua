from auth.application.ports.loggers import Logger
from auth.domain.framework.effects.searchable import SearchableEffect
from auth.domain.models.access.aggregates import account as _account


async def log_effect(effect: SearchableEffect, logger: Logger) -> None:
    sessoins = effect.entities_that(_account.internal.entities.session.Session)

    extended_sessions = sessoins.with_event(
        _account.internal.entities.session.Extended
    )

    replaced_sessions = sessoins.with_event(
        _account.internal.entities.session.Replaced
    )

    cancelled_sessions = sessoins.with_event(
        _account.internal.entities.session.Cancelled
    )

    for extended_session in extended_sessions:
        await logger.log_session_extension(extended_session)

    for replaced_session in replaced_sessions:
        await logger.log_replaced_session(replaced_session)

    for cancelled_session in cancelled_sessions:
        await logger.log_cancelled_session(cancelled_session)
