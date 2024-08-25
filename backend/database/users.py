from typing import TYPE_CHECKING

from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


if TYPE_CHECKING:
    from .habits import Habits


class User(Base):
    username: Mapped[str] = mapped_column(String(32), unique=True)
    user_chat_id: Mapped[int] = mapped_column(BigInteger)
    password: Mapped[str] = mapped_column(String(50))
    posts: Mapped[list["Habits"]] = relationship(back_populates="user")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
