from pawpal_system import Owner, Pet, Task, Schedule, ScheduledItem

# 创建 Owner 和 Pets
owner = Owner(name="Alice", available_minutes=120)
dog = Pet(name="Buddy", species="dog", age_years=3)
cat = Pet(name="Mittens", species="cat", age_years=2)

# 创建 Tasks
walk = Task(title="Walk Buddy", duration_minutes=30, priority="high")
feed_dog = Task(title="Feed Buddy", duration_minutes=10, priority="medium")
feed_cat = Task(title="Feed Mittens", duration_minutes=10, priority="medium")

tasks = [walk, feed_dog, feed_cat]

# 生成日程
schedule = Schedule(owner=owner, pet=dog)  # 这里先用dog举例
schedule.build_from_tasks(tasks)           # 自动排程

# 打印日程
print(schedule)