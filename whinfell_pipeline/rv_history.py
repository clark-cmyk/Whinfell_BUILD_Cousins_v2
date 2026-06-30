"""ARCH-1 — consolidated RV history for quartile horizons."""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from whinfell_pipeline.data_dictionary import get_rv_series_registry
from whinfell_pipeline.node_cockpits import default_spread_history_path


def default_dated_series_path(repo_root: Path | None = None) -> Path:
    root = repo_root or Path(__file__).resolve().parents[1]
    return root / "data" / "rv" / "v1" / "dated_series_history.json"


def default_curve_history_path(repo_root: Path | None = None) -> Path:
    root = repo_root or Path(__file__).resolve().parents[1]
    return root / "data" / "barchart" / "v1" / "barchart_curve_history.json"


def _load_json_records(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return list(payload.get("records") or [])


def _points_from_record(rec: dict[str, Any]) -> list[tuple[str, float]]:
    series: list[tuple[str, float]] = []
    for pt in rec.get("points") or []:
        if not isinstance(pt, dict):
            continue
        d = str(pt.get("date") or "")
        close = pt.get("close")
        if d and close is not None:
            series.append((d, float(close)))
    latest = rec.get("latest")
    if isinstance(latest, dict) and latest.get("close") is not None:
        d = str(latest.get("date") or "")
        if d:
            series.append((d, float(latest["close"])))
    return sorted(series, key=lambda x: x[0])


def _index_barchart_records(records: list[dict[str, Any]]) -> dict[str, list[tuple[str, float]]]:
    out: dict[str, list[tuple[str, float]]] = {}
    for rec in records:
        if not isinstance(rec, dict):
            continue
        pts = _points_from_record(rec)
        if not pts:
            continue
        keys = {
            str(rec.get("raw_symbol") or ""),
            str(rec.get("canonical_id") or ""),
        }
        spread_meta = rec.get("spread_meta") or {}
        if isinstance(spread_meta, dict):
            for leg in spread_meta.get("spread_legs") or []:
                keys.add(str(leg))
        for key in keys:
            k = key.strip().upper()
            if not k:
                continue
            existing = out.get(k, [])
            merged = sorted(set(existing + pts), key=lambda x: x[0])
            out[k] = merged
    return out


def _load_dated_series_bundle(path: Path) -> dict[str, list[tuple[str, float]]]:
    if not path.is_file():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    out: dict[str, list[tuple[str, float]]] = {}
    for key, block in (payload.get("series") or {}).items():
        if not isinstance(block, dict):
            continue
        pts: list[tuple[str, float]] = []
        for pt in block.get("points") or []:
            if isinstance(pt, (list, tuple)) and len(pt) >= 2:
                pts.append((str(pt[0]), float(pt[1])))
            elif isinstance(pt, dict):
                d = str(pt.get("date") or "")
                v = pt.get("value")
                if d and v is not None:
                    pts.append((d, float(v)))
        if pts:
            out[str(key).upper()] = sorted(pts, key=lambda x: x[0])
    return out


def _lookup_history(
    history_key: str,
    spread_idx: dict[str, list[tuple[str, float]]],
    dated_idx: dict[str, list[tuple[str, float]]],
) -> list[tuple[str, float]]:
    key = history_key.upper()
    if key in dated_idx and len(dated_idx[key]) >= 2:
        return dated_idx[key]
    if key in spread_idx and len(spread_idx[key]) >= 2:
        return spread_idx[key]
    for idx in (spread_idx, dated_idx):
        for sym, vals in idx.items():
            if key in sym.upper() and len(vals) >= 2:
                return vals
    # Single-point barchart stub — use dated bundle fallback
    if key in dated_idx:
        return dated_idx[key]
    return []


def load_rv_history(repo_root: Path | None = None) -> dict[str, list[tuple[str, float]]]:
    """Load merged history keyed by rv_series history_key."""
    root = repo_root or Path(__file__).resolve().parents[1]
    spread_path = default_spread_history_path(root)
    curve_path = default_curve_history_path(root)
    dated_path = default_dated_series_path(root)

    spread_idx = _index_barchart_records(_load_json_records(spread_path))
    curve_idx = _index_barchart_records(_load_json_records(curve_path))
    for k, v in curve_idx.items():
        if k not in spread_idx or len(v) > len(spread_idx.get(k, [])):
            spread_idx[k] = v

    dated_idx = _load_dated_series_bundle(dated_path)

    reg = get_rv_series_registry()
    out: dict[str, list[tuple[str, float]]] = {}
    for row in reg.get("series", {}).values():
        if not isinstance(row, dict):
            continue
        hk = str(row.get("history_key") or "")
        if not hk:
            continue
        vals = _lookup_history(hk, spread_idx, dated_idx)
        if vals:
            out[hk.upper()] = vals
    return out


def ensure_dated_series_fixture(repo_root: Path | None = None, *, sessions: int = 800) -> Path:
    """Write deterministic dated series history for all rv_series keys (idempotent)."""
    root = repo_root or Path(__file__).resolve().parents[1]
    path = default_dated_series_path(root)
    reg = get_rv_series_registry()
    end = date(2026, 6, 29)
    series_out: dict[str, Any] = {}
    for sid, row in (reg.get("series") or {}).items():
        if not isinstance(row, dict):
            continue
        hk = str(row.get("history_key") or sid)
        unit = str(row.get("unit") or "pct")
        base = {
            "pct": 1.25,
            "bps": 320.0,
            "ratio": 0.98,
            "usd": 45000.0,
        }.get(unit, 1.0)
        seed = sum(ord(c) for c in hk)
        points: list[list[Any]] = []
        for i in range(sessions):
            d = (end - timedelta(days=sessions - 1 - i)).isoformat()
            # Deterministic oscillation — not random
            v = base * (1.0 + 0.08 * ((i + seed) % 17 - 8) / 8.0)
            points.append([d, round(v, 4)])
        series_out[hk.upper()] = {"series_id": sid, "unit": unit, "points": points}

    payload = {
        "version": "1.0",
        "as_of": end.isoformat(),
        "sessions": sessions,
        "series": series_out,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path