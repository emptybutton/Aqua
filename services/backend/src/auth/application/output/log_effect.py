from auth.application.ports.loggers import Logger
from auth.domain.models.access.aggregates import account as _account
from shared.application.adapters.effects import IndexedEffect


async def log_effect(effect: IndexedEffect, logger: Logger) -> None:
    extended_sessions = effect.entities_with_event(
        entity_type=_account.internal.entities.session.Session,
        event_type=_account.internal.entities.session.Extended,
    )

    replaced_sessions = effect.entities_with_event(
        entity_type=_account.internal.entities.session.Session,
        event_type=_account.internal.entities.session.Replaced,
    )

    # cancelled_sessions = effect.entities_with_event(
    #     entity_type=_account.internal.entities.session.Session,
    #     event_type=_account.internal.entities.session.Cancelled,
    # )

    for extended_session in extended_sessions:
        await logger.log_session_extension(extended_session)

    for replaced_session in replaced_sessions:
        await logger.log_replaced_session(replaced_session)

    # for cancelled_session in cancelled_sessions:
    #     await logger.log_cancelled_session(cancelled_session)
