"""Read-only integrity validation; complete mode is deliberately strict."""
import argparse
import json
from pathlib import Path
import re

try:
    from .render import teaching_issues, lesson_filename, render_lesson
    from .build import record_digest
except ImportError:
    from render import teaching_issues, lesson_filename, render_lesson
    from build import record_digest


def frontmatter(text):
    if not text.startswith("---\n"):
        raise ValueError("Missing frontmatter")
    block = text.split("\n---\n", 1)[0][4:]
    result = {}
    for line in block.splitlines():
        key, value = line.split(":", 1)
        result[key] = json.loads(value.strip())
    return result


def reviewed_body(text):
    text = re.sub(r"<!-- learner-notes:start -->.*?<!-- learner-notes:end -->", "<!-- learner-notes:start --><!-- learner-notes:end -->", text, flags=re.S)
    return re.sub(r"(?m)^- \[[xX]\]", "- [ ]", text).strip()


def validate_course(course_dir, vault_dir, require_complete=False):
    course_dir, vault_dir = Path(course_dir), Path(vault_dir)
    issues = []

    def issue(code, detail):
        issues.append({"code": code, "detail": detail})

    try:
        inventory = json.loads((course_dir / "Inventory.json").read_text())
        lessons = json.loads((course_dir / "Data/Lessons.json").read_text())
        teaching = json.loads((course_dir / "Data/Teaching.json").read_text())
    except (OSError, ValueError) as exc:
        return [{"code": "unreadable_data", "detail": str(exc)}]
    target_ids = [t["id"] for t in inventory["targets"]]
    target_map = {t["id"]: t for t in inventory["targets"]}
    approvals_path = course_dir / "Data/Content-Approvals.json"
    approvals = json.loads(approvals_path.read_text()) if approvals_path.exists() else {}
    occurrences = {o["id"]: o for o in inventory["occurrences"]}
    if len(target_ids) != len(set(target_ids)):
        issue("duplicate_target_id", "Duplicate target ID")
    if len(occurrences) != len(inventory["occurrences"]):
        issue("duplicate_occurrence_id", "Duplicate occurrence ID")
    for occurrence in occurrences.values():
        for tid in occurrence["target_ids"]:
            if tid not in target_map:
                issue("orphan_mapping", occurrence["id"] + " -> " + tid)
    for target in target_map.values():
        for oid in target["source_occurrence_ids"]:
            if oid not in occurrences or target["id"] not in occurrences[oid]["target_ids"]:
                issue("orphan_source", target["id"] + " -> " + oid)
    primary = set()
    lesson_ids = set()
    for lesson in lessons:
        if lesson["id"] in lesson_ids:
            issue("duplicate_lesson_id", lesson["id"])
        lesson_ids.add(lesson["id"])
        for tid in lesson["target_ids"]:
            if tid in primary:
                issue("duplicate_assignment", tid)
            primary.add(tid)
        ids = lesson["target_ids"] or lesson["review_target_ids"]
        if any(tid not in target_map for tid in ids):
            issue("unknown_target", lesson["id"])
        if lesson["preparation_state"] == "ready":
            path = course_dir / "Lessons" / lesson_filename(lesson)
            if not path.is_file():
                issue("missing_lesson", lesson["id"])
            else:
                text = path.read_text(encoding="utf-8")
                for heading in ("## আজকের লক্ষ্য", "## নিজে practice করো", "## Answer key", "## Self-review", "## Agent note"):
                    if heading not in text:
                        issue("incomplete_lesson", lesson["id"] + ": " + heading)
                if not text.startswith("---\n") or "\n---\n" not in text[4:]:
                    issue("missing_frontmatter", lesson["id"])
                try:
                    meta = frontmatter(text)
                    expected = {"course": "Goethe-B1", "lesson_id": lesson["id"], "topic": lesson["topic"],
                        "kind": lesson["kind"], "target_ids": lesson["target_ids"],
                        "review_target_ids": lesson["review_target_ids"], "source_refs": lesson.get("source_refs", []),
                        "preparation_state": "ready", "assessment_state": "not-assessed-in-this-lesson"}
                    if any(meta.get(key) != value for key, value in expected.items()):
                        issue("lesson_metadata_mismatch", lesson["id"])
                except (ValueError, IndexError):
                    issue("lesson_metadata_mismatch", lesson["id"] + ": invalid generated frontmatter")
                try:
                    if reviewed_body(text) != reviewed_body(render_lesson(lesson, teaching)):
                        issue("lesson_content_changed", lesson["id"] + ": teaching/key revision differs; review required")
                except (KeyError, ValueError):
                    issue("lesson_content_changed", lesson["id"] + ": cannot reconstruct reviewed content")
            for tid in ids:
                errors = teaching_issues(teaching.get(tid, {}))
                if errors:
                    issue("unreviewed_content", tid + ": " + "; ".join(errors))
                record = teaching.get(tid, {})
                approval = approvals.get(record.get("lemma"), {})
                if approval.get("state") != "reviewed" or approval.get("digest") != record_digest(record):
                    issue("content_approval_mismatch", tid)
        else:
            path = course_dir / "Lessons" / lesson_filename(lesson)
            if path.exists() and 'preparation_state: "ready"' in path.read_text(encoding="utf-8"):
                issue("stale_ready_lesson", lesson["id"])
    for tid, record in inventory.get("canonical_records", {}).items():
        if tid not in target_map or not (vault_dir / record["tracker"]).is_file():
            issue("invalid_canonical_reference", tid)
    for path in course_dir.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for dest in re.findall(r"\]\(<([^>]+)>\)", text):
            if not re.match(r"\w+://", dest) and not (path.parent / dest.split("#")[0]).is_file():
                issue("broken_link", str(path.relative_to(course_dir)) + " -> " + dest)
    if require_complete:
        if not target_ids:
            issue("empty_inventory", "No learning targets")
        if not inventory.get("source_audit", {}).get("complete"):
            issue("coverage_incomplete", "All source pages/occurrences have not been reconciled")
        if any(o["disposition"] == "needs_review" for o in occurrences.values()):
            issue("unresolved_occurrences", "Source candidates still require review")
        if set(target_ids) != primary:
            issue("unassigned_targets", str(len(set(target_ids) - primary)))
        if not lessons or any(l["preparation_state"] != "ready" for l in lessons):
            issue("lessons_incomplete", "Not every lesson is ready")
    return issues


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("course", type=Path)
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    errors = validate_course(args.course, args.vault, args.require_complete)
    print(json.dumps({"valid": not errors, "require_complete": args.require_complete, "issues": errors}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(errors))
