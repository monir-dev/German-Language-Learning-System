# German Language Learning System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a local Obsidian-friendly German learning system with evidence-based syllabus, dashboard, daily lecture archive, skill trackers, memory, and resource index.

**Architecture:** A self-contained `German Language Learning System` folder will hold human-readable Markdown files. `Agent.md` defines continuity and anti-hallucination rules; `Syllabus.md`, trackers, memory files, and dated lectures provide the source of truth; `Dashboard.md` is a manually maintained but linked overview that works without plugins.

**Tech Stack:** Markdown, Obsidian wikilinks, standard filesystem folders. No external dependencies.

**Spec:** `docs/superpowers/specs/2026-09-24-german-language-learning-system-design.md`

## Global Constraints

- Store the learning system locally under `German Learning/German Language Learning System/`.
- Use standard Markdown so the notes remain readable without Obsidian plugins.
- Keep study resources inside `External Resources/`; do not duplicate them.
- Keep the complete project self-contained so the top-level folder can later become one Git repository.
- Keep `Memory/Current-Progress.md` as the canonical progress source; Dashboard is a summary only.
- Store active phase, listening progress, baseline status, and Bengali/German teaching policy explicitly.
- Create or update a topic-wise cheatsheet automatically after every lecture.
- Track verbs, nouns, adjectives, and adverbs/phrases in separate vocabulary files.
- Maintain a tiered high-utility spoken-verb roadmap with regular, irregular, modal, reflexive, and verb–preposition groups.
- Do not claim a topic is complete without evidence.
- Mark unknown state as `Unknown — needs assessment`.
- Preserve exact learner answers and dated corrections.

## Review Focus

- A new agent can recover the learner's state from the documented files.
- Dashboard links and progress summaries point to real local notes.
- The syllabus distinguishes completed, practiced, weak, and unknown topics.
- Existing resource paths are indexed without changing the source files.
- The current lesson is represented accurately, including known errors.

### Task 1: Create the project foundation

**Files:**
- Create: `German Language Learning System/README.md`
- Create: `German Language Learning System/Agent.md`
- Create: `German Language Learning System/Syllabus.md`
- Create: `German Language Learning System/Dashboard.md`

- [ ] **Step 1:** Write the project usage instructions, agent operating rules, CEFR syllabus, and Obsidian dashboard.
- [ ] **Step 2:** Verify each file contains the required sections and links to the appropriate folders.

### Task 2: Create trackers and persistent memory

**Files:**
- Create: `German Language Learning System/Grammar/Grammar-Tracker.md`
- Create: `German Language Learning System/Vocabulary/Vocabulary-Tracker.md`
- Create: `German Language Learning System/Conjugation/Conjugation-Tracker.md`
- Create: `German Language Learning System/Speaking/Speaking-Tracker.md`
- Create: `German Language Learning System/Writing/Writing-Tracker.md`
- Create: `German Language Learning System/Memory/Current-Progress.md`
- Create: `German Language Learning System/Memory/Error-Log.md`
- Create: `German Language Learning System/Memory/Revision-Queue.md`
- Create: `German Language Learning System/Memory/Session-Index.md`

- [ ] **Step 1:** Add status tables and evidence columns to each skill tracker.
- [ ] **Step 2:** Add current B1.1 baseline, speaking-first goal, known weaknesses, and revision priorities to memory.
- [ ] **Step 3:** Verify the trackers agree on the same status names and learner identity.

### Task 3: Add lecture and resource foundations

**Files:**
- Create: `German Language Learning System/Lectures/2026-09-24__Praeteritum-und-Modalverben.md`
- Create: `German Language Learning System/Resources/Resource-Index.md`
- Create: `German Language Learning System/Grammar/Concepts/README.md`
- Create: `German Language Learning System/Conjugation/Verbs/README.md`
- Create: `German Language Learning System/Speaking/Conversation-Transcripts/README.md`
- Create: `German Language Learning System/Writing/Corrections/README.md`

- [ ] **Step 1:** Record the current session exactly: sein, haben, können, müssen, Präteritum, word order, and the learner's corrections.
- [ ] **Step 2:** Index existing PDFs and CSV files using relative links from the learning system.
- [ ] **Step 3:** Verify the lecture links to the tracked concepts and memory files.

### Task 4: Validate the system

**Files:**
- Validate: all files created in Tasks 1–3.

- [ ] **Step 1:** List the full project tree and confirm every required file exists.
- [ ] **Step 2:** Search for forbidden placeholder text such as `TBD` or `TODO`.
- [ ] **Step 3:** Check all referenced internal files exist and all resource links resolve to existing files.
- [ ] **Step 4:** Read the dashboard and current-progress files end-to-end and confirm they agree.

### Task 5: Keep the repository self-contained

**Files:**
- Move: `Old learning resources/` → `German Language Learning System/External Resources/`
- Move: `docs/` → `German Language Learning System/docs/`
- Move: `.obsidian/` → `German Language Learning System/.obsidian/`
- Rename: `German Learning System/` → `German Language Learning System/`
- Modify: `German Language Learning System/Resources/Resource-Index.md`
- Create: `German Language Learning System/.gitignore`

- [x] Rename the main system folder.
- [x] Move external resources, documentation, and Obsidian configuration inside the system folder.
- [x] Update resource links and documentation paths.
- [x] Add Git-safe ignores for personal editor state and macOS metadata.
- [x] Verify the project has one meaningful top-level folder and no stale operational paths.

### Task 6: Add assessment and multilingual teaching controls

**Files:**
- Create: `German Language Learning System/Listening/Listening-Tracker.md`
- Create: `German Language Learning System/Listening/Practice-Logs/README.md`
- Create: `German Language Learning System/Assessments/Baseline-Assessment.md`
- Modify: `German Language Learning System/Agent.md`
- Modify: `German Language Learning System/Memory/Current-Progress.md`
- Modify: `German Language Learning System/Syllabus.md`
- Modify: `German Language Learning System/Dashboard.md`

- [x] Define `Current-Progress.md` as the canonical progress source.
- [x] Add the active phase field and link it from the syllabus and dashboard.
- [x] Add a dedicated listening tracker and listening practice-log location.
- [x] Add baseline assessment rules for all six core skills.
- [x] Add Bengali/German teaching and correction policy.

### Task 7: Add automatic topic cheatsheets

**Files:**
- Create: `German Language Learning System/Cheatsheets/README.md`
- Create: `German Language Learning System/Cheatsheets/Cheatsheet-Index.md`
- Create: `German Language Learning System/Cheatsheets/Conjugation/Modalverben-Präsens-Präteritum.md`
- Modify: `German Language Learning System/Agent.md`
- Modify: `German Language Learning System/Dashboard.md`
- Modify: relevant lecture, tracker, and session-index files

- [x] Define the automatic create-or-update rule.
- [x] Add the first modal-verb cheatsheet from covered material.
- [x] Add a learner-facing continuation lecture and link the cheatsheet evidence.

### Task 8: Split vocabulary tracking by word type and verb group

**Files:**
- Create: `German Language Learning System/Vocabulary/Vocabulary-Index.md`
- Create: `German Language Learning System/Vocabulary/Verbs/Verb-Tracker.md`
- Create: `German Language Learning System/Vocabulary/Verbs/Core-Verbs-Roadmap.md`
- Create: `German Language Learning System/Vocabulary/Verbs/Verb-Group-Index.md`
- Create: regular, irregular, modal, reflexive, and verb–preposition group notes
- Create: noun, adjective, and adverb/phrase trackers
- Modify: `German Language Learning System/Agent.md` and `Dashboard.md`

- [x] Separate vocabulary by word type.
- [x] Add a high-utility spoken verb roadmap with tier and status tracking.
- [x] Add form-group and topic-group classification rules.
