from modules.tasks import TaskRepository


def main() -> None:
    task_repository = TaskRepository()
    task_repository.create_table()

    created_task = task_repository.create("Learn scalable structure")
    print("Created:", created_task)

    # all_tasks = task_repository.get_all()
    # print("\nAll tasks:")
    # for task in all_tasks:
    #     print(task)


    # updated = task_repository.update(
    #     task_id=created_task.id,
    #     title="Learn scalable structure deeply",
    #     is_done=True,
    # )
    # print("\nUpdated:", updated)

    # found_task = task_repository.get_by_id(created_task.id)
    # print("\nFound by id:", found_task)

    # deleted = task_repository.delete(created_task.id)
    # print("Deleted:", deleted)


if __name__ == "__main__":
    main()