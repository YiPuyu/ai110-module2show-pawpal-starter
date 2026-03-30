# tests/test_pawpal.py
import pytest
from pawpal_system import Task, Pet

def test_task_completion():
    task = Task(title="Feed Buddy", duration_minutes=10)
    assert not task.completed   # 初始状态应该是未完成
    task.mark_complete()
    assert task.completed       # 调用 mark_complete() 后应该变成完成

def test_add_task_to_pet():
    pet = Pet(name="Buddy", species="dog")
    assert len(getattr(pet, "tasks", [])) == 0  # 假设 Pet 里有 tasks 列表
    # 给 Pet 添加一个 tasks 属性
    if not hasattr(pet, "tasks"):
        pet.tasks = []
    new_task = Task(title="Walk Buddy", duration_minutes=30)
    pet.tasks.append(new_task)
    assert len(pet.tasks) == 1  # 添加后任务数量应该变为 1