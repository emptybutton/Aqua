from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import AsyncIterator
from uuid import UUID

from result import Err, Ok, Result

from aqua.application.output.output_effect import output_effect
from aqua.application.ports import loggers, repos, views
from aqua.application.ports.mappers import (
    DayMapperTo,
    RecordMapperTo,
    UserMapperTo,
)
from aqua.application.ports.transactions import TransactionFor
from aqua.domain.framework.effects.searchable import SearchableEffect
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import (
    NegativeWaterAmountError,
    Water,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class NoUserError: ...


@asynccontextmanager
async def write_water[UsersT: repos.Users, ViewT](
    user_id: UUID,
    milliliters: int | None,
    *,
    view_of: views.WritingViewOf[ViewT],
    users: UsersT,
    transaction_for: TransactionFor[UsersT],
    logger: loggers.Logger,
    user_mapper_to: UserMapperTo[UsersT],
    day_mapper_to: DayMapperTo[UsersT],
    record_mapper_to: RecordMapperTo[UsersT],
) -> AsyncIterator[Result[ViewT, NoUserError | NegativeWaterAmountError]]:
    current_time = Time.with_(datetime_=datetime.now(UTC)).unwrap()

    if milliliters is None:
        water = None
    else:
        match Water.with_(milliliters=milliliters):
            case Ok(value):
                water = value
            case Err(_) as result:
                yield result
                return

    async with transaction_for(users):
        user = await users.user_with_id(user_id)

        if user is None:
            yield Err(NoUserError())
            return

        effect = SearchableEffect()
        output = user.write_water(
            water, current_time=current_time, effect=effect
        )

        await output_effect(
            effect,
            user_mapper=user_mapper_to(users),
            day_mapper=day_mapper_to(users),
            record_mapper=record_mapper_to(users),
            logger=logger,
        )

        yield Ok(view_of(user=user, output=output))
