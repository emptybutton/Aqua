from datetime import date
from typing import Any, Iterable
from uuid import UUID

from sqlalchemy import Row, desc, func, select

from aqua.application.ports.views import DayViewFrom
from aqua.infrastructure.adapters.repos.db.users import DBUsers
from aqua.infrastructure.periphery.serializing.from_table_attribute.to_view import (  # noqa: E501
    old_result_view_of,
)
from aqua.infrastructure.periphery.views.db.day_view import (
    DBDayView,
    DBDayViewRecordData,
    empty_db_day_view_with,
)
from shared.infrastructure.periphery.db.tables import aqua as tables


class DBDayViewFrom(DayViewFrom[DBUsers, DBDayView]):
    async def __call__(
        self, db_users: DBUsers, *, user_id: UUID, date_: date
    ) -> DBDayView:
        stmt = select(
            tables.day_table.c.target.label("day_target"),
            tables.day_table.c.water_balance.label("day_water_balance"),
            tables.day_table.c.result.label("day_result"),
            tables.day_table.c.correct_result.label("day_correct_result"),
            tables.day_table.c.pinned_result.label("day_pinned_result"),
            tables.record_table.c.id.label("record_id"),
            tables.record_table.c.drunk_water.label("record_drunk_water"),
            tables.record_table.c.recording_time.label("record_recording_time"),
        ).outerjoin_from(
            tables.day_table,
            tables.record_table,
            (
                (tables.record_table.c.user_id == user_id)
                & (func.date(tables.record_table.c.recording_time) == date_)
            )
        ).where(
            (tables.day_table.c.user_id == user_id)
            & (tables.day_table.c.date_ == date_)
        ).order_by(
            desc(tables.record_table.c.recording_time)
        )

        result = await db_users.connection.execute(stmt)
        rows = result.all()

        if len(rows) == 0:
            return empty_db_day_view_with(user_id=user_id, date_=date_)

        row = rows[0]

        return DBDayView(
            user_id=user_id,
            date_=date_,
            target_water_balance_milliliters=row.day_target,
            water_balance_milliliters=row.day_water_balance,
            result_code=old_result_view_of(row.day_result),
            correct_result_code=old_result_view_of(row.day_correct_result),
            pinned_result_code=old_result_view_of(row.day_pinned_result),
            records=tuple(_records_from(rows)),
        )


def _records_from(rows: Iterable[Row[Any]]) -> Iterable[DBDayViewRecordData]:
    for row in rows:
        yield DBDayViewRecordData(
            record_id=row.record_id,
            drunk_water_milliliters=row.record_drunk_water,
            recording_time=row.record_recording_time,
        )
