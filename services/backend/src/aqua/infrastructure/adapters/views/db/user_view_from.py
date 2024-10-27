from datetime import date
from typing import Any, Iterable
from uuid import UUID

from sqlalchemy import Row, desc, func, select

from aqua.application.ports.views import DayViewFrom
from aqua.infrastructure.adapters.repos.db.users import DBUsers
from aqua.infrastructure.periphery.serializing.from_table_attribute.to_view import (  # noqa: E501
    old_result_view_of,
)
from aqua.infrastructure.periphery.views.db.user_view import (
    DBUserView,
    DBUserViewData,
    DBUserViewRecordData,
)
from shared.infrastructure.periphery.db.tables import aqua as tables


class DBUserViewFrom(DayViewFrom[DBUsers, DBUserView]):
    async def __call__(
        self, db_users: DBUsers, *, user_id: UUID, date_: date
    ) -> DBUserView:
        stmt = (
            select(
                tables.user_table.c.glass.label("user_glass"),
                tables.user_table.c.weight.label("user_weight"),
                tables.day_table.c.target.label("day_target"),
                tables.day_table.c.water_balance.label("day_water_balance"),
                tables.day_table.c.result.label("day_result"),
                tables.day_table.c.correct_result.label("day_correct_result"),
                tables.day_table.c.pinned_result.label("day_pinned_result"),
                tables.record_table.c.id.label("record_id"),
                tables.record_table.c.drunk_water.label("record_drunk_water"),
                tables.record_table.c.recording_time.label(
                    "record_recording_time"
                ),
            )
            .join_from(
                tables.user_table,
                tables.day_table,
                (
                    (tables.user_table.c.id == user_id)
                    & (tables.day_table.c.user_id == user_id)
                    & (tables.day_table.c.date_ == date_)
                ),
            )
            .outerjoin(
                tables.record_table,
                (
                    (tables.record_table.c.user_id == user_id)
                    & (func.date(tables.record_table.c.recording_time) == date_)
                    & (~tables.record_table.c.is_cancelled)
                ),
            )
            .order_by(desc(tables.record_table.c.recording_time))
        )

        result = await db_users.connection.execute(stmt)
        rows = result.all()

        if len(rows) == 0:
            return None

        row = rows[0]

        return DBUserViewData(
            user_id=user_id,
            glass_milliliters=row.user_glass,
            weight_kilograms=row.user_weight,
            date_=date_,
            target_water_balance_milliliters=row.day_target,
            water_balance_milliliters=row.day_water_balance,
            result_code=old_result_view_of(row.day_result),
            correct_result_code=old_result_view_of(row.day_correct_result),
            pinned_result_code=old_result_view_of(row.day_pinned_result),
            records=tuple(_records_from(rows)),
        )


def _records_from(rows: Iterable[Row[Any]]) -> Iterable[DBUserViewRecordData]:
    for row in rows:
        yield DBUserViewRecordData(
            record_id=row.record_id,
            drunk_water_milliliters=row.record_drunk_water,
            recording_time=row.record_recording_time,
        )
