from datetime import UTC, datetime
from typing import Literal
from uuid import UUID

from result import Err, Ok, Result

from aqua.application.output.output_effect import output_effect
from aqua.application.ports import loggers, repos, views
from aqua.application.ports.mappers import (
    DayMapper,
    RecordMapper,
    UserMapeperFactory,
)
from aqua.domain.primitives.vos.time import Time
from aqua.domain.primitives.vos.water import Water
from shared.application.ports.mappers import MapperFactory
from shared.application.ports.transactions import TransactionFactory
from shared.domain.framework.effects.searchable import SearchableEffect


async def write_water[UsersT: repos.Users, ViewT](
    user_id: UUID,
    milliliters: int | None,
    *,
    view_of: views.WritingViewOf[ViewT],
    users: UsersT,
    transaction_for: TransactionFactory[UsersT],
    logger: loggers.Logger,
    user_mapper_in: UserMapeperFactory[UsersT],
    day_mapper_in: MapperFactory[UsersT, DayMapper],
    record_mapper_in: MapperFactory[UsersT, RecordMapper],
) -> Result[ViewT, Literal["no_user", "negative_water_amount"]]:
    current_time = Time.with_(datetime_=datetime.now(UTC)).unwrap()

    if milliliters is None:
        water = None
    else:
        match Water(milliliters=milliliters):
            case Ok(value):
                water = value
            case Err(_) as result:
                return result

    async with transaction_for(users):
        user = await users.user_with_id(user_id)

        if user is None:
            return Err("no_user")

        effect = SearchableEffect()
        output = user.write_water(
            water, current_time=current_time, effect=effect
        )

        await output_effect(
            effect,
            user_mapper=user_mapper_in(users),
            day_mapper=day_mapper_in(users),
            record_mapper=record_mapper_in(users),
            logger=logger,
        )

        return view_of(user=user, output=output)
