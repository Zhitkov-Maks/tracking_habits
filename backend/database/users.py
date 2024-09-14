from typing import TYPE_CHECKING

from sqlalchemy import String, BigInteger, Time, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .habits import Habit


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)
    user_chat_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    password: Mapped[str] = mapped_column(String(100))

    habits: Mapped[list["Habit"]] = relationship(
        "Habit",
        back_populates="user",
        lazy="select",
        cascade="all, delete",
    )

    def __str__(self):
        return f"username={self.username}, chat_id={self.user_chat_id}"

    def __repr__(self):
        return str(self)


class Remind(Base):
    time: Mapped[Time] = mapped_column(Time)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)