from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    MetaData,
    String,
    Table,
    Uuid,
)


metadata = MetaData()

account_table = Table(
    "users",
    metadata,
    Column("id", Uuid, primary_key=True, nullable=False),
    Column("name", String, nullable=False),
    Column("password_hash", String, nullable=False),
    schema="auth",
)

previous_username_table = Table(
    "previous_usernames",
    metadata,
    Column("id", Uuid, primary_key=True, nullable=False),
    Column("user_id", Uuid, nullable=False),
    Column("username", String, nullable=False),
    Column("change_time", DateTime(timezone=True), nullable=True),
    schema="auth",
)

session_table = Table(
    "sessions",
    metadata,
    Column("id", Uuid, primary_key=True, nullable=False),
    Column("user_id", Uuid, nullable=False),
    Column("start_time", DateTime(timezone=True), nullable=True),
    Column("expiration_date", DateTime(timezone=True), nullable=False),
    Column("cancelled", Boolean, nullable=True),
    Column("next_session_id", Uuid, nullable=True),
    schema="auth",
)

aqua_user_table = Table(
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
