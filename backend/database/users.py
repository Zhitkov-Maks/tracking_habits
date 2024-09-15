from typing import TYPE_CHECKING, List

from sqlalchemy import String, BigInteger, Time, ForeignKey, Integer
from sqlalchemy.dialects.mysql import SMALLINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .habits import Habit


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)
    user_chat_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    password: Mapped[str] = mapped_column(String(100))
    remind: Mapped["Remind"] = relationship(back_populates="user")
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
    time: Mapped[int] = mapped_column(SMALLINT)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), index=True, unique=True
    )
    user: Mapped[User] = relationship(
        back_populates="remind",
        lazy="joined"
    )
