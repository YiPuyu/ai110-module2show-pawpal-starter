from __future__ import annotations

# NOTE: from __future__ import annotations is required so that forward references
# (e.g. Owner referencing Task before Task is defined) are evaluated lazily.

from dataclasses import dataclass, field
from typing import List, Optional


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Owner:
    name: str
    available_minutes: int = 120

    def can_fit(self, task: Task, used_minutes: int = 0) -> bool:
        """Return True if task fits within remaining available time."""
        return task.duration_minutes <= (self.available_minutes - used_minutes)

    def __str__(self) -> str:
        return f"{self.name} ({self.available_minutes} min available)"


@dataclass
class Pet:
    name: str
    species: str
    age_years: Optional[float] = None
    notes: str = ""

    def __str__(self) -> str:
        age_str = f", {self.age_years}yr" if self.age_years is not None else ""
        return f"{self.name} the {self.species}{age_str}"


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    completed: bool = False

    def __post_init__(self) -> None:
        # Validate priority value on construction
        if self.priority not in PRIORITY_ORDER:
            raise ValueError(
                f"priority must be one of {list(PRIORITY_ORDER)}, got {self.priority!r}"
            )
        if self.duration_minutes <= 0:
            raise ValueError(f"duration_minutes must be positive, got {self.duration_minutes}")

    def priority_value(self) -> int:
        """Lower number = higher priority (for sorting)."""
        return PRIORITY_ORDER[self.priority]

    def mark_complete(self) -> None:
        self.completed = True

    def __str__(self) -> str:
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.title} ({self.duration_minutes} min, {self.priority})"


@dataclass
class ScheduledItem:
    task: Task
    start_minute: int  # minutes from midnight; 480 = 8:00 AM

    @property
    def end_minute(self) -> int:
        return self.start_minute + self.task.duration_minutes

    def start_time_str(self) -> str:
        minute_of_day = self.start_minute % 1440  # guard against values >= 24h
        h, m = divmod(minute_of_day, 60)
        period = "AM" if h < 12 else "PM"
        h12 = h % 12 or 12
        return f"{h12}:{m:02d} {period}"

    def __str__(self) -> str:
        return f"{self.start_time_str()} — {self.task.title} ({self.task.duration_minutes} min)"


@dataclass
class Schedule:
    owner: Owner
    pet: Pet
    items: List[ScheduledItem] = field(default_factory=list)

    def add_item(self, item: ScheduledItem) -> None:
        self.items.append(item)

    def total_minutes(self) -> int:
        return sum(i.task.duration_minutes for i in self.items)

    def is_within_capacity(self) -> bool:
        return self.total_minutes() <= self.owner.available_minutes

    def build_from_tasks(
        self,
        tasks: List[Task],
        start_minute: int = 480,  # minutes from midnight; 480 = 8:00 AM
    ) -> None:
        """Greedily schedule tasks by priority until available time is used up."""
        self.items.clear()
        sorted_tasks = sorted(tasks, key=lambda t: t.priority_value())
        cursor = start_minute
        remaining = self.owner.available_minutes

        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                self.add_item(ScheduledItem(task=task, start_minute=cursor))
                cursor += task.duration_minutes
                remaining -= task.duration_minutes

    def tasks_by_priority(self, priority: str) -> List[ScheduledItem]:
        return [i for i in self.items if i.task.priority == priority]

    def unscheduled_tasks(self, all_tasks: List[Task]) -> List[Task]:
        scheduled_ids = {id(i.task) for i in self.items}
        return [t for t in all_tasks if id(t) not in scheduled_ids]

    def summary(self) -> str:
        lines = [
            f"Schedule for {self.pet} — owner: {self.owner}",
            f"Total time: {self.total_minutes()} / {self.owner.available_minutes} min",
            "",
        ]
        for item in self.items:
            lines.append(str(item))
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.summary()
