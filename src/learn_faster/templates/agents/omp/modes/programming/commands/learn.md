---
description: Initialize or continue learning a programming topic using project-based approach
---

## Context

Inspect `.learning/` with `read` and `glob`. Ignore `.learning/scripts/` when identifying the current topic. Read the topic metadata, syllabus, progress, and review schedule needed for this workflow.

## Your Task

Initialize learning for the specified programming topic using the FASTER framework with project-based approach.

**If a topic already exists:**

- Inform: "This project is already learning [topic name]"
- Check for due reviews first (conduct before new learning if any)
- Continue with current topic (1 project = 1 learning goal)

**If no topic exists yet:**

1. **Gather learning preferences** with `ask` based on user's selected topic:
   <example>

```json
{
  "questions": [
    {
      "question": "What level do you want to achieve with [topic]?",
      "options": [
        {
          "label": "Beginner",
          "description": "Fundamentals and basic syntax"
        },
        {
          "label": "Intermediate",
          "description": "Common patterns and projects"
        },
        {
          "label": "Advanced",
          "description": "Architecture and optimization"
        },
        {
          "label": "Expert",
          "description": "Deep internals and best practices"
        }
      ],
      "id": "level",
      "multi": false
    },
    {
      "question": "What's your learning goal?",
      "options": [
        {
          "label": "Build projects",
          "description": "Learn by building real applications"
        },
        {
          "label": "Understand deeply",
          "description": "How things work under the hood"
        },
        {
          "label": "Best practices",
          "description": "Production-ready code patterns"
        },
        {
          "label": "Interview prep",
          "description": "Problem-solving and algorithms"
        }
      ],
      "id": "goal",
      "multi": true
    }
  ]
}
```

</example>

2. Run: `python3 .learning/scripts/init_learning.py "[topic name]" .learning`
3. Parse JSON output and follow `llm_directive`
4. **READ** `.learning/<topic-slug>/syllabus.md` to see the template structure
5. Generate comprehensive syllabus **focused on project-based learning**
6. **Replace** the template placeholders with actual content
7. Update metadata: `"syllabus_generated": true` in `.learning/<topic-slug>/metadata.json`

**Programming Mode Syllabus Guidelines:**

- Structure around building progressively complex projects
- Each phase should include 2-3 concepts + 1-2 🔨 hands-on projects
- Projects should build on previous concepts
- Include testing and debugging at each phase
- Focus on understanding "how it works" not just "how to use it"
- Use checkboxes `- [ ]` for tracking progress

**Important:**

- Generate comprehensive, project-focused syllabi
- Every concept should lead to building something
- Include code quality and best practices throughout
