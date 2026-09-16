---
description: Generate a printable exam paper with answer key in PDF format
---

## Context

Inspect `.learning/` with `read` and `glob`. Ignore `.learning/scripts/` when identifying the current topic. Read the topic metadata, syllabus, progress, and review schedule needed for this workflow.

## Your Task

Generate a professional, printable exam paper with a separate answer key that the user can print and complete offline.

### Step 1: Gather Topic Context

Identify the topic directory from the context above (ignore `scripts`, `references`, `config.json`).

Then read:
- `.learning/<topic-slug>/syllabus.md` - What concepts are in the curriculum
- `.learning/<topic-slug>/metadata.json` - Progress and current phase
- `.learning/<topic-slug>/progress.json` - Completed concepts
- `.learning/<topic-slug>/review_schedule.json` - What's been learned and reviewed

### Step 2: Consolidate Context

Create a summary of:
- **Topic name**: [Extract from metadata]
- **Learning phase**: [Current phase from metadata]
- **Concepts covered**: [List from progress.json]
- **Concepts mastered**: [From review_schedule.json - concepts with review_count > 2]
- **Recent concepts**: [Last 5-10 concepts learned]
- **Weak areas**: [Concepts with low review counts or marked as difficult]

### Step 3: Invoke Exam Generator with Context

Use the `task` tool to invoke the `exam-generator` agent with the consolidated context:

**How to invoke a subagent:**

Use the `task` tool with:
- `agent`: "exam-generator"
- `task`: Include all the consolidated context and instructions
- `name`: "ExamGenerator"

**Example:**

```
task tool call:
- agent: "exam-generator"
- name: "ExamGenerator"
- task: "Generate a printable exam paper with answer key.

Topic Context:
- Topic: [topic name]
- Current Phase: [phase name]
- Total concepts covered: [N]
- Concepts mastered: [list]
- Recent concepts: [list]
- Weak areas: [list]

Please:
1. Search online for real exam examples in this domain
2. Ask user preferences (type, difficulty, scope)
3. Generate exam paper covering these concepts (focus on recent and weak areas)
4. Generate separate answer key
5. Convert both to PDF using the script
6. Provide file paths and next steps"
```

The agent will handle the complete workflow and return the results.
