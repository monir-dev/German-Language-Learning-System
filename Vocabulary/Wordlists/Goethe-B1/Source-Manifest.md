# Source manifest — Goethe B1 Wortliste

- Source: [official Goethe-Zertifikat B1 Wortliste](https://www.goethe.de/pro/relaunch/prf/en/Goethe-Zertifikat_B1_Wortliste.pdf)
- Downloaded: 2026-11-12.
- Local file: `External Resources/Goethe-Zertifikat_B1_Wortliste.pdf` (vault-relative).
- Verified PDF pages: 104.
- File size: 475,500 bytes.
- SHA-256: `8860f7f0c916831b2365f66239a3ceba3be81ddba28e1224846ca8420807fe42`.
- Source identity: document copyright notice identifies Goethe-Institut and ÖSD, 2016; PDF metadata modification date is 2017. Do not label this a newly issued 2026 edition.
- Pages 1–7: title/imprint/contents/introduction; pages 8–15: word groups; pages 16–102: alphabetic vocabulary; pages 103–104: notes/back matter.

## Extraction and uncertainty

pdfplumber reads layout coordinates. Alphabetic source-headword columns are extracted separately from the adjacent example columns. Whole word-group pages are retained in the private cache because their varying layouts need explicit target mapping.

2,877 occurrences were captured, but a block can contain several entries, alternate forms or unresolved continuations. Normalization is provisional except for explicitly reviewed teaching targets. Every page/occurrence retains audit state; selected targets checked on a page do not make that whole page reconciled.

Source candidates are lexical/factual reference data, not copied lessons. Original teaching examples and Bengali explanations are in `Data/Authoring.json`; publisher example paragraphs are not included in the public-facing lessons.

## Publication boundary

The source PDF carries a copyright notice and is not treated as an open-licensed resource. Its exact file path and the full extraction cache directory are in `.gitignore`. Do not assume ignore rules remove a previously committed file from Git history.

Full extraction cache: `External Resources/Goethe-B1-private-cache/` (vault-relative, private, not linked as public content).

Before making this system public, review redistribution of all third-party resources and source-derived collections separately. This manifest makes no legal or open-license claim. Linking the official source is not permission to republish the PDF or example collection.
