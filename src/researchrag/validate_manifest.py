from __future__ import annotations

import json
from pathlib import Path


def validate_manifest(raw_dir: Path) -> None:
    manifest_path = raw_dir / "00_manifest.jsonl"
    if not manifest_path.exists():
        raise SystemExit(f"Missing manifest: {manifest_path}")

    # Collect PDFs (exclude manifest itself)
    pdf_paths = sorted(p for p in raw_dir.glob("*.pdf") if p.is_file())
    pdf_filenames = {p.name for p in pdf_paths}

    # Read manifest lines
    entries = []
    with manifest_path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                raise SystemExit(f"Invalid JSON on line {i} of {manifest_path}: {e}") from e
            entries.append((i, obj))

    # Basic field checks + uniqueness
    doc_ids: set[str] = set()
    filenames_in_manifest: set[str] = set()

    required_fields = ["doc_id", "filename", "title", "authors", "year", "source"]

    for line_no, obj in entries:
        for k in required_fields:
            if k not in obj or obj[k] in (None, ""):
                raise SystemExit(f"Missing/empty '{k}' on line {line_no} in {manifest_path}")

        doc_id = str(obj["doc_id"])
        filename = str(obj["filename"])

        if doc_id in doc_ids:
            raise SystemExit(f"Duplicate doc_id '{doc_id}' (line {line_no})")
        doc_ids.add(doc_id)

        if filename in filenames_in_manifest:
            raise SystemExit(f"Duplicate filename '{filename}' (line {line_no})")
        filenames_in_manifest.add(filename)

    # Coverage checks
    missing_in_manifest = sorted(pdf_filenames - filenames_in_manifest)
    if missing_in_manifest:
        raise SystemExit("PDFs missing from manifest:\n  " + "\n  ".join(missing_in_manifest))

    missing_on_disk = sorted(filenames_in_manifest - pdf_filenames)
    if missing_on_disk:
        raise SystemExit("Manifest entries missing on disk:\n  " + "\n  ".join(missing_on_disk))


if __name__ == "__main__":
    validate_manifest(Path("data/raw_pdfs"))
    print("OK: manifest matches PDFs")
