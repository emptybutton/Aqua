from types import TracebackType
from typing import Optional, Type

from sqlalchemy import update, Update
from sqlalchemy.ext.asyncio import AsyncConnection

from src.aqua.domain import entities
from src.shared.infrastructure.adapters import uows
from src.shared.infrastructure.db import tables


class DirtyDayUoW(uows.FakeUoW[entities.Day]):
    def __init__(self, connetion: AsyncConnection) -> None:
        self.__connetion = connetion
        self.__dirty_days: list[entities.Day] = list()

    def register_dirty(self, day: entities.Day) -> None:
        self.__dirty_days.append(day)

    async def __aexit__(
        self,
        error_type: Optional[Type[BaseException]],
        error: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        if error is not None:
            return False

        for dirty_day in self.__dirty_days:
            await self.__connetion.execute(self.__updating_stmt_for(dirty_day))

        return True

    @staticmethod
    def __updating_stmt_for(day: entities.Day) -> Update:
        return update(tables.Day).values(
            user_id=day.user_id,
            real_water_balance=day.real_water_balance.water.milliliters,
            target_water_balance=day.target_water_balance.water.milliliters,
            date_=day.date_,
            result=day.result.value,
        )
