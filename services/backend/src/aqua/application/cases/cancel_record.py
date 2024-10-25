from dataclasses import dataclass
from uuid import UUID

from result import Err, Result

from aqua.application.output.output_effect import output_effect
from aqua.application.ports import loggers, repos, views
from aqua.application.ports.mappers import (
    DayMapperTo,
    RecordMapperTo,
    UserMapperTo,
)
from aqua.application.ports.transactions import TransactionFor
from aqua.domain.framework.effects.searchable import SearchableEffect
from aqua.domain.framework.fp.env import Env
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    CancelledRecordToCancelError,
)
from aqua.domain.model.core.aggregates.user.root import (
    NoRecordDayToCancelError,
    NoRecordToCancelError,
    RecordContext,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class NoUserError: ...


async def cancel_record[UsersT: repos.Users, ViewT](
    user_id: UUID,
    record_id: UUID,
    *,
    view_of: views.CancellationViewOf[ViewT],
    users: UsersT,
    transaction_for: TransactionFor[UsersT],
    logger: loggers.Logger,
    user_mapper_to: UserMapperTo[UsersT],
    day_mapper_to: DayMapperTo[UsersT],
    record_mapper_to: RecordMapperTo[UsersT],
) -> Result[
    ViewT,
    (
        NoUserError
        | NoRecordToCancelError
        | CancelledRecordToCancelError
        | NoRecordDayToCancelError
    ),
]:
    async with transaction_for(users):
        user = await users.user_with_id(user_id)

        if not user:
            return Err(NoUserError())

        effect = SearchableEffect()
        result = user.cancel_record(record_id=record_id, effect=effect)

        match result:
            case Err(Env(RecordContext(record), NoRecordDayToCancelError())):
                await logger.log_record_without_day(record)

        await result.map_async(
            lambda _: output_effect(
                effect,
                user_mapper=user_mapper_to(users),
                day_mapper=day_mapper_to(users),
                record_mapper=record_mapper_to(users),
                logger=logger,
            )
        )

        return result.map(
            lambda output: view_of(user=user, output=output)
        ).map_err(lambda env: env.value)
