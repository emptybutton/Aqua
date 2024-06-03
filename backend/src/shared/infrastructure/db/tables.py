from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class AuthUser(Base):
    __tablename__ = "auth_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password_hash: Mapped[str]

    def __repr__(self) -> str:
        return f"db.AuthUser(id={self.id!r}, name={self.name!r})"


class AquaUser(Base):
    __tablename__ = "aqua_users"

    id: Mapped[int] = mapped_column(
        ForeignKey("auth_users.id"),
        primary_key=True,
    )
    water_balance: Mapped[int]
    glass: Mapped[Optional[int]]
    weight: Mapped[Optional[int]]

    def __repr__(self) -> str:
        return f"db.AquaUser(id={self.id!r})"


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True)
    drunk_water: Mapped[int]
    recording_time: Mapped[datetime]
    user: Mapped["AquaUser"] = relationship(back_populates="records")

    def __repr__(self) -> str:
        return f"db.Record(id={self.id!r})"
