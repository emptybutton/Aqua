from datetime import date, datetime
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from shared.infrastructure.periphery.db.tables.metadata import metadata


class Base(DeclarativeBase):
    __table_args__ = {"schema": "aqua"}  # noqa: RUF012
    metadata = metadata

    id: Mapped[UUID] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f"db.{type(self).__name__}(id={self.id!r})"


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    water_balance: Mapped[int]
    glass: Mapped[int]
    weight: Mapped[int | None]


class Record(Base):
    __tablename__ = "records"

    drunk_water: Mapped[int]
    recording_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[UUID]
    is_accidental: Mapped[bool | None]


class Day(Base):
    __tablename__ = "days"

    user_id: Mapped[UUID]
    real_water_balance: Mapped[int]
    target_water_balance: Mapped[int]
    date_: Mapped[date]
    result: Mapped[int]
    is_result_pinned: Mapped[bool | None]
