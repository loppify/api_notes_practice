from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base
from app.models.task_tags import task_tags

if TYPE_CHECKING:
    from app.models.task import Task


class Tag(Base):
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=True)

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        secondary=task_tags,
        back_populates="tags",
        lazy="selectin",
    )

    @property
    def amount(self) -> int:
        return len(self.tasks) if self.tasks else 0
