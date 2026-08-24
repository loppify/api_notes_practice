import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.task_tags import task_tags

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.tag import Tag

class StatusEnum(str, enum.Enum):
    UNCOMPLETED = "UNCOMPLETED"
    COMPLETED = "COMPLETED"
    REMOVED = "REMOVED"
    ARCHIVED = "ARCHIVED"
    OVERDUE = "OVERDUE"


class Task(Base):
    title: Mapped[str]
    description: Mapped[str]
    deadline: Mapped[datetime]
    status: Mapped[StatusEnum] = mapped_column(default=StatusEnum.UNCOMPLETED, server_default="'UNCOMPLETED'")
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped["User"] = relationship(
        "User",
        back_populates="tasks",
    )

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary=task_tags,
        back_populates="tasks",
    )
