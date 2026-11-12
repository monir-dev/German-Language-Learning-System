# Goethe B1 Vocabulary Course — Design

Date: 2026-11-12
Status: Approved by learner on 2026-11-12 (reply: "okay")
Selected approach: Topic-wise lessons + A–Z index
Builder review: Completed 2026-11-12; independent reviewer reported "nothing important left". This is a design-clarity review, not source coverage or lesson-content verification.

## Intent and agreed requirements

The learner wants to work through the vocabulary in the supplied official Goethe-Zertifikat B1 Wortliste, one manageable lesson at a time, to support passing B1 and everyday communication. Professional vocabulary remains included but everyday vocabulary takes priority. The learner chose topic-wise lessons with an A–Z index on 2026-11-12.

Keep everything in this existing local Obsidian vault. Use Bengali explanations, German words and examples, standard Markdown and YAML; no new app, required plugin or cloud document. Preserve all existing vocabulary and dated learner evidence. Future agents must be able to continue without chat history.

Source: https://www.goethe.de/pro/relaunch/prf/en/Goethe-Zertifikat_B1_Wortliste.pdf
Local source: `External Resources/Goethe-Zertifikat_B1_Wortliste.pdf`
The downloaded file was verified as a 104-page PDF. The publisher describes approximately 2,400 lexical units; that is not a verified count of imported rows, senses, headwords or lessons.
Verified source SHA-256: `8860f7f0c916831b2365f66239a3ceba3be81ddba28e1224846ca8420807fe42`.

## Approaches considered

1. Topic-first lessons with an alphabetical lookup and source-coverage checklist: related words are learned together, everyday topics can come first, and omissions can be audited. Requires explicit mapping between source entries, vocabulary records and lessons. Selected by the learner.
2. Follow the PDF's A–Z order in small lessons: simplest source comparison, but adjacent entries do not necessarily make a useful everyday lesson. Not selected as the teaching sequence; retain alphabetical order for lookup only.

## Goals, non-goals and failure conditions

Goals:
- Account for all vocabulary-bearing source sections, including the preliminary word groups, alphabetic headwords, subordinate entries and regional variants.
- Prepare an auditable inventory, topic sequence, A–Z lookup, self-study lessons, review guidance and evidence-linked progress views.
- Supply original Bengali explanations and German teaching examples rather than copying source example sentences.
- Distinguish preparation, comprehension, recall and independent use.

Non-goals:
- Guarantee an exam pass or claim that word memorization alone establishes B1.
- Treat approximately 2,400 as an exact denominator or assign a completion date before auditing scope and learner recall.
- Add speaking/listening assessment against the learner's existing class-first preference.
- Replace existing trackers, reset old progress, or create a second conflicting learning-status database.
- Publish the official PDF or a copied collection of its example sentences as open-source content.

Failure conditions: silently omitted source sections; copied examples presented as original; plausible but unchecked translations or forms marked verified; empty lesson stubs called ready; lesson files mistaken for completed practice; old guided results upgraded to mastery.

## Inventory and coverage

Create a course area under `Vocabulary/Wordlists/Goethe-B1/`, without moving existing resources or trackers.

Proposed components (builder may adjust filenames, not these responsibilities):
- `README.md`: course entry point, current preparation state, topic route, how to study and resume.
- `Source-Manifest.md`: URL, download date, PDF identity/hash, page count, rights note and extraction method.
- `Coverage.md`: coverage by source section/page range, unresolved extraction items and reconciled counts.
- `Inventory.json`: structured source-occurrence map and normalized learning targets; generated readable Markdown views must be available without running code.
- `A-Z.md`: every accounted target, topic, lesson link and canonical vocabulary-record reference.
- `Lesson-Index.md`: ordered lessons, target IDs, topic and preparation readiness, separate from learner results.
- `Lessons/`: actual reusable self-study lesson notes.

Every source occurrence needs a stable occurrence ID, printed/PDF page reference, source section, normalized target key and an explicit disposition. A source occurrence may map to multiple targets (for example separately teachable gender forms); multiple occurrences may map to one target. Retain all mappings rather than silently deduplicating.

Each normalized target needs a stable ID, lemma/phrase, word type, region where relevant, primary topic, related topics, source occurrence IDs and primary lesson assignment. Articles, plural, separable/reflexive forms and senses must not be lost when useful for learning. Mark difficult parsing or grammatical ambiguity as needing review, never silently guess.

Count source occurrences, normalized targets, regional variants, reviewed targets and lesson assignments separately. The approximate publisher count is contextual only. A coverage-complete claim requires every relevant page/section reconciled, zero unresolved omissions and each target assigned to a primary lesson. Repeated revision appearances are not new words.

## Course order and lesson size — proposed defaults

These are teacher proposals, not additional learner decisions:
- Start with high-utility everyday themes: personal information and people; routines and time; shopping and food; home; travel; health; appointments and services; communication; education, work and public life.
- Preserve coverage of less frequent, regional and exam-instruction items in later lessons; do not drop them because everyday vocabulary is prioritized.
- Use normally five target words/phrases per new-word lesson. A word-family or difficult verb lesson may use fewer. This is an adaptable learning unit, not five guaranteed mastered words per day.
- Keep relevant word types together by topic, with separate noun/verb/adjective/phrase lookup through the established trackers.
- Prefer Germany's standard forms first for everyday production while labelling Austrian/Swiss variants accurately; teach recognition of the variants rather than erasing them.
- Include a review-only lesson after a small group of new-word lessons and short retrieval at later sessions. Proposed review intervals are next session, about three days, one week and a later check; adapt to actual attendance and errors. No reminder automation is implied.

Do not call all lessons ready until they contain actual teaching material, exercises and answer keys. If preparation must be delivered in batches, state exactly which lessons are ready and which remain draft; preparing a complete map is not preparing the complete lesson set.

## Self-study lesson contract

Each prepared lesson has YAML identifying course/lesson ID, topic, target IDs, source references and preparation state. Preparation does not have a practice date, score or studied status.

Learner-facing content:
1. A short Bengali learning goal and small retrieval review.
2. Each target's Bengali meaning and relevant usage distinction.
3. Nouns: article, singular, plural and a useful phrase.
4. Verbs: infinitive, full Präsens forms, Partizip II, Perfekt auxiliary and case/preposition; identify separable/reflexive and regular/irregular patterns. Include/reference Präteritum, but stage active memorization under the existing priority policy.
5. Adjectives/adverbs/phrases: natural use and meaningful contrast where useful; do not invent an opposite just to fill a column.
6. Original short German examples with Bengali explanations and context-appropriate meanings.
7. Meaning/recognition, article/plural/form retrieval, and a small usage exercise; a separate answer key that accepts natural alternatives.
8. Self-review checklist and review prompts.

Prepared lessons live separately from `Lectures/`. Actual sessions continue to produce dated lectures with exact learner answers and corrections, linking the reusable lesson and target IDs. Unanswered exercises stay pending, never scored.

## Progress and continuity

- Existing word-type trackers remain the canonical learning-status records. Extend them with stable target references as needed without discarding rows or evidence.
- The new course inventory is canonical for source mapping and planned assignments, not a competing source of learned status. Course summaries derive learning state from the word-type trackers and dated lectures.
- Keep `Memory/Current-Progress.md` authoritative for current teaching state and next-step selection; Dashboard is a linked summary.
- Track preparation coverage separately from recognition, recall and independent-use evidence. Recognizing a word does not imply active production; successful immediate repetition is not delayed retention.
- Map existing words to course targets without resetting their status or inventing a course assessment. Historical evidence retains its original scope. Untested mappings are explicitly unassessed.
- Preserve `Not started`, `Learning`, `Practiced`, `Needs revision`, `Stable`. These are not automatic percentages of B1 skill. Any quantitative view names its denominator and evidence criterion; unknown evidence is labelled unknown.
- Future agents read the course entry point, current progress, due revisions and latest dated lecture, then select a short recall check plus the next suitable topic lesson. They can derive a starting point even if no fixed next lesson is recorded.
- Update Agent.md, Syllabus, vocabulary/resource/cheatsheet indices and Dashboard to point to the course, without counting preparation time as learner study time.

## Validation and publication boundaries

- Verify the source identity and page count; inspect representative pages and the word-group sections, not just the alphabetic body.
- Reconcile extraction to source sections, handle multi-column text and source-page breaks, and retain an unresolved-item report until checked.
- Validate target/occurrence IDs, mappings, duplicate handling, primary lesson assignments, links, YAML and required lesson content.
- Check Bengali meanings, German spelling/forms, grammatical roles and answer keys; record uncertainties for review rather than presenting bulk output as verified.
- Keep the official PDF and verbatim extraction caches private and ignored by Git. Do not include the publisher's example sentences in generated lessons. Rights status for any future publication is a separate review; no open-license claim is made for third-party material or source-derived collections.
- Existing evidence is not a readiness test for the new course. No invented 2026-11-12 practice session or elapsed study time.

## Delivery order and acceptance

After design approval: write the implementation plan; establish source audit and normalized inventory; map targets to topic lessons and A–Z lookup; author and check the lessons in explicit batches; integrate progress views and continuity guidance; validate the result.

The full request is complete only when the source coverage is reconciled, all target assignments exist, all promised lesson notes contain usable checked teaching material, indices resolve, and old progress is preserved. A partial delivery must disclose remaining extraction, review or lesson-authoring work and must not be described as the whole course finished.

## Builder discretion and approval

Builder may select local extraction libraries already available, parser implementation, exact filenames, topic subdivisions and batch-writing order. Do not install unnecessary dependencies or change the established local Markdown medium. Detailed lesson count follows the audited inventory, not an assumed 2,400/5 calculation.

The learner approved this design on 2026-11-12, including the proposed five-target default and prepared-lessons-versus-dated-lectures separation. Implementation planning follows; approval of the design is not evidence that the course has been built or studied.
