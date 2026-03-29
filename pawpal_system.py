from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Owner:
    name: str
    available_minutes: int = 120

    def can_fit(self, task: Task, used_minutes: int = 0) -> bool: ...

    def __str__(self) -> str: ...


@dataclass
class Pet:
    name: str
    species: str
    age_years: Optional[float] = None
    notes: str = ""

    def __str__(self) -> str: ...


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    completed: bool = False

    def __post_init__(self) -> None: ...

    def priority_value(self) -> int: ...

    def mark_complete(self) -> None: ...

    def __str__(self) -> str: ...


@dataclass
class ScheduledItem:
    task: Task
    start_minute: int

    @property
    def end_minute(self) -> int: ...

    def start_time_str(self) -> str: ...

    def __str__(self) -> str: ...


@dataclass
class Schedule:
    owner: Owner
    pet: Pet
    items: List[ScheduledItem] = field(default_factory=list)

    def add_item(self, item: ScheduledItem) -> None: ...

    def total_minutes(self) -> int: ...

    def is_within_capacity(self) -> bool: ...

    def build_from_tasks(self, tasks: List[Task], start_minute: int = 480) -> None: ...

    def tasks_by_priority(self, priority: str) -> List[ScheduledItem]: ...

    def unscheduled_tasks(self, all_tasks: List[Task]) -> List[Task]: ...

    def summary(self) -> str: ...

    def __str__(self) -> str: ...
