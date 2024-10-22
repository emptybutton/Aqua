from operator import call
from typing import Literal
from uuid import UUID

from result import Ok, Result

from aqua.application.output.output_effect import output_effect
from aqua.application.ports import loggers, repos, views
from aqua.application.ports.mappers import (
    DayMapper,
    RecordMapper,
    UserMapeperFactory,
)
from aqua.domain.access.entities.user import User as AccessUser
from aqua.domain.core.aggregates.user.root import User
from aqua.domain.core.vos.glass import Glass
from aqua.domain.core.vos.target import Target
from aqua.domain.core.vos.water_balance import WaterBalance
from aqua.domain.primitives.vos.water import Water
from aqua.domain.primitives.vos.weight import Weight
from shared.application.ports.mappers import MapperFactory
from shared.application.ports.transactions import TransactionFactory
from shared.domain.framework.effects.searchable import SearchableEffect
from shared.domain.framework.result import frm, ok


async def register_user[UsersT: repos.Users, ViewT](
    user_id: UUID,
    target_water_balance_milliliters: int | None,
    glass_milliliters: int | None,
    weight_kilograms: int | None,
    *,
    view_of: views.RegistrationViewOf[ViewT],
    users: UsersT,
    transaction_for: TransactionFactory[UsersT],
    logger: loggers.Logger,
    user_mapper_to: UserMapeperFactory[UsersT],
    day_mapper_to: MapperFactory[UsersT, DayMapper],
    record_mapper_to: MapperFactory[UsersT, RecordMapper],
) -> Result[
    ViewT,
    Literal[
        "extreme_weight_for_suitable_water_balance",
        "no_weight_for_suitable_water_balance",
        "negative_target_water_balance_milliliters",
        "negative_glass_milliliters",
        "negative_weight_kilograms",
    ]
]:
    if target_water_balance_milliliters is None:
        target_result = Ok(None)
    else:
        target_result = (
            Water
            .with_(milliliters=target_water_balance_milliliters)
            .map_err(lambda _: "negative_target_water_balance_milliliters")
            .map(lambda water: Target(water_balance=WaterBalance(water=water)))
        )

    if weight_kilograms is None:
        weight_result = Ok(None)
    else:
        weight_result = (
            Weight.with_(kilograms=weight_kilograms)
            .map_err(lambda _: "negative_weight_kilograms")
        )

    if glass_milliliters is None:
        glass_result = Ok(None)
    else:
        glass_result = (
            Water
            .with_(milliliters=glass_milliliters)
            .map_err(lambda _: "negative_glass_milliliters")
            .map(lambda water: Glass(capacity=water))
        )

    async with transaction_for(users):
        user = await users.find_with_id(user_id)

        if user is not None:
            await logger.log_registered_user_registration(user)
            return Ok(view_of(user))

        effect = SearchableEffect()

        @call
        @frm(target_result)
        @frm(glass_result)
        @frm(weight_result)
        @ok
        def result(weight: Weight, glass: Glass, target: Target, /) -> User:
            return User.translated_from(
                access_user=AccessUser(id=user_id),
                weight=weight,
                glass=glass,
                target=target,
                effect=effect,
            )

        await result.map_async(lambda _: output_effect(
            effect,
            user_mapper=user_mapper_to(users),
            day_mapper=day_mapper_to(users),
            record_mapper=record_mapper_to(users),
            logger=logger,
        ))

        return result.map(view_of)
