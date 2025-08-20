from datetime import datetime as dt, timedelta
from typing import List

from sqlalchemy import (
    String,
    Text,
    Boolean,
    ForeignKey,
    Integer,
    Date,
    UniqueConstraint,
    DateTime
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
    end_date: Mapped[Date] = mapped_column(
        Date,
        default=dt.now().date() + timedelta(days=21),
        server_default=str(dt.now().date() + timedelta(days=21))
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
    comments: Mapped[list["Comment"]] = relationship(
        back_populates="habit",
        cascade="all, delete-orphan"
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


class Comment(Base):
    __tablename__ = 'comments'
    body: Mapped[str] = mapped_column(String, nullable=False)
    habit_id: Mapped[int] = mapped_column(
        ForeignKey('habits.id'), nullable=False
    )
    habit: Mapped["Habit"] = relationship(back_populates="comments")
    created_at: Mapped[dt] = mapped_column(
        DateTime,
        default=dt.utcnow,
        nullable=False
    )
