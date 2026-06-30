"""Load and query WTM data dictionary — canonical assets, routing, field maps."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

DICTIONARY_VERSION = "1.0"


def default_dictionary_path(repo_root: Path | None = None) -> Path:
    root = repo_root or Path(__file__).resolve().parent
    return root / "data_dictionary.yaml"


@lru_cache(maxsize=1)
def load_data_dictionary(path: str | None = None) -> dict[str, Any]:
    p = Path(path) if path else default_dictionary_path()
    with p.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return dict(data)


def canonical_asset_for_ticker(vendor: str, ticker: str, data: dict[str, Any] | None = None) -> str | None:
    """Resolve raw vendor ticker to canonical asset id."""
    dd = data or load_data_dictionary()
    t = ticker.strip().upper()
    for asset_id, spec in (dd.get("canonical_assets") or {}).items():
        sources = spec.get("sources") or {}
        raw = sources.get(vendor)
        if raw and str(raw).upper() == t:
            return asset_id
        if raw and str(raw).upper().lstrip("^$") == t.lstrip("^$"):
            return asset_id
    return None


def barchart_core_symbols(data: dict[str, Any] | None = None) -> list[str]:
    dd = data or load_data_dictionary()
    return list((dd.get("universes") or {}).get("barchart_core", {}).get("symbols") or [])


def barchart_curve_symbols(data: dict[str, Any] | None = None) -> list[str]:
    dd = data or load_data_dictionary()
    groups = (dd.get("universes") or {}).get("barchart_curves", {}).get("symbol_groups") or {}
    out: list[str] = []
    for key, syms in groups.items():
        if key == "structured_spreads":
            continue
        out.extend(syms)
    return out


def barchart_spread_symbols(data: dict[str, Any] | None = None) -> list[str]:
    dd = data or load_data_dictionary()
    groups = (dd.get("universes") or {}).get("barchart_curves", {}).get("symbol_groups") or {}
    return list(groups.get("structured_spreads") or [])


def barchart_all_approved_symbols(data: dict[str, Any] | None = None) -> list[str]:
    return barchart_core_symbols(data) + barchart_curve_symbols(data) + barchart_spread_symbols(data)


def barchart_canonical_core_map(data: dict[str, Any] | None = None) -> dict[str, str]:
    dd = data or load_data_dictionary()
    return dict(dd.get("barchart_canonical_core") or {})


def barchart_history_field_map(data: dict[str, Any] | None = None) -> dict[str, str]:
    dd = data or load_data_dictionary()
    return dict(dd.get("barchart_history_fields") or {})


def barchart_instrument_class_map(data: dict[str, Any] | None = None) -> dict[str, str]:
    dd = data or load_data_dictionary()
    return dict(dd.get("barchart_instrument_class") or {})


def source_system_ids(data: dict[str, Any] | None = None) -> list[str]:
    dd = data or load_data_dictionary()
    return list((dd.get("source_systems") or {}).keys())


def legacy_alias(name: str, data: dict[str, Any] | None = None) -> str | None:
    dd = data or load_data_dictionary()
    entry = (dd.get("legacy_aliases") or {}).get(name)
    if isinstance(entry, dict):
        return entry.get("canonical")
    return None


def snapshot_field_map(data: dict[str, Any] | None = None) -> dict[str, str]:
    dd = data or load_data_dictionary()
    return dict((dd.get("field_mappings") or {}).get("snapshot") or {})


def master_dictionary_info(data: dict[str, Any] | None = None) -> dict[str, str]:
    """Return locked Master Data Dictionary version, date, and status."""
    dd = data or load_data_dictionary()
    mdd = dd.get("master_data_dictionary") or {}
    return {
        "version": str(mdd.get("version") or dd.get("version") or DICTIONARY_VERSION),
        "date": str(mdd.get("date") or dd.get("updated") or ""),
        "status": str(mdd.get("status") or dd.get("status") or "Locked"),
        "alignment": str(mdd.get("alignment") or "Aligned"),
    }


def dictionary_status(data: dict[str, Any] | None = None) -> str:
    return master_dictionary_info(data)["status"]


def get_project_structure(data: dict[str, Any] | None = None) -> dict[str, Any]:
    dd = data or load_data_dictionary()
    return dict(dd.get("project_structure") or {})


def get_watchlist_names(data: dict[str, Any] | None = None) -> dict[str, Any]:
    dd = data or load_data_dictionary()
    return dict(dd.get("watchlist_names") or {})


def get_canonical_filename_patterns(data: dict[str, Any] | None = None) -> dict[str, Any]:
    dd = data or load_data_dictionary()
    return dict(dd.get("file_naming_conventions") or {})


def get_json_field_map(data: dict[str, Any] | None = None) -> dict[str, Any]:
    dd = data or load_data_dictionary()
    return dict(dd.get("json_structures") or {})


def get_column_mappings(data: dict[str, Any] | None = None) -> dict[str, Any]:
    dd = data or load_data_dictionary()
    return dict(dd.get("column_mappings") or {})


def get_ticker_standards(data: dict[str, Any] | None = None) -> dict[str, Any]:
    dd = data or load_data_dictionary()
    return dict(dd.get("ticker_standards") or {})


def canonical_saved_view_names(data: dict[str, Any] | None = None) -> list[str]:
    views = (get_watchlist_names(data).get("koyfin_saved_views") or {})
    return list(views.keys())