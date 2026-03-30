# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

My initial UML design for PawPal+ includes five main classes: Owner, Pet, Task, ScheduledItem, and Schedule.

Owner: Stores the owner's name and available time; checks if a task fits in the schedule.
Pet: Stores pet details (name, species, age, notes) and provides a readable display.
Task: Stores task info (title, duration, priority), tracks completion, and provides priority for scheduling.
ScheduledItem: Represents a task at a specific time, calculates end time, and formats display.
Schedule: Manages the daily plan, builds it from tasks considering priorities and available time, and provides summaries and queries.

This design separates responsibilities clearly: Owner and Pet are entities, Task represents actions, ScheduledItem represents scheduled occurrences, and Schedule manages the overall plan.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
Time availability: Each owner has a daily limit of available minutes (e.g., 120 min). Tasks cannot exceed this limit.
Task priority: Tasks are labeled high, medium, or low priority; higher-priority tasks are scheduled first.
Task duration: The scheduler checks whether a task fits in the remaining available time.
Pet association: Each task is linked to a specific pet to ensure correct assignment.

Decision rationale:

Time and priority are the most critical constraints because an owner has limited daily time, and high-priority tasks must be completed.
Pet association ensures tasks are correctly assigned to each pet.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
Tradeoff: The current scheduler uses a greedy, priority-based algorithm and does not detect overlapping task times.
Reasoning: This approach is simple, efficient, and easy to understand, and it ensures high-priority tasks are scheduled. Handling exact overlaps or partial conflicts would increase complexity without significant benefit for a typical pet owner.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
