from core.db import get_connection
from modules.tasks.model import Task


class TaskRepository:
    def create_table(self) -> None:
        from modules.tasks.schema import CREATE_TASKS_TABLE_SQL

        with get_connection() as connection:
            connection.execute(CREATE_TASKS_TABLE_SQL)
            connection.commit()

    def create(self, title: str, is_done: bool = False) -> Task:
        query = """
        INSERT INTO tasks (title, is_done)
        VALUES (?, ?)
        """

        with get_connection() as connection:
            cursor = connection.execute(query, (title, int(is_done)))
            connection.commit()

            return Task(
                id=cursor.lastrowid,
                title=title,
                is_done=is_done,
            )

    def get_all(self) -> list[Task]:
        query = """
        SELECT id, title, is_done
        FROM tasks
        ORDER BY id ASC
        """

        with get_connection() as connection:
            rows = connection.execute(query).fetchall()

        return [
            Task(
                id=row["id"],
                title=row["title"],
                is_done=bool(row["is_done"]),
            )
            for row in rows
        ]

    def get_by_id(self, task_id: int) -> Task | None:
        query = """
        SELECT id, title, is_done
        FROM tasks
        WHERE id = ?
        """

        with get_connection() as connection:
            row = connection.execute(query, (task_id,)).fetchone()

        if row is None:
            return None

        return Task(
            id=row["id"],
            title=row["title"],
            is_done=bool(row["is_done"]),
        )

    def update(
        self,
        task_id: int,
        title: str,
        is_done: bool,
    ) -> bool:
        query = """
        UPDATE tasks
        SET title = ?, is_done = ?
        WHERE id = ?
        """

        with get_connection() as connection:
            cursor = connection.execute(query, (title, int(is_done), task_id))
            connection.commit()
            return cursor.rowcount > 0

    def delete(self, task_id: int) -> bool:
        query = "DELETE FROM tasks WHERE id = ?"

        with get_connection() as connection:
            cursor = connection.execute(query, (task_id,))
            connection.commit()
            return cursor.rowcount > 0