class TaskError(Exception):
    """Base exception for the tasks module."""


class TaskNotFoundError(TaskError):
    """Raised when a task cannot be found."""


class InvalidParentTaskError(TaskError):
    """Raised when a task is assigned an invalid parent."""
