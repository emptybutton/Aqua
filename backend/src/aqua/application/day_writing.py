from datetime import datetime, UTC, timedelta
from typing import TypeVar

from src.aqua.application.ports import repos
from src.aqua.domain import entities
from src.shared.application.ports import uows


_TodayRecordsT = TypeVar("_TodayRecordsT", bound=repos.TodayRecords)
_UsersWithTodayRecordsT = TypeVar(
    "_UsersWithTodayRecordsT",
    bound=repos.UsersWithTodayRecords,
)
_PastDaysT = TypeVar("_PastDaysT", bound=repos.PastDays)


async def write_day(  # noqa: PLR0913
    *,
    users_with_today_records: _UsersWithTodayRecordsT,
    today_records: _TodayRecordsT,
    past_days: _PastDaysT,
    user_uow_for: uows.UoWFactory[_UsersWithTodayRecordsT, entities.User],
    today_record_uow_for: uows.UoWFactory[_TodayRecordsT, entities.Record],
    past_day_uow_for: uows.UoWFactory[_PastDaysT, entities.Day],
) -> None:
    yesterday_date = datetime.now(UTC).date() - timedelta(days=1)

    user_uow = user_uow_for(users_with_today_records)
    today_record_uow = today_record_uow_for(today_records)
    past_day_uow = past_day_uow_for(past_days)

    async with user_uow, today_record_uow:
        for user in await users_with_today_records.pop_all():
            records = await today_records.pop_all_with_user_id(user.id)
            water_balance = entities.water_balance_from(*records)

            yesterday = entities.Day(
                user_id=user.id,
                target_water_balance=user.target_water_balance,
                __real_water_balance=water_balance,
                date_=yesterday_date,
            )

            async with past_day_uow:
                past_day_uow.register_new(yesterday)
                await past_days.add(yesterday)
