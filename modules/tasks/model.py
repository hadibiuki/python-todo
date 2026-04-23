from __future__ import annotations

from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    is_done: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("tasks.id"),
        nullable=True,
    )

    parent: Mapped[Optional["Task"]] = relationship(
        "Task",
        remote_side=lambda: [Task.id],
        back_populates="children",
    )

    children: Mapped[list["Task"]] = relationship(
        "Task",
        back_populates="parent",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"Task(id={self.id}, title={self.title!r}, "
            f"is_done={self.is_done}, parent_id={self.parent_id})"
        )