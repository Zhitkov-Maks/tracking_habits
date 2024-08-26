from datetime import datetime as dt, UTC
from sqlalchemy import String, Text, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .mixins import UserRelationMixin
from .base import Base


class Habits(UserRelationMixin, Base):
    # _user_id_nullable = False
    # _user_id_unique = False
    _user_back_populates = "habits"

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    start_date: Mapped[DateTime] = mapped_column(
        DateTime,
        default=dt.now(UTC),
        server_default=str(dt.now(UTC))
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    def __str__(self):
        return (
                f"{self.__class__.__name__}(id={self.id}, "
                f"username={self.title!r}, user_id={self.user_id})"
        )

    def __repr__(self):
        return str(self)
