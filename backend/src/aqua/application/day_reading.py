from dataclasses import dataclass
from datetime import date

from src.aqua.domain import entities, value_objects
from src.aqua.application.ports import repos


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    user_id: int
    target_water_balance: int
    real_water_balance: int
    result_code: int


class BaseError(Exception): ...


class NoUserError(BaseError): ...


async def read_day(
    user_id: int,
    date_: date,
    *,
    users: repos.Users,
    past_days: repos.PastDays,
    today_records: repos.TodayRecords,
) -> OutputDTO:
    user = await users.get_by_id(user_id)

    if user is None:
        raise NoUserError()

    day = await past_days.get_on(date_, user_id=user.id)

    if day is not None:
        return OutputDTO(
            user_id=day.user_id,
            target_water_balance=day.target_water_balance.water.milliliters,
            real_water_balance=day.real_water_balance.water.milliliters,
            result_code=day.result.value,
        )

    records = await today_records.get_all_with_user_id(user.id)

    water_balance = entities.water_balance_from(*records)
    status = value_objects.status_of(
        water_balance,
        target=user.target_water_balance,
    )

    return OutputDTO(
        user_id=user.id,
        target_water_balance=user.target_water_balance.water.milliliters,
        real_water_balance=water_balance.water.milliliters,
        result_code=status.value,
    )
