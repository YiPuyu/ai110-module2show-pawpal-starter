from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import timedelta, datetime

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
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def __str__(self) -> str:
        age_str = f", {self.age_years}yr" if self.age_years is not None else ""
        return f"{self.name} the {self.species}{age_str}"


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    completed: bool = False
    frequency: Optional[str] = None  # "daily", "weekly", or None
    due_date: Optional[datetime] = None  # next scheduled date

    def __post_init__(self) -> None:
        if self.priority not in PRIORITY_ORDER:
            raise ValueError(f"priority must be one of {list(PRIORITY_ORDER)}, got {self.priority!r}")
        if self.duration_minutes <= 0:
            raise ValueError(f"duration_minutes must be positive, got {self.duration_minutes}")

    def priority_value(self) -> int:
        """Lower number = higher priority."""
        return PRIORITY_ORDER[self.priority]

    def mark_complete(self) -> Optional[Task]:
        """Mark this task complete; if recurring, return next instance."""
        self.completed = True
        if self.frequency:
            next_date = None
            if self.due_date:
                if self.frequency == "daily":
                    next_date = self.due_date + timedelta(days=1)
                elif self.frequency == "weekly":
                    next_date = self.due_date + timedelta(weeks=1)
            else:
                next_date = datetime.now() + (timedelta(days=1) if self.frequency=="daily" else timedelta(weeks=1))
            # return new task instance
            return Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                frequency=self.frequency,
                due_date=next_date
            )
        return None

    def __str__(self) -> str:
        status = "✓" if self.completed else "○"
        freq = f", {self.frequency}" if self.frequency else ""
        return f"[{status}] {self.title} ({self.duration_minutes} min, {self.priority}{freq})"


@dataclass
class ScheduledItem:
    task: Task
    start_minute: int  # minutes from midnight; 480 = 8:00 AM

    @property
    def end_minute(self) -> int:
        return self.start_minute + self.task.duration_minutes

    def start_time_str(self) -> str:
        minute_of_day = self.start_minute % 1440
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

    def build_from_tasks(self, tasks: List[Task], start_minute: int = 480) -> None:
        """Greedy scheduler: sort by priority and fit tasks in available time."""
        self.items.clear()
        # sort tasks: first incomplete, then priority, then optional due_date
        sorted_tasks = sorted(
            [t for t in tasks if not t.completed],
            key=lambda t: (t.due_date or datetime.min, t.priority_value())
        )
        cursor = start_minute
        remaining = self.owner.available_minutes
        for task in sorted_tasks:
            if task.duration_minutes <= remaining:
                # check for conflict
                conflict = any(
                    item.start_minute < cursor + task.duration_minutes and cursor < item.end_minute
                    for item in self.items
                )
                if conflict:
                    print(f"⚠ Conflict detected for task '{task.title}' at {cursor} min")
                self.add_item(ScheduledItem(task=task, start_minute=cursor))
                cursor += task.duration_minutes
                remaining -= task.duration_minutes

    def filter_by_completion(self, completed: bool) -> List[ScheduledItem]:
        return [i for i in self.items if i.task.completed == completed]

    def filter_by_pet(self, pet_name: str) -> List[ScheduledItem]:
        if self.pet.name != pet_name:
            return []
        return self.items

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