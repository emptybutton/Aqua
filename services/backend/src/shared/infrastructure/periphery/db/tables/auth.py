from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    String,
    Table,
    Uuid,
)

from shared.infrastructure.periphery.db.tables.metadata import metadata


account_table = Table(
    "accounts",
    metadata,
    Column("id", Uuid, primary_key=True, nullable=False),
    Column("password_hash", String, nullable=False),
    schema="auth",
)

account_name_table = Table(
    "account_names",
    metadata,
    Column("id", Uuid, primary_key=True, nullable=False),
    Column("account_id", Uuid, nullable=False),
    Column("text", String, nullable=False),
    Column("is_current", Boolean, nullable=False),
    schema="auth",
)

account_name_taking_time_table = Table(
    "account_name_taking_times",
    metadata,
    Column("id", Uuid, primary_key=True, nullable=False),
    Column("account_name_id", Uuid, nullable=False),
    Column("time", DateTime(timezone=True), nullable=False),
    schema="auth",
)

session_table = Table(
    "sessions",
    metadata,
    Column("id", Uuid, primary_key=True, nullable=False),
    Column("account_id", Uuid, nullable=False),
    Column("start_time", DateTime(timezone=True), nullable=True),
    Column("end_time", DateTime(timezone=True), nullable=False),
    Column("is_cancelled", Boolean, nullable=True),
    Column("leader_session_id", Uuid, nullable=True),
    schema="auth",
)
