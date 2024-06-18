from uuid import UUID
from dataclasses import dataclass
from datetime import date

from src.aqua.domain import entities
from src.aqua.application.ports import repos


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    user_id: UUID
    target_water_balance: int
    real_water_balance: int
    result_code: int


class BaseError(Exception): ...


class NoUserError(BaseError): ...


async def read_day(
    user_id: UUID,
    date_: date,
    *,
    users: repos.Users,
    days: repos.Days,
) -> OutputDTO:
    user = await users.get_by_id(user_id)

    if user is None:
        raise NoUserError()

    day = await days.get_on(date_, user_id=user.id)

    if day is None:
        day = entities.Day(
            user_id=user.id,
            target_water_balance=user.target_water_balance,
        )

    return OutputDTO(
        user_id=day.user_id,
        target_water_balance=day.target_water_balance.water.milliliters,
        real_water_balance=day.real_water_balance.water.milliliters,
        result_code=day.result.value,
    )
