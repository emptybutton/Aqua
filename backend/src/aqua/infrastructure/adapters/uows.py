from sqlalchemy import update, Update
from sqlalchemy.ext.asyncio import AsyncSession

from aqua.domain import entities
from shared.infrastructure.adapters import uows
from shared.infrastructure.db import tables


class DirtyDayUoW(uows.DBUoW[entities.Day]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)
        self.__dirty_days: list[entities.Day] = list()

    def register_dirty(self, day: entities.Day) -> None:
        self.__dirty_days.append(day)

    async def _finish_work(self) -> None:
        for dirty_day in self.__dirty_days:
            await self._session.execute(self.__updating_stmt_for(dirty_day))

    @staticmethod
    def __updating_stmt_for(day: entities.Day) -> Update:
        return (
            update(tables.Day)
            .where(tables.Day.id == day.id)
            .values(
                user_id=day.user_id,
                real_water_balance=day.water_balance.water.milliliters,
                target_water_balance=day.target.water.milliliters,
                date_=day.date_,
                result=day.result.value,
                is_result_pinned=day.is_result_pinned,
            )
        )
