from datetime import date
from typing import Optional, Any
from uuid import UUID

from sqlalchemy import select, insert, exists, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.aqua.application.ports import repos
from src.aqua.domain import entities, value_objects as vo
from src.shared.infrastructure.db import tables


class Users(repos.Users):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

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

        await self.__session.execute(stmt)

    async def get_by_id(self, user_id: UUID) -> Optional[entities.User]:
        query = (
            select(
                tables.AquaUser.id,
                tables.AquaUser.water_balance,
                tables.AquaUser.glass,
                tables.AquaUser.weight,
            )
            .where(tables.AquaUser.id == user_id)
        )
        results = await self.__session.execute(query)
        raw_user = results.first()

        if raw_user is None:
            return None

        glass = vo.Glass(vo.Water(raw_user.glass))

        weight = None if raw_user.weight is None else vo.Weight(raw_user.weight)

        water_balance = vo.WaterBalance(
            vo.Water(raw_user.water_balance)
        )

        return entities.User(
            weight=weight,
            glass=glass,
            _target_water_balance=water_balance,
            id=raw_user.id,
        )

    async def has_with_id(self, user_id: UUID) -> bool:
        query = select(exists(1).where(tables.AquaUser.id == user_id))

        result = await self.__session.scalar(query)
        return bool(result)


class Records(repos.Records):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, record: entities.Record) -> None:
        stmt = insert(tables.Record).values(
            id=record.id,
            drunk_water=record.drunk_water.milliliters,
            recording_time=record.recording_time,
            user_id=record.user_id,
        )

        await self.__session.execute(stmt)

    async def get_on(
        self,
        date_: date,
        *,
        user_id: UUID,
    ) -> tuple[entities.Record, ...]:
        query = (
            select(
                tables.Record.id,
                tables.Record.drunk_water,
                tables.Record.recording_time,
            )
            .where(
                (tables.Record.user_id == user_id)
                & (func.date(tables.Record.recording_time) == date_)
            )
        )

        results = await self.__session.execute(query)

        return tuple(self.__record_of(data, user_id) for data in results.all())

    def __record_of(
        self,
        record_data: Any,  # noqa: ANN401
        user_id: UUID,
    ) -> entities.Record:
        return entities.Record(
            id=record_data.id,
            user_id=user_id,
            drunk_water=vo.Water(record_data.drunk_water),
            _recording_time=record_data.recording_time,
        )


class Days(repos.Days):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, day: entities.Day) -> None:
        stmt = insert(tables.Day).values(
            id=day.id,
            user_id=day.user_id,
            real_water_balance=day.real_water_balance.water.milliliters,
            target_water_balance=day.target_water_balance.water.milliliters,
            date_=day.date_,
            result=day.result.value,
        )

        await self.__session.execute(stmt)

    async def get_on(
        self,
        date_: date,
        *,
        user_id: UUID,
    ) -> Optional[entities.Day]:
        query = (
            select(
                tables.Day.id,
                tables.Day.real_water_balance,
                tables.Day.target_water_balance,
                tables.Day.date_,
                tables.Day.result,
            ).where(
                (tables.Day.date_ == date_)
                & (tables.Day.user_id == user_id)
            )
            .limit(1)
        )

        results = await self.__session.execute(query)
        raw_data = results.first()

        if raw_data is None:
            return None

        return self.__day_of(raw_data, user_id, date_)

    def __day_of(
        self,
        raw_data: Any,  # noqa: ANN401
        user_id: UUID,
        date_: date,
    ) -> entities.Day:
        target = vo.WaterBalance(vo.Water(raw_data.target_water_balance))
        water_balance = vo.WaterBalance(vo.Water(raw_data.real_water_balance))
        result = vo.WaterBalanceStatus(raw_data.result)

        return entities.Day(
            id=raw_data.id,
            user_id=user_id,
            date_=date_,
            target_water_balance=target,
            _real_water_balance=water_balance,
            _result=result,
        )
