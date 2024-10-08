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
