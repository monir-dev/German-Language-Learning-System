"""Normalize source candidates while preserving uncertainties and old evidence."""
import copy
import hashlib
import re
import unicodedata


def target_id(lemma, word_type, region=None, sense=""):
    key = unicodedata.normalize("NFC", "|".join([lemma, word_type, region or "", sense]))
    return "gb1-" + hashlib.sha256(key.encode()).hexdigest()[:12]


def guess_target(raw):
    raw = raw.strip()
    if not raw or (raw.endswith("-") and "," not in raw) or "→" == raw[:1] or re.match(r"^(hat|ist|war|wurde|wird)\b", raw):
        return None
    noun = re.match(r"^(der|die|das)\s+([^,;(]+)", raw)
    if noun:
        lemma = noun.group(2).strip()
        if len(lemma.split()) > 4:
            return None
        word_type = "noun"
    else:
        lemma = raw.split(",", 1)[0].strip()
        lemma = re.sub(r"\s*\([^)]*\).*$", "", lemma).strip()
        if len(lemma.split()) > 5 or not re.search(r"[A-Za-zÄÖÜäöüß]", lemma):
            return None
        word_type = "verb" if "," in raw and re.search(r"(?:en|eln|ern|tun|sein)$", lemma) else "other"
    region_match = re.search(r"\(([DAC H,]+)\)", raw.split("→", 1)[0])
    return {"lemma": lemma, "word_type": word_type,
            "region": region_match.group(1).strip() if region_match else None}


def normalize_occurrences(occurrences, overrides):
    rows, targets = [], {}
    for source in occurrences:
        row = copy.deepcopy(source)
        row["target_ids"] = []
        explicit = source["id"] in overrides
        specs = overrides.get(source["id"])
        complete = True
        if isinstance(specs, dict):
            complete = specs.get("complete", False)
            specs = specs["targets"]
        if specs is None:
            candidate = guess_target(source.get("raw", ""))
            specs = [candidate] if candidate else []
        for spec in specs:
            tid = target_id(spec["lemma"], spec["word_type"], spec.get("region"), spec.get("sense", ""))
            if tid not in targets:
                targets[tid] = {**spec, "id": tid, "source_occurrence_ids": [],
                    "primary_topic": None, "related_topics": [], "primary_lesson_id": None,
                    "canonical_record_key": None, "normalization_state": "reviewed" if explicit and spec.get("reviewed", True) else "candidate"}
            elif explicit and spec.get("reviewed", True):
                targets[tid]["normalization_state"] = "reviewed"
            if source["id"] not in targets[tid]["source_occurrence_ids"]:
                targets[tid]["source_occurrence_ids"].append(source["id"])
            row["target_ids"].append(tid)
        row["disposition"] = "mapped" if explicit and complete else "needs_review"
        row["review_note"] = ("Explicit normalization reviewed." if complete else "Selected targets reviewed; rest of source block remains open.") if explicit else source.get("review_note", "Normalization pending review.")
        rows.append(row)
    return {"occurrences": rows, "targets": list(targets.values()),
            "source_audit": {"complete": False, "pending_pages": sorted({r["pdf_page"] for r in rows if r["disposition"] == "needs_review"})}}


def map_existing_records(targets, tracker_paths):
    records = {}
    for path in tracker_paths:
        path = __import__("pathlib").Path(path)
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 4:
                continue
            lemma = re.sub(r"^(der|die|das)\s+", "", cells[0]).strip()
            records.setdefault(lemma, []).append({"tracker": str(path), "key": cells[0],
                "status": cells[-2], "evidence": cells[-1]})
    output = {}
    for target in targets:
        matches = records.get(target["lemma"], [])
        if len(matches) == 1:
            output[target["id"]] = matches[0]
    return output
