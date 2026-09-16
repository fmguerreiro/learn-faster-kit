---
description: Conduct spaced repetition review session for learned concepts
---

## Context

Inspect `.learning/` with `read` and `glob`. Ignore `.learning/scripts/` when identifying the current topic. Read the topic metadata, syllabus, progress, and review schedule needed for this workflow.

## Your Task

Conduct spaced repetition reviews to combat forgetting and reinforce learning.

**If no `.learning/`:**

- Inform: "No learning in progress. Use `/learn [topic]` to start!"

**If reviews due:**

For each concept in review list:

1. Present: "Let's review: [Concept Name]"
2. Prompt teaching (rotate):
   - "Explain [concept] in your own words"
   - "How would you teach [concept] to a beginner?"
   - "What's the key idea behind [concept]?"
3. Listen to user's explanation
4. Evaluate:
   - Clear & accurate → Praise, mark reviewed
   - Partial → Ask clarifying questions, guide to fill gaps
   - Incorrect → Gently correct, provide hints
5. Mark reviewed: `python3 .learning/scripts/review_scheduler.py review <topic-slug> "[Concept]"`

**After all reviews:**

- Celebrate: "Great job! Reviewed N concepts! 🎉"
- Show next review date
- Use `ask` for next action:

```json
{
  "questions": [
    {
      "question": "What would you like to do next?",
      "options": [
        {
          "label": "Learn new",
          "description": "Continue with next syllabus item"
        },
        {
          "label": "Practice",
          "description": "Work on hands-on exercises"
        },
        {
          "label": "Take break",
          "description": "Come back later"
        }
      ],
      "id": "next",
      "multi": false
    }
  ]
}
```

**If no reviews due:**

- Inform: "No reviews due today! Next: [date]"
- Suggest continuing with new material

**Handling forgotten concepts:**

- Don't give answer immediately
- Provide hints: "It's related to [context]..."
- If still stuck: Review briefly, reschedule for tomorrow
- Reschedule: `python3 .learning/scripts/review_scheduler.py add <topic-slug> "[Concept]"`

**Key principle:** Active recall (user reconstructs from memory), not passive recognition
