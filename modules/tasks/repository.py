from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.db import get_session
from modules.tasks.model import Task


class TaskRepository:
    def create(
        self,
        title: str,
        is_done: bool = False,
        parent_id: int | None = None,
    ) -> Task:
        with get_session() as session:
            task = Task(
                title=title,
                is_done=is_done,
                parent_id=parent_id,
            )
            session.add(task)
            session.flush()
            session.refresh(task)
            return task

    def get_all(self) -> list[Task]:
        with get_session() as session:
            stmt = (
                select(Task)
                .options(selectinload(Task.children))
                .order_by(Task.id.asc())
            )
            return list(session.scalars(stmt).all())

    def get_by_id(self, task_id: int) -> Task | None:
        with get_session() as session:
            stmt = (
                select(Task)
                .where(Task.id == task_id)
                .options(selectinload(Task.children))
            )
            return session.scalar(stmt)

    def update(
        self,
        task_id: int,
        *,
        title: str | None = None,
        is_done: bool | None = None,
        parent_id: int | None = None,
    ) -> Task | None:
        with get_session() as session:
            task = session.get(Task, task_id)
            if task is None:
                return None

            if title is not None:
                task.title = title

            if is_done is not None:
                task.is_done = is_done

            task.parent_id = parent_id
            session.flush()
            session.refresh(task)
            return task

    def delete(self, task_id: int) -> bool:
        with get_session() as session:
            task = session.get(Task, task_id)
            if task is None:
                return False

            session.delete(task)
            session.flush()
            return True

    def get_root_tasks(self) -> list[Task]:
        with get_session() as session:
            stmt = (
                select(Task)
                .where(Task.parent_id.is_(None))
                .options(selectinload(Task.children))
                .order_by(Task.id.asc())
            )
            return list(session.scalars(stmt).all())

    def get_subtasks(self, parent_id: int) -> list[Task]:
        with get_session() as session:
            stmt = (
                select(Task)
                .where(Task.parent_id == parent_id)
                .order_by(Task.id.asc())
            )
            return list(session.scalars(stmt).all())