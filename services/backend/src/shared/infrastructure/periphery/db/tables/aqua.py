from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    Table,
    Uuid,
)

from shared.infrastructure.periphery.db.tables.metadata import metadata


user_table = Table(
    "users",
    metadata,
    Column("id", Uuid, primary_key=True, nullable=False),
    Column("water_balance", Integer, nullable=False),
    Column("glass", Integer, nullable=False),
    Column("weight", Integer, nullable=True),
    schema="aqua",
)

record_table = Table(
    "records",
    metadata,
    Column("id", Uuid, primary_key=True, nullable=False),
    Column("user_id", Uuid, nullable=False),
    Column("drunk_water", Integer, nullable=False),
    Column("recording_time", DateTime(timezone=True), nullable=False),
    Column("is_accidental", Boolean, nullable=True),
    schema="aqua",
)

day_table = Table(
    "days",
    metadata,
    Column("id", Uuid, primary_key=True, nullable=False),
    Column("user_id", Uuid, nullable=False),
    Column("real_water_balance", Integer, nullable=False),
    Column("target_water_balance", Integer, nullable=False),
    Column("date_", Date, nullable=False),
    Column("result", Integer, nullable=False),
    Column("is_result_pinned", Boolean, nullable=True),
    schema="aqua",
)
