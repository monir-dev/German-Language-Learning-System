"""Regression tests for source coverage and honest course readiness."""
import copy
import importlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SCRIPTS))


def implementation(name):
    try:
        return importlib.import_module("goethe_b1." + name)
    except ModuleNotFoundError:
        return None


def approved_fixture(mod, authored):
    """A reviewer approves a specific content revision, not the whole input file."""
    authored = copy.deepcopy(authored)
    authored["content_approvals"] = {r["lemma"]: {"state": "reviewed", "digest": mod.record_digest(r)}
                                    for r in mod.authored_records(authored)}
    return authored


class ExtractionTests(unittest.TestCase):
    def test_checksum_mismatch_rejected_before_processing(self):
        mod = implementation("extract")
        self.assertIsNotNone(mod, "source identity guard not implemented")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.pdf"
            path.write_bytes(b"not the requested source")
            with self.assertRaisesRegex(ValueError, "SHA-256"):
                mod.verify_source(path, "expected")

    def test_headword_columns_do_not_capture_examples_or_headers(self):
        mod = implementation("extract")
        self.assertIsNotNone(mod, "layout extraction not implemented")
        lines = [
            {"x0": 35.2, "top": 20, "text": "WORTLISTE"},
            {"x0": 35.2, "top": 100, "text": "die Testkarte, -n"},
            {"x0": 35.2, "top": 111, "text": "(D)"},
            {"x0": 141.6, "top": 100, "text": "This is an example."},
            {"x0": 314.6, "top": 100, "text": "testbar"},
            {"x0": 421.1, "top": 100, "text": "Another example."},
            {"x0": 35.2, "top": 810, "text": "16"},
        ]
        result = mod.headword_blocks(lines, 16)
        self.assertEqual([x["raw"] for x in result], ["die Testkarte, -n (D)", "testbar"])
        self.assertEqual(result[0]["pdf_page"], 16)
        self.assertEqual(result[0]["section"], "alphabetic")

    def test_source_final_nonvocabulary_pages_not_counted_as_targets(self):
        mod = implementation("extract")
        self.assertIsNotNone(mod, "source section boundaries not implemented")
        self.assertEqual(mod.source_section(8), "word-groups")
        self.assertEqual(mod.source_section(102), "alphabetic")
        self.assertEqual(mod.source_section(103), "non-vocabulary")


class NormalizationTests(unittest.TestCase):
    def test_partially_reviewed_word_group_stays_open(self):
        mod = implementation("normalize")
        self.assertIsNotNone(mod)
        result = mod.normalize_occurrences([{"id": "group", "raw": "", "pdf_page": 13}],
            {"group": {"targets": [{"lemma": "Fisch", "word_type": "noun"}], "complete": False}})
        self.assertEqual(result["targets"][0]["normalization_state"], "reviewed")
        self.assertEqual(result["occurrences"][0]["disposition"], "needs_review")
        self.assertFalse(result["source_audit"]["complete"])

    def test_unchanged_noun_plural_dash_is_not_a_truncated_headword(self):
        mod = implementation("normalize")
        self.assertIsNotNone(mod)
        result = mod.normalize_occurrences([{"id": "o1", "raw": "das Fenster, -", "pdf_page": 40}], {})
        self.assertEqual([t["lemma"] for t in result["targets"]], ["Fenster"])

    def test_duplicate_occurrences_share_target_without_losing_mapping(self):
        mod = implementation("normalize")
        self.assertIsNotNone(mod, "normalization not implemented")
        rows = [{"id": "o1", "raw": "die Testkarte, -n", "pdf_page": 16},
                {"id": "o2", "raw": "die Testkarte, -n", "pdf_page": 17}]
        result = mod.normalize_occurrences(rows, {})
        self.assertEqual(len(result["targets"]), 1)
        self.assertEqual(result["targets"][0]["source_occurrence_ids"], ["o1", "o2"])
        self.assertEqual(len(result["occurrences"]), 2)

    def test_explicit_split_and_stable_ids_preserve_regional_variants(self):
        mod = implementation("normalize")
        self.assertIsNotNone(mod, "split mapping not implemented")
        rows = [{"id": "o1", "raw": "test form / variant", "pdf_page": 16}]
        overrides = {"o1": [{"lemma": "Testform", "word_type": "noun", "region": "D"},
                            {"lemma": "Testvariante", "word_type": "noun", "region": "A"}]}
        result = mod.normalize_occurrences(rows, overrides)
        self.assertEqual(len(result["occurrences"][0]["target_ids"]), 2)
        original_id = result["targets"][0]["id"]
        expanded = mod.normalize_occurrences(rows + [{"id": "o2", "raw": "anderes", "pdf_page": 18}], overrides)
        self.assertEqual(expanded["targets"][0]["id"], original_id)
        self.assertEqual([x["region"] for x in result["targets"]], ["D", "A"])

    def test_uncertain_and_hyphenated_entries_are_not_silently_accepted(self):
        mod = implementation("normalize")
        self.assertIsNotNone(mod, "uncertainty retention not implemented")
        result = mod.normalize_occurrences([{"id": "o1", "raw": "abge-", "pdf_page": 16}], {})
        self.assertEqual(result["occurrences"][0]["disposition"], "needs_review")
        self.assertEqual(result["occurrences"][0]["target_ids"], [])


class LessonTests(unittest.TestCase):
    def test_alphabetic_view_links_canonical_tracker_without_copying_mastery(self):
        mod = implementation("render")
        self.assertIsNotNone(mod)
        inventory = {"targets": [{"id": "t1", "lemma": "Termin", "word_type": "noun", "normalization_state": "reviewed"}],
                     "canonical_records": {"t1": {"tracker": "Vocabulary/Nouns/Noun-Tracker.md", "key": "der Termin", "status": "Needs revision"}}}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            mod.render_navigation(inventory, [], path)
            text = (path / "A-Z.md").read_text()
            self.assertIn("../../../Vocabulary/Nouns/Noun-Tracker.md", text)
            self.assertNotIn("Needs revision", text)

    def test_review_groups_span_small_topics_without_one_review_per_word_batch(self):
        mod = implementation("render")
        self.assertIsNotNone(mod)
        targets = [{"id": str(i), "lemma": "T" + str(i)} for i in range(20)]
        assignments = {"topic" + str(i): [str(j) for j in range(i * 5, i * 5 + 5)] for i in range(4)}
        result = mod.assign_lessons(targets, assignments)
        self.assertEqual([l["kind"] for l in result], ["new", "new", "new", "new", "review"])
        self.assertEqual(len(result[-1]["review_target_ids"]), 20)

    def test_every_target_assigned_once_and_review_does_not_add_targets(self):
        mod = implementation("render")
        self.assertIsNotNone(mod, "lesson assignment not implemented")
        targets = [{"id": "t" + str(i), "lemma": "Test" + str(i)} for i in range(21)]
        lessons = mod.assign_lessons(targets, {"alltag": [t["id"] for t in targets]})
        new = [l for l in lessons if l["kind"] == "new"]
        reviews = [l for l in lessons if l["kind"] == "review"]
        self.assertEqual(sum(len(l["target_ids"]) for l in new), 21)
        self.assertEqual(len(new), 5)
        self.assertEqual(len(reviews), 2)
        with self.assertRaisesRegex(ValueError, "duplicate"):
            mod.assign_lessons(targets, {"a": ["t0"], "b": ["t0"]})
        with self.assertRaisesRegex(ValueError, "unknown"):
            mod.assign_lessons(targets, {"a": ["missing"]})
        with self.assertRaisesRegex(ValueError, "unassigned"):
            mod.assign_lessons(targets, {"a": ["t0"]}, require_assigned=True)

    def test_ready_requires_bengali_noun_forms_and_reviewed_answers(self):
        mod = implementation("render")
        self.assertIsNotNone(mod, "content readiness checks not implemented")
        record = {"lemma": "Testkarte", "word_type": "noun", "review_state": "reviewed"}
        self.assertTrue(mod.teaching_issues(record))
        record.update({"bn_meanings": ["পরীক্ষার কার্ড"],
                       "grammar": {"article": "die", "plural": "Testkarten"},
                       "original_examples": [{"de": "Die Testkarte ist neu.", "bn": "কার্ডটি নতুন।"}],
                       "exercise": "পরীক্ষার কার্ড: article-সহ লেখো।", "answer": "die Testkarte"})
        self.assertEqual(mod.teaching_issues(record), [])
        draft = copy.deepcopy(record)
        draft["review_state"] = "draft"
        self.assertTrue(mod.teaching_issues(draft))

    def test_verb_must_have_six_forms_and_auxiliary(self):
        mod = implementation("render")
        self.assertIsNotNone(mod, "verb validation not implemented")
        record = {"lemma": "lernen", "word_type": "verb", "review_state": "reviewed",
                  "bn_meanings": ["শেখা"], "original_examples": [{"de": "Ich lerne.", "bn": "আমি শিখছি।"}],
                  "exercise": "শেখা: infinitive", "answer": "lernen", "grammar": {}}
        self.assertTrue(mod.teaching_issues(record))
        record["grammar"] = {"praesens": ["lerne", "lernst", "lernt", "lernen", "lernt", "lernen"],
                             "partizip_ii": "gelernt", "auxiliary": "haben", "praeteritum": "lernte",
                             "case": "Akkusativ where an object is expressed", "group": "regular"}
        self.assertEqual(mod.teaching_issues(record), [])


class ContinuityTests(unittest.TestCase):
    def test_unreviewed_new_and_changed_content_cannot_be_ready(self):
        mod = implementation("build")
        self.assertIsNotNone(mod)
        extraction = {"source": {}, "pages": [], "occurrences": [
            {"id": "o1", "raw": "lernen, lernt, lernte, hat gelernt", "pdf_page": 16}]}
        authored = {"review_state": "reviewed", "nouns": [], "modifiers": [], "source_overrides": {},
            "units": [{"topic": "Learning", "lemmas": ["lernen"]}], "verbs": [
                {"lemma": "lernen", "bn_meaning": "শেখা", "praesens": ["lerne", "lernst", "lernt", "lernen", "lernt", "lernen"],
                 "partizip_ii": "gelernt", "auxiliary": "haben", "praeteritum": "lernte", "case": "Akkusativ", "group": "regular",
                 "example_de": "Ich lerne Deutsch.", "example_bn": "আমি জার্মান শিখি।", "notes": "", "review_state": "needs_review"}]}
        self.assertNotEqual(mod.build_data(extraction, authored, [])["lessons"][0]["preparation_state"], "ready")
        authored["verbs"][0].pop("review_state")
        self.assertTrue(hasattr(mod, "record_digest"), "content-bound approval not implemented")
        approved = approved_fixture(mod, authored)
        self.assertEqual(mod.build_data(extraction, approved, [])["lessons"][0]["preparation_state"], "ready")
        approved["verbs"][0]["partizip_ii"] = "incorrect"
        self.assertNotEqual(mod.build_data(extraction, approved, [])["lessons"][0]["preparation_state"], "ready")

    def test_withdrawn_lesson_is_explicitly_marked_without_losing_hash_history(self):
        mod = implementation("build")
        self.assertIsNotNone(mod)
        extraction = {"source": {}, "pages": [], "occurrences": [{"id": "o1", "raw": "die Testkarte, -n", "pdf_page": 16}]}
        authored = {"review_state": "reviewed", "nouns": [["Testkarte", "die", "die Testkarten", "পরীক্ষার কার্ড", "Die Testkarte ist neu.", "কার্ডটি নতুন।", ""]],
            "modifiers": [], "verbs": [], "units": [{"topic": "Test", "lemmas": ["Testkarte"]}], "source_overrides": {}}
        if hasattr(mod, "record_digest"):
            authored = approved_fixture(mod, authored)
        bundle = mod.build_data(extraction, authored, [])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            mod.write_bundle(bundle, path)
            bundle["lessons"][0]["preparation_state"] = "draft"
            mod.write_bundle(bundle, path)
            text = (path / "Lessons/GB1-L001.md").read_text()
            self.assertNotIn('preparation_state: "ready"', text)
            self.assertIn("withdrawn", text)
            self.assertIn("GB1-L001.md", json.loads((path / "Data/Generated-Lesson-Hashes.json").read_text()))

    def test_rebuild_does_not_overwrite_learner_edited_lesson(self):
        mod = implementation("build")
        self.assertIsNotNone(mod)
        extraction = {"source": {"sha256": "x", "page_count": 104}, "pages": [],
            "occurrences": [{"id": "o1", "raw": "die Testkarte, -n", "pdf_page": 16}]}
        authored = {"review_state": "reviewed", "nouns": [["Testkarte", "die", "die Testkarten", "পরীক্ষার কার্ড", "Die Testkarte ist neu.", "কার্ডটি নতুন।", ""]],
            "modifiers": [], "verbs": [], "units": [{"topic": "Test", "lemmas": ["Testkarte"]}], "source_overrides": {}}
        authored = approved_fixture(mod, authored)
        bundle = mod.build_data(extraction, authored, [])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            mod.write_bundle(bundle, path)
            lesson = path / "Lessons/GB1-L001.md"
            edited = lesson.read_text() + "\nMy own note.\n"
            lesson.write_text(edited)
            with self.assertRaisesRegex(ValueError, "edited"):
                mod.write_bundle(bundle, path)
            self.assertEqual(lesson.read_text(), edited)

    def test_bundle_uses_authored_content_without_marking_new_words_learned(self):
        mod = implementation("build")
        self.assertIsNotNone(mod, "course build orchestration not implemented")
        extraction = {"source": {"sha256": "x", "page_count": 104}, "pages": [],
            "occurrences": [{"id": "o1", "raw": "die Testkarte, -n", "pdf_page": 16}]}
        authored = {"review_state": "reviewed", "nouns": [["Testkarte", "die", "die Testkarten", "পরীক্ষার কার্ড", "Die Testkarte ist neu.", "কার্ডটি নতুন।", ""]],
            "modifiers": [], "verbs": [], "units": [{"topic": "Test", "lemmas": ["Testkarte"]}], "source_overrides": {}}
        authored = approved_fixture(mod, authored)
        bundle = mod.build_data(extraction, authored, [])
        self.assertEqual(len(bundle["teaching"]), 1)
        self.assertEqual(bundle["lessons"][0]["preparation_state"], "ready")
        self.assertNotIn("status", bundle["inventory"]["targets"][0])
        self.assertEqual(bundle["inventory"]["canonical_records"], {})

    def test_mapping_preserves_historic_status_and_never_writes_tracker(self):
        mod = implementation("normalize")
        self.assertIsNotNone(mod, "canonical tracker mapping not implemented")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "Noun-Tracker.md"
            text = "| Noun | Meaning | Gender | Plural | Useful phrase | Status | Evidence |\n|---|---|---|---|---|---|---|\n| der Termin | appointment | der | die Termine | einen Termin haben | Needs revision | [[old-lecture]] |\n"
            path.write_text(text)
            result = mod.map_existing_records([{"id": "t1", "lemma": "Termin", "word_type": "noun"}], [path])
            self.assertEqual(result["t1"]["status"], "Needs revision")
            self.assertIn("old-lecture", result["t1"]["evidence"])
            self.assertEqual(path.read_text(), text)


class ValidationTests(unittest.TestCase):
    def test_reviewed_markdown_must_match_metadata_and_answer_content(self):
        builder, validator = implementation("build"), implementation("validate")
        self.assertIsNotNone(builder)
        extraction = {"source": {}, "pages": [], "occurrences": [{"id": "o1", "raw": "die Testkarte, -n", "pdf_page": 16}]}
        authored = {"review_state": "reviewed", "nouns": [["Testkarte", "die", "die Testkarten", "পরীক্ষার কার্ড", "Die Testkarte ist neu.", "কার্ডটি নতুন।", ""]],
            "modifiers": [], "verbs": [], "units": [{"topic": "Test", "lemmas": ["Testkarte"]}], "source_overrides": {}}
        if hasattr(builder, "record_digest"):
            authored = approved_fixture(builder, authored)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            builder.write_bundle(builder.build_data(extraction, authored, []), path)
            note = path / "Lessons/GB1-L001.md"
            text = note.read_text().replace('target_ids: [', 'target_ids: ["nonexistent", ')
            text = text.replace("die Testkarte; plural: die Testkarten", "das Testkarte; plural: wrong")
            note.write_text(text)
            issues = validator.validate_course(path, path)
            codes = {i["code"] for i in issues}
            self.assertIn("lesson_metadata_mismatch", codes)
            self.assertIn("lesson_content_changed", codes)

    def test_orphan_source_mapping_is_an_integrity_error_even_in_partial_mode(self):
        mod = implementation("validate")
        self.assertIsNotNone(mod)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path / "Data").mkdir()
            (path / "Inventory.json").write_text(json.dumps({"targets": [], "occurrences": [
                {"id": "o1", "target_ids": ["missing"], "disposition": "needs_review"}],
                "source_audit": {"complete": False}}))
            (path / "Data/Lessons.json").write_text("[]")
            (path / "Data/Teaching.json").write_text("{}")
            self.assertTrue(any(i["code"] == "orphan_mapping" for i in mod.validate_course(path, path)))

    def test_incomplete_course_allowed_only_when_not_claimed_complete(self):
        mod = implementation("validate")
        self.assertIsNotNone(mod, "honest completion gate not implemented")
        with tempfile.TemporaryDirectory() as directory:
            course = Path(directory)
            (course / "Inventory.json").write_text(json.dumps({"targets": [], "occurrences": [],
                "source_audit": {"complete": False, "pending_pages": [8]}}))
            (course / "Data").mkdir()
            (course / "Data/Lessons.json").write_text("[]")
            (course / "Data/Teaching.json").write_text("{}")
            issues = mod.validate_course(course, course, require_complete=True)
            self.assertTrue(any(i["code"] == "coverage_incomplete" for i in issues))
            self.assertTrue(any(i["code"] == "empty_inventory" for i in issues))


if __name__ == "__main__":
    unittest.main()
