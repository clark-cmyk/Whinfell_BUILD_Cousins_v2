"""Tests for funds flow sponsorship builder and credit fallback — PR-2/PR-3b."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRATCH = Path(
    "/var/folders/qn/gdsdhg9j3f77wk7fn889zbq40000gn/T/grok-goal-121c0aab5bcc/implementer"
)
SCRATCH.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(REPO_ROOT))

from whinfell_pipeline.flows_fallback import merge_fallback_into_sidecar, parse_credit_cross_section_flows
from whinfell_pipeline.funds_flows import (
    apply_confidence_delta,
    build_funds_flows,
    build_flows_sidecar_metadata,
    load_flows_sidecar,
    merge_flow_rationale,
)
from whinfell_pipeline.node_cockpits import build_node_cockpit, build_node_cockpits


def _healthy_credit_sidecar() -> dict:
    tickers = {}
    specs = [
        ("HYG", 0.08, 0.31, 0.35),
        ("LQD", 0.02, 0.09, 0.30),
        ("BKLN", 0.01, 0.04, 0.20),
        ("CWB", -0.01, -0.02, 0.15),
    ]
    for ticker, d1, d5, _w in specs:
        tickers[ticker] = {
            "ticker": ticker,
            "asset_id": ticker.lower() if ticker != "LQD" else "jaaa",
            "latest": {"date": "2026-06-29", "flow_pct_aum_1d": d1, "flow_usd_1d": d1 * 100},
            "rolling": {
                "flow_pct_aum_5d": d5,
                "flow_usd_5d": d5 * 100,
                "sessions_in_5d": 5,
                "persistence_score_20d": 0.65,
            },
        }
    return {
        "version": "1.0.0",
        "as_of": "2026-06-29",
        "source_file": "flows_20260629_1525.csv",
        "ingest_mode": "timeseries_primary",
        "tickers": tickers,
    }


def _minimal_cockpit(node_id: str = "credit") -> dict:
    return build_node_cockpit(
        node_id,
        global_payload={"whinfell_score": 65, "transmission_state": "normal", "key_observation": "Credit firm."},
        horizon_marks={"d1": "up", "d5": "up", "d20": "up", "d60": "flat"},
        as_of=datetime(2026, 6, 29, 15, 0, 0, tzinfo=timezone.utc),
        freshness_status="fresh",
        flows_sidecar=None,
    )


class TestFlowsFallback(unittest.TestCase):
    def test_parse_credit_cross_section(self):
        rows = [
            {"Ticker": "HYG", "AUM": "14500", "Fund Flows/Periodic (D)": "120.5"},
            {"Ticker": "LQD", "AUM": "42000", "Fund Flows/Periodic (D)": "45.0"},
            {"Ticker": "SPY", "AUM": "500000", "Fund Flows/Periodic (D)": "200"},
        ]
        parsed = parse_credit_cross_section_flows("", rows=rows)
        tickers = {r["ticker"] for r in parsed}
        self.assertEqual(tickers, {"HYG", "LQD"})
        hyg = next(r for r in parsed if r["ticker"] == "HYG")
        self.assertAlmostEqual(hyg["flow_pct_aum_1d"], (120.5 / 14500) * 100, places=3)

    def test_merge_fallback_into_sidecar_no_5d(self):
        rows = parse_credit_cross_section_flows(
            "",
            rows=[
                {"Ticker": "HYG", "AUM": "14500", "Fund Flows/Periodic (D)": "120.5"},
                {"Ticker": "LQD", "AUM": "42000", "Fund Flows/Periodic (D)": "45.0"},
            ],
        )
        sidecar = merge_fallback_into_sidecar(None, rows, as_of="2026-06-29")
        self.assertEqual(sidecar["ingest_mode"], "fallback_1d_only")
        self.assertTrue(sidecar["fallback_overlay"]["active"])
        hyg = sidecar["tickers"]["HYG"]
        self.assertIn("flow_pct_aum_1d", hyg["latest"])
        self.assertEqual(hyg.get("rolling"), {})
        self.assertNotIn("flow_pct_aum_5d", hyg.get("rolling", {}))


class TestFundsFlowsBuilder(unittest.TestCase):
    def test_build_credit_healthy(self):
        cockpit = _minimal_cockpit("credit")
        cockpit.pop("funds_flows", None)
        result = build_funds_flows(
            "credit",
            sidecar=_healthy_credit_sidecar(),
            node_cockpit=cockpit,
            as_of="2026-06-29",
        )
        self.assertTrue(result["enabled"])
        self.assertEqual(result["flows_meta"]["flows_status"], "ok")
        self.assertEqual(result["degrade_mode"], "full")
        self.assertIn(result["aggregate"]["verdict"], ("supportive", "neutral", "mixed", "diverging"))
        self.assertIsNotNone(result["aggregate"]["flow_pct_aum_5d"])
        self.assertEqual(len(result["etfs"]), 4)
        primary = next(e for e in result["etfs"] if e["basket_role"] == "primary")
        self.assertEqual(primary["ticker"], "HYG")
        (SCRATCH / "funds_flows_sample.json").write_text(
            json.dumps(result, indent=2),
            encoding="utf-8",
        )

    def test_build_credit_fallback_1d(self):
        rows = parse_credit_cross_section_flows(
            "",
            rows=[
                {"Ticker": "HYG", "AUM": "14500", "Fund Flows/Periodic (D)": "120.5"},
                {"Ticker": "LQD", "AUM": "42000", "Fund Flows/Periodic (D)": "45.0"},
            ],
        )
        sidecar = merge_fallback_into_sidecar(None, rows, as_of="2026-06-29")
        cockpit = _minimal_cockpit("credit")
        cockpit.pop("funds_flows", None)
        result = build_funds_flows("credit", sidecar=sidecar, node_cockpit=cockpit)
        self.assertTrue(result["enabled"])
        self.assertEqual(result["flows_meta"]["flows_status"], "fallback_1d")
        self.assertEqual(result["degrade_mode"], "fallback_1d_credit")
        self.assertIsNone(result["aggregate"]["flow_pct_aum_5d"])
        self.assertEqual(result["aggregate"]["confidence_delta"], 0)
        self.assertEqual(
            result["interpretation"]["degrade_notice"],
            "5D flows unavailable — using 1D Credit cross-section fallback.",
        )

    def test_build_breadth_unavailable_without_sidecar(self):
        cockpit = _minimal_cockpit("breadth")
        cockpit.pop("funds_flows", None)
        result = build_funds_flows("breadth", sidecar=None, node_cockpit=cockpit)
        self.assertFalse(result["enabled"])
        self.assertEqual(result["flows_meta"]["flows_status"], "unavailable")
        self.assertEqual(result["flows_meta"]["fallback_reason"], "missing_wtm_flows_file")
        self.assertIsNone(result["aggregate"]["verdict"])

    def test_apply_confidence_delta_and_rationale(self):
        funds = build_funds_flows(
            "credit",
            sidecar=_healthy_credit_sidecar(),
            node_cockpit=_minimal_cockpit("credit"),
        )
        boosted = apply_confidence_delta("low", funds)
        if funds["aggregate"]["confidence_delta"] > 0 and funds["flows_meta"]["flows_confidence_penalty"] == 0:
            self.assertEqual(boosted, "medium")
        merged = merge_flow_rationale("Base rationale.", funds)
        if funds["aggregate"]["verdict"] in ("supportive", "diverging"):
            self.assertIn("Flows:", merged)


class TestNodeCockpitFundsWire(unittest.TestCase):
    def _tracer(self) -> dict[str, dict[str, str]]:
        return {nid: {"d1": "up", "d5": "up", "d20": "flat", "d60": "flat"} for nid in (
            "liquidity", "credit", "breadth", "highbeta", "basis"
        )}

    def test_all_nodes_have_funds_flows(self):
        cockpits = build_node_cockpits(
            global_payload={"whinfell_score": 65, "transmission_state": "normal"},
            suggested_tracer=self._tracer(),
            as_of=datetime(2026, 6, 29, tzinfo=timezone.utc),
            freshness_status="fresh",
            flows_sidecar=_healthy_credit_sidecar(),
        )
        for node_id, cockpit in cockpits.items():
            self.assertIn("funds_flows", cockpit)
            ff = cockpit["funds_flows"]
            self.assertIn("flows_meta", ff)
            self.assertIn(ff["flows_meta"]["flows_status"], ("ok", "partial", "fallback_1d", "unavailable"))
        credit = cockpits["credit"]
        self.assertTrue(credit["funds_flows"]["enabled"])
        (SCRATCH / "node_cockpits_funds.json").write_text(
            json.dumps({k: v.get("funds_flows") for k, v in cockpits.items()}, indent=2),
            encoding="utf-8",
        )

    def test_no_sidecar_unavailable_degrade(self):
        cockpits = build_node_cockpits(
            global_payload={"whinfell_score": 65},
            suggested_tracer=self._tracer(),
            as_of=datetime(2026, 6, 29, tzinfo=timezone.utc),
            freshness_status="fresh",
            flows_sidecar=None,
        )
        self.assertEqual(cockpits["breadth"]["funds_flows"]["flows_meta"]["flows_status"], "unavailable")
        self.assertFalse(cockpits["breadth"]["funds_flows"]["enabled"])

    def test_fallback_credit_only(self):
        rows = parse_credit_cross_section_flows(
            "",
            rows=[{"Ticker": "HYG", "AUM": "14500", "Fund Flows/Periodic (D)": "120.5"}],
        )
        sidecar = merge_fallback_into_sidecar(None, rows, as_of="2026-06-29")
        cockpits = build_node_cockpits(
            global_payload={"whinfell_score": 65},
            suggested_tracer=self._tracer(),
            as_of=datetime(2026, 6, 29, tzinfo=timezone.utc),
            freshness_status="fresh",
            flows_sidecar=sidecar,
        )
        self.assertEqual(cockpits["credit"]["funds_flows"]["flows_meta"]["flows_status"], "fallback_1d")
        self.assertEqual(cockpits["breadth"]["funds_flows"]["flows_meta"]["flows_status"], "unavailable")

    def test_load_flows_sidecar_from_disk(self):
        sidecar = _healthy_credit_sidecar()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "data" / "flows" / "v1" / "latest_flows.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(sidecar), encoding="utf-8")
            loaded = load_flows_sidecar(root)
            self.assertIsNotNone(loaded)
            meta = build_flows_sidecar_metadata(loaded)
            self.assertEqual(meta["ingest_mode"], "timeseries_primary")
            self.assertEqual(meta["ticker_count"], 4)


if __name__ == "__main__":
    unittest.main()