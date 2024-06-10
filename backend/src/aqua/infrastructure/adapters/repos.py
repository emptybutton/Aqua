from datetime import date
from typing import Optional

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncConnection

from src.aqua.application.ports import repos
from src.aqua.domain import entities, value_objects as vo
from src.shared.infrastructure.db import tables


class Users(repos.Users):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    async def add(self, user: entities.User) -> None:
        water_balance = user.target_water_balance.water.milliliters
        weight = None
        glass = None

        if user.weight is not None:
            weight = user.weight.kilograms

        if user.glass is not None:
            glass = user.glass.capacity.milliliters

        stmt = insert(tables.AquaUser).values(
            id=user.id,
            water_balance=water_balance,
            weight=weight,
            glass=glass,
        )

        await self.__connection.execute(stmt)

    async def get_by_id(self, user_id: int) -> Optional[entities.User]:
        query = (
            select(
                tables.AquaUser.id,
                tables.AquaUser.water_balance,
                tables.AquaUser.glass,
                tables.AquaUser.weight,
            )
            .where(tables.AquaUser.id == user_id)
        )
        results = await self.__connection.execute(query)
        raw_user = results.first()

        if raw_user is None:
            return None

        if raw_user.glass is None:
            glass = None
        else:
            glass = vo.Glass(vo.Water(raw_user.glass))

        weight = None if raw_user.weight is None else vo.Weight(raw_user.weight)

        water_balance = vo.WaterBalance(
            vo.Water(raw_user.water_balance)
        )

        return entities.User(
            weight=weight,
            glass=glass,
            __target_water_balance=water_balance,
            id=raw_user.id,
        )


class Records(repos.Records):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    async def add(self, record: entities.Record) -> None:
        stmt = insert(tables.Record).values(
            id=record.id,
            drunk_water=record.drunk_water.milliliters,
            recording_time=record.recording_time,
            user_id=record.user_id,
        )

        await self.__connection.execute(stmt)


class Days(repos.Days):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    async def add(self, day: entities.Day) -> None:
        stmt = insert(tables.Day).values(
            id=day.id,
            user_id=day.user_id,
            real_water_balance=day.real_water_balance.water.milliliters,
            target_water_balance=day.target_water_balance.water.milliliters,
            date_=day.date_,
            result=day.result.value,
        )

        await self.__connection.execute(stmt)

    async def get_on(self, date_: date) -> Optional[entities.Day]:
        query = (
            select(
                tables.Day.user_id,
                tables.Day.real_water_balance,
                tables.Day.target_water_balance,
                tables.Day.date_,
            ).where(tables.Day.date_ == date_)
        )

        results = await self.__connection.execute(query)
        raw_day = results.first()

        if raw_day is None:
            return raw_day

        return entities.Day(
            date_=raw_day.date_,
            user_id=raw_day.user_id,
            target_water_balance=(
                vo.WaterBalance(vo.Water(raw_day.target_water_balance))
            ),
            __real_water_balance=(
                vo.WaterBalance(vo.Water(raw_day.real_water_balance))
            ),
            id=raw_day.id,
            __result=vo.WaterBalanceStatus(raw_day.result),
        )
