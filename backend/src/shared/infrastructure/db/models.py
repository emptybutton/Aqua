from datetime import datetime
from typing import Optional

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    password_hash: Mapped[str]
    water_balance: Mapped[int]
    glass: Mapped[Optional[int]]
    weight: Mapped[Optional[int]]

    def __repr__(self) -> str:
        return f"db.User(id={self.id!r}, name={self.name!r})"


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True)
    drunk_water: Mapped[int]
    recording_time: Mapped[datetime]
    user: Mapped["User"] = relationship(back_populates="records")

    def __repr__(self) -> str:
        return f"db.Record(id={self.id!r})"
