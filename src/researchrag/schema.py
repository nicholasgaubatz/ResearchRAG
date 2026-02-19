import hashlib
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    doc_id: str  # Goal: hash that won't change on file renames.
    source_path: Path
    title: str


@dataclass(frozen=True)
class Chunk:
    doc_id: str
    chunk_id: str
    page_start: str
    page_end: str
    text: str
    section_heading: str | None = None


def compute_doc_id(path: Path) -> str:
    """Hash based on file contents."""
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()[:16]
