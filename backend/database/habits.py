from datetime import datetime as dt
from typing import List

from sqlalchemy import (
    String,
    Text,
    Boolean,
    ForeignKey,
    Integer,
    Date,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import User
from .base import Base


class Habit(Base):
    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    start_date: Mapped[Date] = mapped_column(
        Date,
        default=dt.now().date(),
        server_default=str(dt.now().date())
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    number_of_days: Mapped[int] = mapped_column(
        Integer, default=21, server_default="21"
    )
    user: Mapped[List["User"]] = relationship(
        "User",
        back_populates="habits",
        lazy="select"
    )
    tracking: Mapped[list["Tracking"]] = relationship(
        "Tracking",
        back_populates="habit",
        cascade="all, delete",
        lazy="select"
    )

    def __str__(self):
        return (f"title={self.title}, "
                f"body={self.body}, "
                f"start_date={self.start_date}")

    def __repr__(self):
        return str(self)


class Tracking(Base):
    __table_args__ = (
        UniqueConstraint(
            "habit_id",
            "date",
        ),
    )
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    date: Mapped[Date] = mapped_column(
        Date,
        default=dt.now().date(),
        server_default=str(dt.now().date())
    )
    habit_id: Mapped[int] = mapped_column(ForeignKey("habits.id"), index=True)
    habit: Mapped[List["Habit"]] = relationship(
        "Habit",
        back_populates="tracking",
        lazy="select"
    )
