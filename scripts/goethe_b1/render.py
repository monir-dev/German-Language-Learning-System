"""Lesson/navigation rendering. A generated file is not a learning result."""
import json
from pathlib import Path
import re


def german_sort_key(text):
    value = text.casefold()
    for old, new in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        value = value.replace(old, new)
    return value


def assign_lessons(targets, assignments, require_assigned=False):
    known = {target["id"] for target in targets}
    used, lessons, group = set(), [], []
    for topic, tids in assignments.items():
        if any(tid not in known for tid in tids):
            raise ValueError("unknown target in assignments")
        if any(tid in used for tid in tids) or len(tids) != len(set(tids)):
            raise ValueError("duplicate primary target assignment")
        used.update(tids)
        for offset in range(0, len(tids), 5):
            lid = f"GB1-L{1 + sum(l['kind'] == 'new' for l in lessons):03d}"
            chunk = tids[offset:offset + 5]
            lessons.append({"id": lid, "topic": topic, "kind": "new", "target_ids": chunk,
                            "review_target_ids": [], "preparation_state": "draft"})
            group.extend(chunk)
            if sum(l["kind"] == "new" for l in lessons) % 4 == 0:
                rid = f"GB1-R{1 + sum(l['kind'] == 'review' for l in lessons):03d}"
                lessons.append({"id": rid, "topic": topic, "kind": "review", "target_ids": [],
                                "review_target_ids": list(group), "preparation_state": "draft"})
                group.clear()
    if group:
        rid = f"GB1-R{1 + sum(l['kind'] == 'review' for l in lessons):03d}"
        lessons.append({"id": rid, "topic": "Mixed everyday revision", "kind": "review", "target_ids": [],
                        "review_target_ids": list(group), "preparation_state": "draft"})
    if require_assigned and known != used:
        raise ValueError("unassigned targets remain")
    return lessons


def teaching_issues(record):
    errors = []
    if record.get("review_state") != "reviewed":
        errors.append("linguistic review pending")
    meanings = record.get("bn_meanings", [])
    if not meanings or not any(re.search(r"[\u0980-\u09ff]", s) for s in meanings):
        errors.append("Bengali meaning missing")
    examples = record.get("original_examples", [])
    if not examples or any(not e.get("de") or not e.get("bn") for e in examples):
        errors.append("bilingual original example missing")
    if not record.get("exercise") or not record.get("answer"):
        errors.append("exercise or answer missing")
    grammar = record.get("grammar", {})
    if record.get("word_type") == "noun":
        if not grammar.get("article") or not grammar.get("plural"):
            errors.append("noun article/plural missing")
    if record.get("word_type") == "verb":
        if len(grammar.get("praesens", [])) != 6:
            errors.append("six Präsens forms missing")
        for key in ("partizip_ii", "auxiliary", "praeteritum", "case", "group"):
            if not grammar.get(key):
                errors.append("verb " + key + " missing")
    return errors


def lesson_filename(lesson):
    return lesson["id"] + ".md"


def render_lesson(lesson, teaching):
    ids = lesson["target_ids"] or lesson["review_target_ids"]
    if any(tid not in teaching or teaching_issues(teaching[tid]) for tid in ids):
        raise ValueError("Cannot render ready lesson with missing/unreviewed teaching data")
    review = lesson["kind"] == "review"
    title = ("Revision — " if review else "Vocabulary — ") + lesson["topic"]
    front = {"course": "Goethe-B1", "lesson_id": lesson["id"], "topic": lesson["topic"],
             "kind": lesson["kind"], "target_ids": lesson["target_ids"],
             "review_target_ids": lesson["review_target_ids"], "preparation_state": "ready",
             "source_refs": lesson.get("source_refs", []), "assessment_state": "not-assessed-in-this-lesson"}
    lines = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in front.items()] + ["---", "", "# " + lesson["id"] + " — " + title, "",
        "> এটি প্রস্তুত study material, completed practice নয়। আগে থেকে জানা শব্দ থাকলে ছোট recall check করে এগোবে।", "",
        "## আজকের লক্ষ্য", "", "অর্থ বুঝে শব্দ মনে করা, noun হলে article/plural এবং verb হলে প্রয়োজনীয় forms-সহ ব্যবহার করা।", "",
        "## কীভাবে পড়বে", "", "১. শব্দ ও বাক্য পড়ো। ২. অংশটি ঢেকে অর্থ মনে করো। ৩. practice করো। ৪. শেষে answer key মিলিয়ে দেখো।", ""]
    if not review:
        lines += ["## ছোট revision", "", "আগের lesson থেকে দুটি শব্দ article/form-সহ মনে করো; প্রথম lesson হলে আগে জানা দুটি শব্দ বলো।", "", "## শব্দ ও ব্যবহার", ""]
        for tid in ids:
            record, grammar = teaching[tid], teaching[tid].get("grammar", {})
            label = (grammar.get("article", "") + " " + record["lemma"]).strip()
            lines += ["### " + label, "", "**অর্থ:** " + "; ".join(record["bn_meanings"]), ""]
            if record["word_type"] == "noun":
                lines += ["**Plural:** " + grammar["plural"], ""]
            elif record["word_type"] == "verb":
                lines += ["**Group/pattern:** " + grammar["group"], "", "| Subject | Präsens |", "|---|---|"]
                lines += [f"| {subject} | {form} |" for subject, form in zip(["ich", "du", "er/sie/es", "wir", "ihr", "sie/Sie"], grammar["praesens"])]
                lines += ["", f"**Partizip II:** {grammar['partizip_ii']} · **Perfekt auxiliary:** {grammar['auxiliary']}", "",
                          f"**Präteritum reference:** {grammar['praeteritum']} — regular verbs-এর ক্ষেত্রে এখন Perfekt-এ বেশি practice; priority-list অনুযায়ী active Präteritum।", "",
                          "**Case/preposition:** " + grammar["case"], ""]
            if record.get("usage_notes"):
                lines += [record["usage_notes"], ""]
            for example in record["original_examples"]:
                lines += ["- **" + example["de"] + "** — " + example["bn"]]
            pages = ", ".join(str(p) for p in record.get("pdf_pages", []))
            lines += ["", f"Target: `{tid}` · মূল PDF page: {pages} · উদাহরণ নিজে তৈরি, PDF থেকে কপি নয়।", ""]
    lines += ["## নিজে practice করো", "", "উত্তর না দেখে চেষ্টা করো।", ""]
    for index, tid in enumerate(ids, 1):
        lines += [f"{index}. {teaching[tid]['exercise']}"]
    lines += ["", "## ছোট ব্যবহার", "", "এই lesson-এর যেকোনো দুটি শব্দ দিয়ে দুটি ছোট German বাক্য লেখো। Revision lesson হলে চারটি শব্দ নিয়ে চেষ্টা করো।", "",
              "## Answer key", "", "অর্থ ও grammar সঠিক হলে স্বাভাবিক বিকল্প বাক্যও গ্রহণযোগ্য।", ""]
    for index, tid in enumerate(ids, 1):
        lines += [f"{index}. {teaching[tid]['answer']}"]
    lines += ["", "### ছোট ব্যবহারের উদাহরণ — একমাত্র সঠিক উত্তর নয়", ""]
    for tid in ids[:2]:
        example = teaching[tid]["original_examples"][0]
        lines += ["- " + example["de"] + " — " + example["bn"]]
    lines += ["", "## Self-review", "", "- [ ] অর্থ না দেখে মনে করতে পারি।", "- [ ] Article/plural বা verb form মনে করতে পারি।",
              "- [ ] নিজের ছোট বাক্যে ব্যবহার করতে পারি।", "", "আবার দেখো: পরের session → প্রায় ৩ দিন → ১ সপ্তাহ → পরে আরেকবার। এগুলো প্রস্তাবিত revision interval, reminder নয়।", "",
              "## Agent note", "", "এই ফাইলের checkbox নিজের self-check; scored evidence নয়। Actual practice হলে dated lecture-এ exact answer, correction ও এই lesson ID রাখবে। Canonical tracker evidence অনুযায়ী update করবে।", "",
              "## Learner notes", "", "<!-- learner-notes:start -->", "", "<!-- learner-notes:end -->", ""]
    return "\n".join(lines)


def render_navigation(inventory, lessons, output_dir):
    output_dir = Path(output_dir)
    targets = {t["id"]: t for t in inventory["targets"]}
    lesson_map = {l["id"]: l for l in lessons}
    lines = ["# Goethe B1 — A–Z lookup", "", "> পূর্ণ source coverage এখনও যাচাই হয়নি। Candidate rows-কে verified vocabulary বা learned words ধরবে না।", "",
             "German phonebook-style sorting: ä→ae, ö→oe, ü→ue, ß→ss; বানান অপরিবর্তিত।", "", "| Word | Type | Topic | Primary lesson | Source check | Live tracker |", "|---|---|---|---|---|---|"]
    for target in sorted(targets.values(), key=lambda t: german_sort_key(t["lemma"])):
        lesson = lesson_map.get(target.get("primary_lesson_id"))
        label = "Not assigned — source/topic review pending"
        if lesson:
            label = f"[{lesson['id']}](<Lessons/{lesson_filename(lesson)}>)" if lesson["preparation_state"] == "ready" else lesson["id"] + " — not ready"
        safe_lemma = target["lemma"].replace("|", "/")
        canonical = inventory.get("canonical_records", {}).get(target["id"])
        tracker = f"[{Path(canonical['tracker']).stem}](<../../../{canonical['tracker']}>)" if canonical else "Not registered; no learning evidence inferred"
        lines.append(f"| {safe_lemma} | {target['word_type']} | {target.get('primary_topic') or 'Needs topic review'} | {label} | {target['normalization_state']} | {tracker} |")
    (output_dir / "A-Z.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    lines = ["# Goethe B1 — Lesson index", "", "> Ready = study material প্রস্তুত; completed practice বা mastery নয়।", "", "| Lesson | Topic | Kind | Targets | Preparation |", "|---|---|---|---:|---|"]
    for lesson in lessons:
        label = f"[{lesson['id']}](<Lessons/{lesson_filename(lesson)}>)" if lesson["preparation_state"] == "ready" else lesson["id"]
        count = len(lesson["target_ids"] or lesson["review_target_ids"])
        lines.append(f"| {label} | {lesson['topic']} | {lesson['kind']} | {count} | {lesson['preparation_state']} |")
    unassigned = sum(not t.get("primary_lesson_id") for t in targets.values())
    lines += ["", f"Unassigned candidate targets: **{unassigned}**. Source normalization/topic assignment বাকি; এই অংশকে completed syllabus বলা যাবে না।", ""]
    (output_dir / "Lesson-Index.md").write_text("\n".join(lines), encoding="utf-8")
