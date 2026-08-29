from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base

if TYPE_CHECKING:
    from app.models.task import Task


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    tasks: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
