from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application import ports
from aqua.application.cases import register_user
from aqua.domain import entities
from aqua.domain import value_objects as vos
from aqua.infrastructure.adapters import repos
from aqua.presentation.di.containers import adapter_container
from shared.infrastructure.adapters.transactions import DBTransactionFactory


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    target_water_balance_milliliters: int
    glass_milliliters: int
    weight_kilograms: int | None


IncorrectWaterAmountError: TypeAlias = vos.Water.IncorrectAmountError

IncorrectWeightAmountError: TypeAlias = vos.Weight.IncorrectAmountError

NoWeightForWaterBalanceError: TypeAlias = (
    entities.User.NoWeightForSuitableWaterBalanceError
)

ExtremeWeightForWaterBalanceError: TypeAlias = (
    vos.WaterBalance.ExtremeWeightForSuitableWaterBalanceError
)

Error: TypeAlias = (
    IncorrectWaterAmountError
    | IncorrectWeightAmountError
    | NoWeightForWaterBalanceError
    | ExtremeWeightForWaterBalanceError
)


async def perform(
    user_id: UUID,
    water_balance_milliliters: int | None,
    glass_milliliters: int | None,
    weight_kilograms: int | None,
    *,
    session: AsyncSession,
) -> Output:
    async with adapter_container(context={AsyncSession: session}) as container:
        user = await register_user.perform(
            user_id,
            water_balance_milliliters,
            glass_milliliters,
            weight_kilograms,
            users=await container.get(repos.DBUsers, "repos"),
            logger=await container.get(ports.loggers.Logger, "loggers"),
            transaction_for=await container.get(
                DBTransactionFactory, "transactions"
            ),
        )

    weight_kilograms = None if user.weight is None else user.weight.kilograms

    return Output(
        user_id=user.id,
        target_water_balance_milliliters=user.target.water.milliliters,
        weight_kilograms=weight_kilograms,
        glass_milliliters=user.glass.capacity.milliliters,
    )
