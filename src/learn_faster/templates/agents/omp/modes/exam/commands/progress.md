---
description: Show detailed progress report for current learning topic
---

## Context

Inspect `.learning/` with `read` and `glob`. Ignore `.learning/scripts/` when identifying the current topic. Read the topic metadata, syllabus, progress, and review schedule needed for this workflow.

## Your Task

Generate an encouraging progress report showing learning journey and next steps.

**If no `.learning/`:**

- Inform: "No learning in progress yet. Use `/learn [topic]` to start!"

**Calculate metrics:**

- Sessions completed (from metadata)
- Days since start (from created_at)
- Concepts learned (count from progress.md)
- Syllabus progress (checked `[x]` vs total `[ ]`)
- Reviews completed (from review_schedule.json)
- Current phase (from syllabus position)

**Present report:**

```markdown
📊 Progress Report: [Topic Name]

🎯 Overview
Sessions: [N] | Days: [N] | Phase: [X] - [Name]
Syllabus: [X]% ([M]/[Total] items)

📚 Concepts Learned
✓ [Concept 1]
✓ [Concept 2]
... ([N] total)

🎉 Recent Wins

- [Achievement 1]
- [Achievement 2]

📅 Review Stats
Completed: [N] | Scheduled: [N]
Next review: [date] ([N] concepts)

🎯 Next Focus

1. [Next unchecked item]
2. [Next unchecked item]

💡 Insights
[Personalized based on data]
```

**Celebrate milestones:**

- 5 sessions: "🎉 Building momentum!"
- 10 sessions: "🔥 Committed to learning!"
- 25%: "🎯 Quarter way!"
- 50%: "🚀 Halfway there!"
- 75%: "⭐ Almost mastered!"
- 100%: "🏆 Syllabus complete!"

**Consistency tracking:**

- 3-day streak: "Nice! 3 days in a row!"
- 7-day: "🔥 One week streak!"
- 14-day: "🌟 Two weeks strong!"
- 30-day: "🏅 One month!"

**After report:**

- Suggest next actions
- Offer options: continue learning, do reviews, or break
- Keep encouraging tone

**Key:** Progress reports should motivate, not just inform. Celebrate wins, show growth, suggest forward momentum.
