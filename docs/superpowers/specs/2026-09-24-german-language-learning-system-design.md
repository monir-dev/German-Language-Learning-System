# German Language Learning System Design

**Date:** 2026-09-24

## Goal

Create a local, Obsidian-friendly German learning system that lets the learner and any future AI agent track syllabus progress, grammar concepts, vocabulary, conjugation, speaking, writing, resources, mistakes, revision, and evidence-based next steps.

## Requirements

- Store all project files locally under `German Learning/German Language Learning System/`.
- Keep a persistent `Agent.md` as the operating contract for future AI agents.
- Maintain a syllabus from the current B1.1 stage toward C1, with speaking fluency as the first practical target.
- Create one dated lecture note for each practice session.
- Create or update a topic-wise cheatsheet after every lecture for independent revision outside chat.
- Track grammar concepts, vocabulary, conjugation, speaking, writing, assessments, resources, errors, and revision.
- Track listening separately and establish explicit grammar, vocabulary, conjugation, speaking, listening, and writing baselines.
- Use a Bengali/German teaching policy so lessons remain understandable while practice gradually becomes German-heavy.
- Track vocabulary separately by word type and classify verbs by form group and use/topic group.
- Make progress evidence-based: no topic is marked complete without a linked lecture, exercise, or assessment.
- Let each agent derive the next starting point from current state instead of relying on a hard-coded next lesson.
- Keep the notes readable in Obsidian without requiring Dataview or other plugins.

## Information Architecture

```text
German Language Learning System/
├── .gitignore
├── .obsidian/
├── Agent.md
├── README.md
├── Syllabus.md
├── Dashboard.md
├── Lectures/
├── Cheatsheets/
│   ├── Cheatsheet-Index.md
│   ├── Grammar/
│   ├── Conjugation/
│   └── Vocabulary/
├── Grammar/
│   ├── Grammar-Tracker.md
│   └── Concepts/
├── Vocabulary/
│   ├── Vocabulary-Tracker.md
│   ├── Vocabulary-Index.md
│   ├── Verbs/
│   ├── Nouns/
│   ├── Adjectives/
│   ├── Adverbs-and-Phrases/
│   └── Wordlists/
├── Conjugation/
│   ├── Conjugation-Tracker.md
│   └── Verbs/
├── Speaking/
│   ├── Speaking-Tracker.md
│   └── Conversation-Transcripts/
├── Listening/
│   ├── Listening-Tracker.md
│   └── Practice-Logs/
├── Writing/
│   ├── Writing-Tracker.md
│   └── Corrections/
├── Assessments/
│   ├── Baseline-Assessment.md
│   ├── Placement-Tests/
│   └── Progress-Tests/
├── docs/
├── Resources/
│   ├── Resource-Index.md
│   └── Notes/
├── External Resources/
└── Memory/
    ├── Current-Progress.md
    ├── Error-Log.md
    ├── Revision-Queue.md
    └── Session-Index.md
```

## Lecture and cheatsheet design

Each lecture contains two layers: a learner-facing revision sheet with explanation, examples, exercises, answer key, and checklist; and an agent-facing YAML/evidence record. After the lecture, the agent creates or updates one topic-wise cheatsheet and links it from the lecture, index, Dashboard, and relevant tracker.

## Dashboard Design

`Dashboard.md` will use standard Markdown headings, tables, emoji labels, checkboxes, and text progress bars. It will contain:

1. Current mission and target.
2. Skill snapshot for grammar, vocabulary, conjugation, speaking, listening, and writing.
3. Current syllabus phase and evidence link.
4. Top weaknesses and revision priorities.
5. Recent sessions.
6. Next-session decision rules, not a fixed lesson promise.

Every summary item will link back to the source note where possible.

## Agent Safety and Continuity Rules

`Agent.md` will require every agent to read the syllabus, dashboard, current progress, error log, revision queue, and recent lectures before teaching. Unknown information must be labelled `Unknown — needs assessment`; agents must not infer completion, invent prior lessons, or silently overwrite evidence. Each update must preserve the learner's exact answer, correction, evidence link, and date.

## Status Model

Topics use: `Not started`, `Learning`, `Practiced`, `Needs revision`, and `Stable`. A topic becomes `Stable` only after successful use across more than one practice or an assessment. Errors are tracked separately with first seen date, latest example, correction, recurrence count, and review status.

## Repository and resource layout

All project content is inside this folder so it can later be added to Git as one repository. Existing PDFs, CSVs, and HTML resources live under `External Resources/`; they are indexed by `Resources/Resource-Index.md` and are not duplicated. Obsidian editor state is kept under `.obsidian/`, with personal workspace files excluded by `.gitignore`. Planning and design records live under `docs/`.

Before publishing publicly, review `External Resources/` for copyright and redistribution permissions.
