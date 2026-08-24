from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.task_tags import task_tags

if TYPE_CHECKING:
    from app.models.task import Task

class Tag(Base):
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column(unique=True)
    amount: Mapped[int]

    task: Mapped[list["Task"]] = relationship(
        "Task",
        secondary=task_tags,
        back_populates="tags",
    )
