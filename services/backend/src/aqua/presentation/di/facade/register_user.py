from dataclasses import dataclass
from uuid import UUID

from result import Err, Ok
from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases.register_user import (
    NegativeWeightKilogramsError,
    register_user,
)
from aqua.application.ports.loggers import Logger
from aqua.domain.model.core.aggregates.user.root import (
    NoWeightForSuitableWaterBalanceError,
)
from aqua.domain.model.core.vos.water_balance import (
    ExtremeWeightForSuitableWaterBalanceError,
)
from aqua.infrastructure.adapters.mappers.db.day_mapper import DBDayMapperTo
from aqua.infrastructure.adapters.mappers.db.record_mapper import (
    DBRecordMapperTo,
)
from aqua.infrastructure.adapters.mappers.db.user_mapper import DBUserMapperTo
from aqua.infrastructure.adapters.repos.db.users import DBUsers
from aqua.infrastructure.adapters.transactions.db.transaction import (
    DBTransactionForDBUsers,
)
from aqua.infrastructure.adapters.views.in_memory.registration_view_of import (
    InMemoryRegistrationViewOf,
)
from aqua.infrastructure.periphery.serializing.from_model.to_view import (
    glass_view_of,
    maybe_weight_view_of,
    target_view_of,
)
from aqua.presentation.di.containers import adapter_container


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    target_water_balance_milliliters: int
    glass_milliliters: int
    weight_kilograms: int | None


class Error(Exception): ...


class IncorrectWaterAmountError(Error): ...


class IncorrectWeightAmountError(Error): ...


class NoWeightForWaterBalanceError(Error): ...


class ExtremeWeightForWaterBalanceError(Error): ...


async def perform(
    user_id: UUID,
    water_balance_milliliters: int | None,
    glass_milliliters: int | None,
    weight_kilograms: int | None,
    *,
    session: AsyncSession,
) -> Output:
    async with adapter_container(context={AsyncSession: session}) as container:
        result = await register_user(
            user_id,
            water_balance_milliliters,
            glass_milliliters,
            weight_kilograms,
            view_of=await container.get(InMemoryRegistrationViewOf, "views"),
            users=await container.get(DBUsers, "repos"),
            transaction_for=await container.get(
                DBTransactionForDBUsers, "transactions"
            ),
            logger=await container.get(Logger, "loggers"),
            user_mapper_to=await container.get(DBUserMapperTo, "mappers"),
            record_mapper_to=await container.get(DBRecordMapperTo, "mappers"),
            day_mapper_to=await container.get(DBDayMapperTo, "mappers"),
        )

    match result:
        case Err(ExtremeWeightForSuitableWaterBalanceError()):
            raise ExtremeWeightForWaterBalanceError
        case Err(NoWeightForSuitableWaterBalanceError()):
            raise NoWeightForWaterBalanceError
        case Err(NegativeWeightKilogramsError()):
            raise IncorrectWeightAmountError
        case Err(_):
            raise IncorrectWaterAmountError
        case Ok(view):
            user = view.user

    return Output(
        user_id=user.id,
        target_water_balance_milliliters=target_view_of(user.target),
        weight_kilograms=maybe_weight_view_of(user.weight),
        glass_milliliters=glass_view_of(user.glass),
    )
