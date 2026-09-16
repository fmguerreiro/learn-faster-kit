---
description: Initialize a new learning topic $ARGUMENTS or continue learning an existing one using the FASTER framework
---

## Context

Inspect `.learning/` with `read` and `glob`. Ignore `.learning/scripts/` when identifying the current topic. Read the topic metadata, syllabus, progress, and review schedule needed for this workflow.

## Your Task

Initialize learning for the specified topic using the FASTER framework.

**If a topic already exists:**

- Inform: "This project is already learning [topic name]"
- Check for due reviews first (conduct before new learning if any)
- Continue with current topic (1 project = 1 learning goal)

**If no topic exists yet:**

1. **Gather learning preferences** with `ask` base on users selected topic:
   <example>

```json
{
  "questions": [
    {
      "question": "What level do you want to achieve with [topic]?",
      "options": [
        {
          "label": "Beginner",
          "description": "Fundamentals and basic concepts"
        },
        {
          "label": "Intermediate",
          "description": "Practical skills and common patterns"
        },
        {
          "label": "Advanced",
          "description": "Deep expertise and edge cases"
        },
        {
          "label": "Expert",
          "description": "Mastery level, architecture, optimization"
        }
      ],
      "id": "level",
      "multi": false
    },
    {
      "question": "What do you want to focus on?",
      "options": [
        {
          "label": "Theory",
          "description": "Concepts, principles, how things work"
        },
        {
          "label": "Practice",
          "description": "Hands-on coding and building projects"
        },
        {
          "label": "Real-world",
          "description": "Production patterns and best practices"
        },
        {
          "label": "Interview prep",
          "description": "Common questions and problem-solving"
        }
      ],
      "id": "focus",
      "multi": true
    }
  ]
}
```

</example>

2. Run: `python3 .learning/scripts/init_learning.py "[topic name]" .learning`
3. Parse JSON output and follow `llm_directive`
4. **READ** `.learning/<topic-slug>/syllabus.md` to see the template structure
5. Generate comprehensive syllabus content **tailored to user's level and focus areas**
6. **Replace** the template placeholders with actual content
7. Update metadata: `"syllabus_generated": true` in `.learning/<topic-slug>/metadata.json`

**Follow the template structure:**

- All sections from the template file (Overview, Prerequisites, Learning Objectives, etc.)
- 3-4 Phases with specific concepts + 🔨 hands-on projects
- Checkboxes `- [ ]` for tracking progress

**Important:**

- Generate comprehensive syllabi (not minimal)
- Include hands-on practice in every phase
