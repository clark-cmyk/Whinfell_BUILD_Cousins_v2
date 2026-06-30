"""Sync Master Data Dictionary metadata to desk-facing JS for Transmission Control."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from whinfell_pipeline.data_dictionary import (
    DICTIONARY_VERSION,
    canonical_saved_view_names,
    get_project_structure,
    master_dictionary_info,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
META_JS = REPO_ROOT / "08_Deliverables" / "data_dictionary_meta.js"
META_JSON = REPO_ROOT / "08_Deliverables" / "data_dictionary_meta.json"


def build_meta_payload() -> dict:
    info = master_dictionary_info()
    ps = get_project_structure()
    return {
        "version": info["version"],
        "date": info["date"],
        "status": info["status"],
        "alignment": info["alignment"],
        "machine_version": DICTIONARY_VERSION,
        "repo_root": ps.get("repo_root", ""),
        "saved_views": canonical_saved_view_names(),
        "validated": True,
        "source": "whinfell_pipeline/data_dictionary.yaml",
    }


def write_meta_files(payload: dict | None = None) -> Path:
    payload = payload or build_meta_payload()
    META_JSON.parent.mkdir(parents=True, exist_ok=True)
    META_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    js = f"window.DICTIONARY_META = {json.dumps(payload, indent=2)};\n"
    META_JS.write_text(js, encoding="utf-8")
    return META_JS


def main() -> int:
    path = write_meta_files()
    print(f"synced {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())