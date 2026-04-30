from modules.tasks.exceptions import InvalidParentTaskError, TaskNotFoundError
from modules.tasks.repository import TaskRepository
from modules.tasks.schemas import TaskCreate, TaskRead, TaskUpdate


class TaskService:
    def __init__(self, repository: TaskRepository | None = None) -> None:
        self.repository = repository or TaskRepository()

    def create_task(self, payload: TaskCreate) -> TaskRead:
        if payload.parent_id is not None and not self.repository.exists(payload.parent_id):
            raise InvalidParentTaskError(
                f"Parent task with id={payload.parent_id} does not exist"
            )

        task = self.repository.create(
            title=payload.title,
            is_done=payload.is_done,
            parent_id=payload.parent_id,
        )
        return TaskRead.model_validate(task)

    def get_task_by_id(self, task_id: int) -> TaskRead:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with id={task_id} was not found")

        return TaskRead.model_validate(task)

    def get_all_tasks(self) -> list[TaskRead]:
        tasks = self.repository.get_all()
        return [TaskRead.model_validate(task) for task in tasks]

    def update_task(self, task_id: int, payload: TaskUpdate) -> TaskRead:
        existing_task = self.repository.get_by_id(task_id)
        if existing_task is None:
            raise TaskNotFoundError(f"Task with id={task_id} was not found")

        if payload.parent_id is not None:
            if payload.parent_id == task_id:
                raise InvalidParentTaskError("A task cannot be its own parent")

            if not self.repository.exists(payload.parent_id):
                raise InvalidParentTaskError(
                    f"Parent task with id={payload.parent_id} does not exist"
                )

        updated_task = self.repository.update(
            task_id,
            title=payload.title,
            is_done=payload.is_done,
            parent_id=payload.parent_id,
        )

        if updated_task is None:
            raise TaskNotFoundError(f"Task with id={task_id} was not found")

        return TaskRead.model_validate(updated_task)

    def delete_task(self, task_id: int) -> None:
        deleted = self.repository.delete(task_id)
        if not deleted:
            raise TaskNotFoundError(f"Task with id={task_id} was not found")