from datetime import date, datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True)

    def __repr__(self) -> str:
        return f"db.{type(self).__name__}(id={self.id!r})"


class AuthUser(Base):
    __tablename__ = "auth_users"

    name: Mapped[str]
    password_hash: Mapped[str]

    def __repr__(self) -> str:
        return f"db.AuthUser(id={self.id!r}, name={self.name!r})"


class PreviousUsername(Base):
    __tablename__ = "auth_previous_usernames"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("auth_users.id"))
    username: Mapped[str]


class Session(Base):
    __tablename__ = "sessions"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("auth_users.id"))
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expiration_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AquaUser(Base):
    __tablename__ = "aqua_users"

    id: Mapped[UUID] = mapped_column(
        ForeignKey("auth_users.id"), primary_key=True
    )
    water_balance: Mapped[int]
    glass: Mapped[int]
    weight: Mapped[int | None]
    records: Mapped[list["Record"]] = relationship(back_populates="user")


class Record(Base):
    __tablename__ = "records"

    drunk_water: Mapped[int]
    recording_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("aqua_users.id"))
    user: Mapped["AquaUser"] = relationship(back_populates="records")


class Day(Base):
    __tablename__ = "days"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("aqua_users.id"))
    real_water_balance: Mapped[int]
    target_water_balance: Mapped[int]
    date_: Mapped[date]
    result: Mapped[int]
    is_result_pinned: Mapped[bool | None]
