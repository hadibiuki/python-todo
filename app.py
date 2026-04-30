from core.init_db import init_db
from modules.tasks import TaskCreate, TaskService, TaskUpdate
from modules.tasks.exceptions import InvalidParentTaskError, TaskNotFoundError


def main() -> None:
    init_db()

    task_service = TaskService()

    try:
        root_task = task_service.create_task(
            TaskCreate(title="Build TaskService with Pydantic")
        )
        print("Created root task:")
        print(root_task)

        sub_task = task_service.create_task(
            TaskCreate(
                title="Add validation layer",
                parent_id=root_task.id,
            )
        )
        print("\nCreated sub task:")
        print(sub_task)

        print("\nAll tasks:")
        for task in task_service.get_all_tasks():
            print(task)

        updated_root_task = task_service.update_task(
            root_task.id,
            TaskUpdate(
                title="Build TaskService + Pydantic structure",
                is_done=True,
            ),
        )
        print("\nUpdated root task:")
        print(updated_root_task)

        loaded_task = task_service.get_task_by_id(root_task.id)
        print("\nLoaded task by id:")
        print(loaded_task)

        task_service.delete_task(sub_task.id)
        print("\nSub task deleted successfully.")

    except InvalidParentTaskError as error:
        print(f"Parent error: {error}")
    except TaskNotFoundError as error:
        print(f"Not found error: {error}")
    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()