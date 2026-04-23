from core.init_db import init_db
from modules.tasks import TaskRepository


def main() -> None:
    init_db()

    task_repository = TaskRepository()

    root_task = task_repository.create("Build SQLAlchemy version")
    sub_task_1 = task_repository.create(
        "Create database layer",
        parent_id=root_task.id,
    )
    sub_task_2 = task_repository.create(
        "Create task repository",
        parent_id=root_task.id,
    )

    print("Created root task:")
    print(root_task)

    print("\nCreated subtasks:")
    print(sub_task_1)
    print(sub_task_2)

    print("\nAll tasks:")
    for task in task_repository.get_all():
        print(task)

    print("\nRoot tasks only:")
    for task in task_repository.get_root_tasks():
        print(task)

    print("\nSubtasks of root task:")
    for task in task_repository.get_subtasks(root_task.id):
        print(task)

    # updated_task = task_repository.update(
    #     root_task.id,
    #     title="Build professional SQLAlchemy structure",
    #     is_done=True,
    # )
    # print("\nUpdated root task:")
    # print(updated_task)

    # deleted = task_repository.delete(sub_task_2.id)
    # print(f"\nDeleted sub_task_2: {deleted}")


if __name__ == "__main__":
    main()