"""Build Markdown/JSON views from explicitly authored content and private source candidates."""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re

try:
    from .normalize import normalize_occurrences, guess_target, map_existing_records
    from .render import assign_lessons, teaching_issues, render_lesson, render_navigation, lesson_filename
except ImportError:
    from normalize import normalize_occurrences, guess_target, map_existing_records
    from render import assign_lessons, teaching_issues, render_lesson, render_navigation, lesson_filename


def authored_records(data):
    records = []
    for lemma, article, plural, meaning, de, bn, notes in data["nouns"]:
        records.append({"lemma": lemma, "word_type": "noun", "bn_meanings": [meaning],
            "grammar": {"article": article, "plural": plural}, "usage_notes": notes,
            "original_examples": [{"de": de, "bn": bn}],
            "exercise": meaning + " — noun ও article লেখো; plural-ও মনে করার চেষ্টা করো।",
            "answer": article + " " + lemma + "; plural: " + plural})
    for lemma, word_type, meaning, de, bn, notes in data["modifiers"]:
        records.append({"lemma": lemma, "word_type": word_type, "bn_meanings": [meaning],
            "grammar": {}, "usage_notes": notes, "original_examples": [{"de": de, "bn": bn}],
            "exercise": meaning + " — German word লেখো।", "answer": lemma})
    for verb in data["verbs"]:
        records.append({"lemma": verb["lemma"], "word_type": "verb", "bn_meanings": [verb["bn_meaning"]],
            "grammar": {key: verb[key] for key in ["praesens", "partizip_ii", "auxiliary", "praeteritum", "case", "group"]},
            "usage_notes": verb["notes"], "original_examples": [{"de": verb["example_de"], "bn": verb["example_bn"]}],
            "exercise": verb["bn_meaning"] + " — infinitive ও Partizip II লেখো; ich-form বলো।",
            "answer": f"{verb['lemma']}; {verb['partizip_ii']}; ich {verb['praesens'][0]}"})
    blocked = {v["lemma"] for v in data["verbs"] if v.get("review_state") == "needs_review"}
    for record in records:
        approval = data.get("content_approvals", {}).get(record["lemma"], {})
        approved = (record["lemma"] not in blocked and approval.get("state") == "reviewed"
                    and approval.get("digest") == record_digest(record))
        record["review_state"] = "reviewed" if approved else "needs_review"
        record["reviewed_content_digest"] = approval.get("digest") if approved else None
        record["content_review_basis"] = approval.get("basis", "Individual content approval pending")
    return records


def record_digest(record):
    """Approval binds to content, not status flags, page refs or generated IDs."""
    keys = ["lemma", "word_type", "bn_meanings", "grammar", "usage_notes", "original_examples", "exercise", "answer"]
    content = {key: record.get(key) for key in keys}
    return hashlib.sha256(json.dumps(content, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def build_data(extraction, authoring, tracker_paths):
    records = authored_records(authoring)
    occurrences = extraction["occurrences"]
    preliminary = normalize_occurrences(occurrences, {})
    preliminary_targets = preliminary["targets"]
    occurrence_map = {o["id"]: o for o in occurrences}
    overrides = {}
    record_occurrences = {}
    for record in records:
        oid = authoring.get("source_overrides", {}).get(record["lemma"])
        if not oid:
            matches = [t for t in preliminary_targets if t["lemma"] == record["lemma"]]
            if not matches:
                raise ValueError("No source mapping for authored word: " + record["lemma"])
            oid = matches[0]["source_occurrence_ids"][0]
        if oid not in occurrence_map:
            raise ValueError("Source override occurrence not found: " + oid)
        record_occurrences[record["lemma"]] = oid
        override = overrides.setdefault(oid, {"targets": [], "complete": False})
        override["targets"].append({"lemma": record["lemma"], "word_type": record["word_type"], "region": None})
    for oid, override in overrides.items():
        original = guess_target(occurrence_map[oid].get("raw", ""))
        if original and original["lemma"] not in {t["lemma"] for t in override["targets"]}:
            override["targets"].append({**original, "reviewed": False})
    inventory = normalize_occurrences(occurrences, overrides)
    inventory["source"] = extraction["source"]
    inventory["source_pages"] = extraction.get("pages", [])
    targets = inventory["targets"]
    by_lemma = {t["lemma"]: t for t in targets if t["normalization_state"] == "reviewed"}
    teaching = {}
    for record in records:
        target = by_lemma[record["lemma"]]
        oid = record_occurrences[record["lemma"]]
        record.update({"target_id": target["id"], "pdf_pages": [occurrence_map[oid]["pdf_page"]]})
        teaching[target["id"]] = record
    assignments = {unit["topic"]: [by_lemma[word]["id"] for word in unit["lemmas"]] for unit in authoring["units"]}
    lessons = assign_lessons(targets, assignments)
    for lesson in lessons:
        tids = lesson["target_ids"] or lesson["review_target_ids"]
        lesson["source_refs"] = sorted({page for tid in tids for page in teaching[tid]["pdf_pages"]})
        if all(not teaching_issues(teaching[tid]) for tid in tids):
            lesson["preparation_state"] = "ready"
        if lesson["kind"] == "review":
            lesson["topic"] = "Mixed revision — " + lesson["id"]
        for tid in lesson["target_ids"]:
            target = next(t for t in targets if t["id"] == tid)
            target["primary_topic"] = lesson["topic"]
            target["primary_lesson_id"] = lesson["id"]
    canonical = map_existing_records(targets, tracker_paths)
    inventory["canonical_records"] = canonical
    for target in targets:
        if target["id"] in canonical:
            record = canonical[target["id"]]
            target["canonical_record_key"] = record["tracker"] + " :: " + record["key"]
    return {"inventory": inventory, "teaching": teaching, "lessons": lessons,
            "content_approvals": authoring.get("content_approvals", {}),
            "overrides": overrides, "assignments": assignments}


def write_bundle(bundle, course):
    course = Path(course)
    hashes_path = course / "Data/Generated-Lesson-Hashes.json"
    old_hashes = json.loads(hashes_path.read_text()) if hashes_path.exists() else {}
    rendered = {}
    # Preflight before any write: respect Obsidian notes/checkmarks added by the learner.
    for lesson in bundle["lessons"]:
        if lesson["preparation_state"] != "ready":
            continue
        filename = lesson_filename(lesson)
        text = render_lesson(lesson, bundle["teaching"])
        path = course / "Lessons" / filename
        if path.exists():
            existing = path.read_text(encoding="utf-8")
            old_digest = hashlib.sha256(existing.encode()).hexdigest()
            if filename in old_hashes:
                if old_digest != old_hashes[filename]:
                    raise ValueError("Learner-edited lesson preserved; reconcile before rebuild: " + filename)
            elif existing != text:
                raise ValueError("Existing edited lesson has no generated hash; preserve it: " + filename)
        rendered[filename] = text
    # Retired/downgraded files retain a withdrawal notice, never stale ready content.
    for filename, old_digest in old_hashes.items():
        if filename in rendered:
            continue
        path = course / "Lessons" / filename
        if not path.exists():
            continue
        existing = path.read_text(encoding="utf-8")
        if hashlib.sha256(existing.encode()).hexdigest() != old_digest:
            raise ValueError("Learner-edited withdrawn lesson preserved; reconcile first: " + filename)
        rendered[filename] = ('---\npreparation_state: "withdrawn"\n---\n\n# Withdrawn lesson\n\n'
            '> এই lesson-এর approval বা assignment বদলেছে। Source data review না হওয়া পর্যন্ত ব্যবহার করবে না।\n'
            '\nএই notice পুরোনো ready content-এর জায়গায় আছে; original teaching data Data/Authoring.json-এ থাকে।\n')
    (course / "Data").mkdir(parents=True, exist_ok=True)
    (course / "Lessons").mkdir(exist_ok=True)
    for path, obj in [("Inventory.json", bundle["inventory"]), ("Data/Teaching.json", bundle["teaching"]),
                      ("Data/Lessons.json", bundle["lessons"]), ("Data/Normalization-Overrides.json", bundle["overrides"]),
                      ("Data/Topic-Assignments.json", bundle["assignments"]),
                      ("Data/Content-Approvals.json", bundle.get("content_approvals", {}))]:
        (course / path).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for filename, text in rendered.items():
        (course / "Lessons" / filename).write_text(text, encoding="utf-8")
    new_hashes = {filename: hashlib.sha256(text.encode()).hexdigest() for filename, text in rendered.items()}
    history_path = course / "Data/Generated-Lesson-Hash-History.json"
    history = json.loads(history_path.read_text()) if history_path.exists() else {}
    for filename, digest in old_hashes.items():
        if digest != new_hashes.get(filename) and digest not in history.setdefault(filename, []):
            history[filename].append(digest)
    history_path.write_text(json.dumps(history, indent=2) + "\n", encoding="utf-8")
    hashes_path.write_text(json.dumps({**old_hashes, **new_hashes}, indent=2) + "\n", encoding="utf-8")
    render_navigation(bundle["inventory"], bundle["lessons"], course)
    inventory, lessons = bundle["inventory"], bundle["lessons"]
    stats = {"source_occurrences": len(inventory["occurrences"]), "candidate_targets": len(inventory["targets"]),
             "reviewed_teaching_targets": sum(not teaching_issues(r) for r in bundle["teaching"].values()),
             "ready_new_lessons": sum(l["kind"] == "new" and l["preparation_state"] == "ready" for l in lessons),
             "ready_review_lessons": sum(l["kind"] == "review" and l["preparation_state"] == "ready" for l in lessons),
             "unassigned_candidates": sum(not t["primary_lesson_id"] for t in inventory["targets"]),
             "source_coverage_complete": False}
    (course / "Data/Preparation-Counts.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    rows = ["# Source coverage — incomplete", "", "> নিচের সংখ্যা preparation/extraction-এর; শেখা শব্দ বা B1 proficiency নয়।", "",
            "| Metric | Count |", "|---|---:|"] + [f"| {key} | {value} |" for key, value in stats.items()]
    rows += ["", "## Page audit", "", "Selected teaching targets have checked source references; this does not reconcile every entry on their page.", "",
             "| PDF page | Section | Candidate occurrences | Reconciled |", "|---:|---|---:|---|"]
    counts = Counter(o["pdf_page"] for o in inventory["occurrences"])
    for meta in inventory["source_pages"]:
        if meta["section"] != "non-vocabulary":
            rows += [f"| {meta['pdf_page']} | {meta['section']} | {counts[meta['pdf_page']]} | No — source review remains |"]
    rows += ["", "## What remains", "", "- Word groups: full target mapping and deduplication, including variants, numbers, dates and expressions.",
             "- Alphabetic candidates: reconcile all blocks and split subordinate/merged entries; keep uncertain items visible.",
             "- Assign remaining reviewed targets to meaningful topics and author their lessons.",
             "- Re-run complete-mode validation. It must fail while this work remains.", ""]
    (course / "Coverage.md").write_text("\n".join(rows), encoding="utf-8")
    return stats


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--vault", type=Path, default=Path("."))
    args = cli.parse_args()
    vault = args.vault.resolve()
    course = vault / "Vocabulary/Wordlists/Goethe-B1"
    extraction = json.loads((vault / "External Resources/Goethe-B1-private-cache/extraction.json").read_text())
    authoring = json.loads((course / "Data/Authoring.json").read_text())
    approvals_path = course / "Data/Content-Approvals.json"
    authoring["content_approvals"] = json.loads(approvals_path.read_text()) if approvals_path.exists() else {}
    tracker_paths = [vault / p for p in ["Vocabulary/Nouns/Noun-Tracker.md", "Vocabulary/Verbs/Verb-Tracker.md",
        "Vocabulary/Adjectives/Adjective-Tracker.md", "Vocabulary/Adverbs-and-Phrases/Adverb-Phrase-Tracker.md"]]
    bundle = build_data(extraction, authoring, tracker_paths)
    for record in bundle["inventory"]["canonical_records"].values():
        record["tracker"] = str(Path(record["tracker"]).relative_to(vault))
    for target in bundle["inventory"]["targets"]:
        if target["id"] in bundle["inventory"]["canonical_records"]:
            r = bundle["inventory"]["canonical_records"][target["id"]]
            target["canonical_record_key"] = r["tracker"] + " :: " + r["key"]
    print(json.dumps(write_bundle(bundle, course), ensure_ascii=False, indent=2))
