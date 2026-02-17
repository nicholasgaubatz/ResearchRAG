from pathlib import Path

import pytest

pytestmark = pytest.mark.integration


def test_manifest_matches_pdfs():
    raw_dir = Path("data/raw_pdfs")
    manifest = raw_dir / "00_manifest.jsonl"
    if not manifest.exists():
        pytest.skip("Local data/manifest not present; skipping.")

    from validate_manifest import validate_manifest

    validate_manifest(raw_dir)
