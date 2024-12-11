from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.mysql import SMALLINT, BIGINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .habits import Habit


class User(Base):
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100))
    remind: Mapped["Remind"] = relationship(back_populates="user")
    habits: Mapped[list["Habit"]] = relationship(
        "Habit",
        back_populates="user",
        lazy="select",
        cascade="all, delete",
    )

    def __str__(self):
        return f"username={self.email}"

    def __repr__(self):
        return str(self)


class Remind(Base):
    time: Mapped[int] = mapped_column(SMALLINT)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), index=True, unique=True,
    )
    user_chat_id: Mapped[BIGINT] = mapped_column(BIGINT)
    user: Mapped[User] = relationship(
        back_populates="remind",
        lazy="select"
    )
