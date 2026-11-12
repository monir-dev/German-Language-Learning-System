# Goethe B1 Vocabulary Course Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare a local topic-wise Goethe B1 vocabulary course with audited source coverage, complete self-study lessons, A–Z lookup and evidence-preserving progress integration.

**Architecture:** An occurrence inventory maps source sections/pages to normalized targets and primary lessons. Existing word-type trackers remain the learning-status authority; prepared course lessons are separate from dated practice lectures. Readable Markdown views work in Obsidian without running scripts.

**Tech Stack:** Markdown, YAML frontmatter, UTF-8 JSON, Python standard library, bundled pdfplumber/pypdf. No new app or required Obsidian plugin.

**Spec:** `docs/superpowers/specs/2026-11-12-goethe-b1-vocabulary-course-design.md` — approved 2026-11-12.

**Plan state:** Native execution selected by learner. Implementation in progress; see `2026-11-12-goethe-b1-execution-ledger.md`. First starter batch is available; full source reconciliation/remaining authoring are not complete.

## Global Constraints

- Keep everything in this existing local Obsidian vault.
- Preserve all existing vocabulary and dated learner evidence.
- Use normally five target words/phrases per new-word lesson. A word-family or difficult verb lesson may use fewer.
- Existing word-type trackers remain the canonical learning-status records.
- Keep `Memory/Current-Progress.md` authoritative for current teaching state and next-step selection; Dashboard is a linked summary.
- Keep the official PDF and verbatim extraction caches private and ignored by Git.
- Do not include the publisher's example sentences in generated lessons.
- No invented 2026-11-12 practice session or elapsed study time.
- Do not call all lessons ready until they contain actual teaching material, exercises and answer keys.
- Do not initialize Git or make commits/pushes as part of this request. Preserve the user's future-publication option without assuming third-party redistribution rights.

## Review Focus

- Multi-column source text must not combine headwords with neighboring examples or drop continuations at page breaks.
- Word groups on PDF pages 8–15, subordinate entries and regional variants must not disappear when deduplicating the alphabetic body.
- Existing guided evidence must not be overwritten, inflated or treated as a new course assessment.
- Structurally valid lesson files must not be called checked/ready if meanings, forms or answer keys remain unreviewed.
- Preparation counts, learned-word evidence and approximate publisher counts must never share an unlabeled denominator.

## Paths and interfaces

All paths below are relative to `German Language Learning System/`. Course root: `Vocabulary/Wordlists/Goethe-B1/`.

Create:
- `scripts/goethe_b1/{extract,normalize,render,validate}.py`: narrowly scoped reproducible transformations and checks.
- `scripts/goethe_b1/tests/test_course.py`: standard-library unittest regression tests.
- Course root: `Source-Manifest.md`, `Inventory.json`, `Coverage.md`, `README.md`, `A-Z.md`, `Lesson-Index.md`, `Preparation-Log.md`.
- Course `Data/`: reviewed normalization overrides, topic assignments and original teaching records in JSON; authoritative editable inputs, not learning statuses.
- Course `Lessons/`: prepared topic lessons and review lessons.
- `Cheatsheets/Vocabulary/Goethe-B1-Course.md`: course revision/navigation guidance; topic sheets link rather than duplicate progress.

Modify: `.gitignore`, `Agent.md`, `README.md`, `Syllabus.md`, `Dashboard.md`, `Resources/Resource-Index.md`, `Vocabulary/{Vocabulary-Index,Vocabulary-Tracker}.md`, existing word-type trackers as needed, `Cheatsheets/Cheatsheet-Index.md`, `Memory/{Current-Progress,Revision-Queue}.md`.

Private extraction cache: `External Resources/Goethe-B1-private-cache/` (exact directory ignore). Never put source example prose into generated teaching records.

Execution environment already checked: system Python lacks PDF libraries and `pdftotext` is absent. Bundled Python has pdfplumber and pypdf:
`/Users/mac133/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3`.
Use its path for the commands below on this computer; on another computer discover an installed compatible runtime rather than hard-coding this path into portable course notes.

Shared schemas:
- `Occurrence`: id, PDF page (1-based), printed page, section, layout block, raw headword/form reference, disposition (`mapped`/`needs_review`/`non_target`), target_ids, review_note.
- `Target`: id, lemma, word_type, region, source_occurrence_ids, primary_topic, related_topics, primary_lesson_id, canonical_record_key; no learned-status field.
- `TeachingRecord`: target_id, bn_meanings, usage_notes, grammar, original_examples, exercises, answers, review_state. Verb grammar has six ordered Präsens forms (ich/du/er-sie-es/wir/ihr/sie-Sie), Partizip II, auxiliary, Präteritum, group and case/preposition. Nouns have article, singular, plural or an explicit no-plural note.
- `Lesson`: id, topic, ordered target_ids (normally 1–5), review_target_ids, preparation_state (`draft`/`needs_review`/`ready`), source_refs.

### Task 1: Auditable extraction and source manifest

**Files:** `extract.py`, extraction tests in `test_course.py`, manifest, private cache, `.gitignore`.

**Interfaces:** `extract_source(pdf_path: Path, cache_dir: Path) -> dict` produces source metadata, per-page layout blocks and candidate occurrences. It must not claim candidates are verified targets.

- [ ] Write tests for checksum mismatch, 1-based page references, header/footer exclusion and independent source/example column extraction using small synthetic fixtures, not copied example paragraphs.
- [ ] Run the tests with `python3 -m unittest discover -s scripts/goethe_b1/tests -v`; confirm the unimplemented extraction checks fail.
- [ ] Implement extraction using pdfplumber word coordinates and font/layout information, keeping candidate continuations and ambiguities visible. Keep raw page extraction private.
- [ ] Verify source SHA-256 `8860f7f0c916831b2365f66239a3ceba3be81ddba28e1224846ca8420807fe42`, 104 pages, and sections: preliminaries 1–7, word groups 8–15, alphabetic body from 16 through the last content page; inspect actual terminal pages rather than assuming every page contains targets.
- [ ] Run tests; manually compare early, middle and final alphabetic pages plus every word-group section to the source. Record extraction limitations, not a completion claim.

### Task 2: Reconciled normalized inventory

**Files:** `normalize.py`, normalization tests, normalization overrides, `Inventory.json`, `Coverage.md`.

**Interfaces:** `normalize_occurrences(occurrences: list[dict], overrides: dict) -> dict` emits `occurrences` and `targets` arrays plus unresolved issues. IDs are persisted; appending/correcting a target must not renumber existing target IDs.

- [ ] Write failing tests for one occurrence mapping to several targets, duplicate occurrences mapping to one target, subordinate entries, regional variants, different senses, hyphenated continuations, and preservation of unresolved candidates.
- [ ] Implement normalization with explicit overrides for exceptions. Keep full source-occurrence mappings; no automatic deletion of uncertain rows.
- [ ] Review source occurrences section by section, resolving parsing/word-group/variant issues into teaching targets with word-type metadata. Explicitly distinguish a source synonym/expansion from an additional target.
- [ ] Build per-section coverage counts: source occurrences, normalized targets, variants, reviewed items and unresolved items; never force them to equal approximately 2,400.
- [ ] Run tests and reconcile every vocabulary-bearing page. If any source segment is not reviewed, label coverage partial and retain its open work in Preparation-Log.

### Task 3: Topic route, lesson assignments and A–Z index

**Files:** `render.py`, assignment tests, topic assignments, `README.md`, `Lesson-Index.md`, `A-Z.md`.

**Interfaces:** `assign_lessons(targets: list[dict], assignments: dict) -> list[dict]`; `render_navigation(inventory: dict, lessons: list[dict], output_dir: Path) -> None`.

- [ ] Write failing tests for unassigned targets, duplicate primary assignments, missing target IDs, revision appearances not increasing target counts, and sorting with German umlauts/ß while preserving spelling.
- [ ] Assign every target a primary everyday/topic lesson, retaining secondary topic tags. Put everyday themes first, with education/work/public-life, regional and exam-instruction coverage included rather than discarded.
- [ ] Use five targets by default, smaller verb/family groups where justified; insert a review lesson after each four new-word lessons, with a final review for any smaller final group. This is an implementation default, adjustable from learner evidence.
- [ ] Render all assigned lessons into the index with accurate preparation states, plus an A–Z entry for every target. Do not generate empty lesson notes and label them ready.
- [ ] Run assignment tests and verify every navigation link points to an existing note or an explicitly labelled not-yet-authored assignment without a broken clickable link.

### Task 4: Author and review complete self-study lesson batches

**Files:** original teaching-record JSON, `Lessons/`, per-batch Preparation-Log, teaching-record tests, renderer.

**Interfaces:** `render_lesson(lesson: dict, teaching: dict[str, dict]) -> str`; required content follows the approved spec. Original teaching records are authored/reviewed data, not generated translations assumed correct.

- [ ] Write failing content tests for missing Bengali meaning, noun forms, incomplete six-person verb forms, absent auxiliary/Partizip II/case information, missing exercises/answer keys and draft content marked ready.
- [ ] Author records in bounded batches of at most ten new-word lessons, with Bengali explanations and original German examples. For ambiguous senses, prepositions and regional forms, verify against primary dictionary/reference sources and cite the verification; do not guess.
- [ ] Include recognition, article/plural/form retrieval and short use exercises, separate answers and self-review. Mark alternative natural answers valid; do not force exact wording where meaning and grammar match.
- [ ] Render and review every batch for German forms, Bengali meaning, original examples and exercise/key consistency. Structural validation alone does not set `ready`; linguistic review is explicit per record.
- [ ] Add review-only lesson material for each completed group; check natural verb groups and active Präteritum staging against Agent.md.
- [ ] Repeat authoring and review until every assigned lesson is actually ready. A checkpoint delivery lists ready/draft/unwritten counts and pending work, never calls the full request complete early.

### Task 5: Integrate historical evidence and future-agent continuity

**Files:** existing word-type trackers; course entry point; Agent, Syllabus, Dashboard, README; resource/vocabulary/cheatsheet indices; Current-Progress and Revision-Queue.

**Interfaces:** `map_existing_records(targets: list[dict], tracker_paths: list[Path]) -> dict` returns canonical record keys and evidence links without changing historic statuses. `summarize_course(inventory: dict, lessons: list[dict], canonical_records: dict) -> dict` separates preparation, learning-status and dimension-specific evidence counts.

- [ ] Write failing regression tests that retain recorded statuses/evidence for Termin, Vertrag, Kunde, Meldung, defekt and the 2026-10-14 shopping nouns; mapping must not create a new assessment or overwrite exact answers.
- [ ] Map existing entries to course target IDs; keep unassessed future targets as planned inventory, not as thousands of newly learned words. Add canonical tracker entries as teaching occurs, or explicitly Not started if pre-registering targets; never default them to Introduced/Practiced.
- [ ] Make coverage views derive learning states from canonical trackers/dated evidence. Unknown recognition, recall or independent use stays unknown; use target denominators only for explicitly defined metrics, not overall B1 percentages.
- [ ] Link the course from operating instructions, syllabus, Dashboard, indices and reusable cheatsheet. Write the resume rule: check latest evidence and due review, then select the next suitable ready lesson, even with no fixed next lesson.
- [ ] Record project preparation without adding study minutes, practice scores or dated lecture sessions. Preserve pending historical revisions and the everyday-first preference.

### Task 6: Whole-course validation and handoff

**Files:** `validate.py`, integration tests, coverage report, Preparation-Log and final course entry point.

**Interfaces:** `validate_course(course_dir: Path, vault_dir: Path, require_complete: bool = False) -> list[dict]`; CLI exits nonzero on errors and, in complete mode, unresolved coverage or non-ready lessons.

- [ ] Write failing integration tests for orphan occurrence/target IDs, invalid canonical references, missing lessons, missing content review, broken internal links and contradictory summary denominators.
- [ ] Implement read-only validation and run all tests using bundled Python; validate the actual course with and without `--require-complete`.
- [ ] Inspect the beginning, middle and end of both A–Z and lesson index; open representative noun/verb/variant/review lessons as Markdown and check readable Obsidian links and separated answer keys. Review every lesson's readiness record, not just samples.
- [ ] Audit publication boundaries: private PDF/cache ignored; generated lessons do not copy publisher examples; no third-party licensing claim added.
- [ ] Reconcile all source sections and final ready/total counts. Only when complete-mode validation and linguistic/coverage review pass may the whole course be called prepared. Otherwise report exact remaining work and continuation state.
- [ ] Hand off the entry point, A–Z index, first ready lesson and honest progress summary. Start actual learning only as a separate evidence-backed practice session.

## Self-review

- Spec sections map to Tasks 1–6: source/coverage (1–2), lesson route (3), actual teaching content (4), historical progress/continuity (5), validation/publication (6).
- Five Review Focus risks have explicit fixtures or acceptance checks in their owning tasks.
- Functions and schemas above share the same keys; task outputs are later-task inputs. Implementation may refine helper functions without changing data ownership or evidence rules.
- Known environment constraint handled: bundled PDF runtime, no pdftotext installation assumed.
- No additional product decision remains beyond learner plan/execution-method review; exact audited target and lesson counts intentionally remain unknown.
