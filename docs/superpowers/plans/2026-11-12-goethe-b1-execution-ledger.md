# Execution ledger — plan: 2026-11-12-goethe-b1-vocabulary-course.md

Method: Native, explicitly selected by learner on 2026-11-12.
Spec: ../specs/2026-11-12-goethe-b1-vocabulary-course-design.md

## Pre-flight

- Task 1 → Task 2: extracted occurrences feed normalization; reviewed source coverage is a separate flag, never inferred from extraction success.
- Task 2 → Task 3: normalized target IDs persist; assignments must not renumber them.
- Tasks 3–4 → Task 5: prepared lesson readiness is not learned status; keep canonical trackers unchanged until evidence supports changes.
- Tasks 1–5 → Task 6: complete-mode checks must reject unresolved source coverage and unwritten/unreviewed lessons.

Ruling: Work additively in the requested existing vault, without Git/worktree helper scripts — git rev-parse confirms this is not a repository and the approved plan forbids initializing one — rollback is file-based, not commit-based; preserve this ledger rather than deleting the only execution record.

## Task state

1. Source extraction code: implemented, tests green; 104 pages processed, 2,877 occurrences retained. Full page reconciliation NOT complete.
2. Normalized inventory: provisional 2,732 candidates; 100 teaching targets checked. Full source coverage NOT complete; word-group pages remain explicitly open.
3. Topic assignments/navigation: starter 100 assigned; A–Z candidate lookup and lesson route rendered. 2,632 candidates remain unassigned/unreconciled; not a final remaining-word count.
4. Teaching material: starter GB1-L001–L020 and GB1-R001–R005 ready; remaining source lesson authoring pending.
5. Progress integration: course linked from Agent, README, Syllabus, Dashboard and vocabulary/resource/cheatsheet indices. No historical statuses, exact learner answers or study-time log changed.
6. Starter checkpoint validation and independent review performed. After one fix pass, 20/20 tests pass and actual partial validation passes. Complete validation intentionally remains red for coverage/unresolved occurrences/2,632 unassigned candidates. Full request is still in progress, NOT achieved.

## Evidence and implementation findings

- RED: initial 11 tests failed for absent implementation; extraction/normalization/render/validation then passed. New invariant-plural and partial-word-group tests were added before their fixes; review grouping and edited-lesson preservation also observed RED→GREEN.
- Parser bug identified and fixed: a trailing plural dash is not a truncated noun. `das Fenster, -` must remain a candidate.
- Word-group overrides can review selected targets without declaring the whole page reconciled.
- Review grouping spans every four new-word lessons, including across topic boundaries; no one-review-after-every-five-words inflation.
- Builder preflights generated lesson hashes and preserves learner edits; authoring inputs remain editable.
- Latest suite: bundled Python `-m unittest discover -s scripts/goethe_b1/tests -v` → 17/17 pass.

## Independent checkpoint review and one fix pass

Read-only reviewer Bernoulli examined code, all 100 authored records, 25 lesson renderings and navigation. No Critical findings; three Important findings reproduced with failing tests before the fixes:

- Final: fixed inherited/global content approval — `test_unreviewed_new_and_changed_content_cannot_be_ready` RED→GREEN. Approval is individual and tied to a digest of meaning/forms/example/exercise/key; a changed/new item is pending by default.
- Final: fixed stale-ready Markdown on downgrade — `test_withdrawn_lesson_is_explicitly_marked_without_losing_hash_history` RED→GREEN. Preserve learner edits, issue withdrawal notices and retain hash history.
- Final: fixed content-blind validation — `test_reviewed_markdown_must_match_metadata_and_answer_content` RED→GREEN. Frontmatter target/lesson metadata and reviewed teaching/key content are checked; marked learner notes/checkbox ticks are permitted.
- Fix-pass suite: 20/20 green. No reviewer re-dispatch; regression tests verify fixes. Deferred minors: none reported.
- Final navigation requirement check added canonical live-tracker links to A–Z without copying snapshot mastery states; `test_alphabetic_view_links_canonical_tracker_without_copying_mastery` observed RED→GREEN. Final suite: 21/21 green.

### Reviewer scope rulings

Final: Ruling: Exhaustive source coverage/cross-page/variant reconciliation is not certified — retain source_audit.complete=false, unresolved mappings and failing complete-mode validation — the remaining candidate list may still contain omissions, duplicates or merged entries, so it cannot be treated as a final exam word count.

Final: Ruling: Dictionary-level verification of every teaching statement is not claimed — author review and independent obvious-error review support the 100-target starter, while future ambiguous entries require reference checks — subtle usage/translation nuance may remain and should be corrected with new evidence.

Final: Ruling: Byte-for-byte historical preservation has no preimplementation snapshot — rely on additive write scope, read-only tracker mapping and retained dated evidence; do not claim a forensic comparison — an exact baseline comparison cannot be supplied retroactively.

Final: Ruling: B1 exam sufficiency is not inferred from a vocabulary starter — retain exam-readiness assessment as separate and unassessed here — finishing these words alone does not establish an exam pass.

## Handoff checkpoint

- Full course preparation is unfinished; next engineering work is exhaustive word-group/body source reconciliation and subsequent lesson authoring, not repeating this starter batch.
- Current deliverable: course README, candidate A–Z, 20 ready new-word + 5 review lessons (100 targets), structural safeguards, tests and preserved learner evidence.
- 25 lesson files; 23 course integration links checked; no 2026-11-12 assessed practice lecture created and no study minutes added.
- This ledger is intentionally retained: no Git history exists to replace it. No branch/merge/commit/cleanup operations apply to this vault.

No learner practice or study minutes are created by this preparation work.
