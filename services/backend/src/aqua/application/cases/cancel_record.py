from typing import Literal
from uuid import UUID

from result import Err, Result

from aqua.application.output.output_effect import output_effect
from aqua.application.ports import loggers, repos, views
from aqua.application.ports.mappers import (
    DayMapper,
    RecordMapper,
    UserMapeperFactory,
)
from shared.application.ports.mappers import MapperFactory
from shared.application.ports.transactions import TransactionFactory
from shared.domain.framework.effects.searchable import SearchableEffect


async def cancel_record[UsersT: repos.Users, ViewT](
    user_id: UUID,
    record_id: UUID,
    *,
    view_of: views.CancellationViewOf[ViewT],
    users: UsersT,
    transaction_for: TransactionFactory[UsersT],
    logger: loggers.Logger,
    user_mapper_in: UserMapeperFactory[UsersT],
    day_mapper_in: MapperFactory[UsersT, DayMapper],
    record_mapper_in: MapperFactory[UsersT, RecordMapper],
) -> Result[
    ViewT,
    Literal[
        "no_user",
        "no_record_to_cancel",
        "cancelled_record_to_cancel",
        "no_record_day_to_cancel",
    ],
]:
    async with transaction_for(users):
        user = await users.user_with_id(user_id)

        if not user:
            return Err("no_user")

        effect = SearchableEffect()
        result = user.cancel_record(record_id=record_id, effect=effect)

        if result.err() == "no_record_day_to_cancel":
            await logger.log_record_without_day()

        await result.map_async(lambda _: output_effect(
            effect,
            user_mapper=user_mapper_in(users),
            day_mapper=day_mapper_in(users),
            record_mapper=record_mapper_in(users),
            logger=logger,
        ))

        return result.map(lambda output: view_of(user=user, output=output))
