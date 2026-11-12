"""Extract private source layout and candidate headword blocks, not examples."""
import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re

EXPECTED_SHA = "8860f7f0c916831b2365f66239a3ceba3be81ddba28e1224846ca8420807fe42"


def verify_source(path, expected_sha=EXPECTED_SHA):
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if actual != expected_sha:
        raise ValueError("SHA-256 mismatch: source changed; review before extracting")
    return actual


def source_section(page):
    if 8 <= page <= 15:
        return "word-groups"
    if 16 <= page <= 102:
        return "alphabetic"
    return "non-vocabulary"


def headword_blocks(lines, page):
    """Group adjacent headword lines; caller supplies source-column lines only."""
    output = []
    for column, (left, right) in enumerate(((33, 131), (313, 411)), start=1):
        selected = [line for line in lines if left <= line["x0"] < right
                    and 60 <= line["top"] < 790
                    and not re.fullmatch(r"[A-ZÄÖÜ]|WORTLISTE|ZERTIFIKAT B1|\d+", line["text"].strip())]
        selected.sort(key=lambda row: row["top"])
        groups = []
        for row in selected:
            if not groups or row["top"] - groups[-1][-1]["top"] > 15:
                groups.append([])
            groups[-1].append(row)
        for group in groups:
            raw = " ".join(row["text"].strip() for row in group)
            block_key = f"p{page:03d}-c{column}-y{round(group[0]['top']):03d}"
            output.append({"id": "goethe-" + block_key, "pdf_page": page,
                           "printed_page": page, "section": "alphabetic", "layout_block": block_key,
                           "raw": raw, "raw_lines": [r["text"] for r in group],
                           "disposition": "needs_review", "target_ids": [],
                           "review_note": "Candidate from source column; source reconciliation pending."})
    return output


def _column_lines(page, left, right):
    crop = page.crop((left, 60, right, 790))
    words = crop.extract_words(extra_attrs=["size"])
    rows = defaultdict(list)
    for word in words:
        if 7.0 <= word["size"] <= 9.4:
            rows[round(word["top"] / 2) * 2].append(word)
    result = []
    for top, row in sorted(rows.items()):
        row.sort(key=lambda word: word["x0"])
        result.append({"x0": row[0]["x0"], "top": top,
                       "text": " ".join(w["text"] for w in row)})
    return result


def extract_source(pdf_path, cache_dir):
    import pdfplumber
    sha = verify_source(pdf_path)
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    candidates, pages = [], []
    with pdfplumber.open(pdf_path) as pdf:
        if len(pdf.pages) != 104:
            raise ValueError("Expected 104 pages; source needs review")
        for number, page in enumerate(pdf.pages, 1):
            section = source_section(number)
            meta = {"pdf_page": number, "section": section, "audit_state": "not-reviewed"}
            if section == "alphabetic":
                lines = _column_lines(page, 34, 131) + _column_lines(page, 314, 411)
                blocks = headword_blocks(lines, number)
                candidates.extend(blocks)
                meta["candidate_blocks"] = len(blocks)
            elif section == "word-groups":
                # Varied layouts: retain the page intact instead of inventing word boundaries.
                candidates.append({"id": f"goethe-p{number:03d}-word-groups", "pdf_page": number,
                    "printed_page": number, "section": section, "layout_block": "whole-page",
                    "raw": "", "disposition": "needs_review", "target_ids": [],
                    "review_note": "Variable-layout word groups require explicit reviewed target mapping."})
            else:
                meta["audit_state"] = "non-vocabulary"
            pages.append(meta)
            (cache_dir / f"page-{number:03d}.txt").write_text(page.extract_text() or "", encoding="utf-8")
    result = {"source": {"sha256": sha, "page_count": 104,
               "url": "https://www.goethe.de/pro/relaunch/prf/en/Goethe-Zertifikat_B1_Wortliste.pdf"},
              "pages": pages, "occurrences": candidates}
    (cache_dir / "extraction.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("pdf", type=Path)
    cli.add_argument("cache", type=Path)
    args = cli.parse_args()
    result = extract_source(args.pdf, args.cache)
    print(json.dumps({"pages": len(result["pages"]), "candidate_blocks": len(result["occurrences"]),
                      "coverage_complete": False}))
