from dataclasses import dataclass


@dataclass(slots=True)
class Task:
    id: int
    title: str
    is_done: bool