"""WTM data dictionary loader tests."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from whinfell_pipeline.data_dictionary import (
    barchart_all_approved_symbols,
    barchart_core_symbols,
    barchart_curve_symbols,
    barchart_instrument_class_map,
    barchart_spread_symbols,
    canonical_asset_for_ticker,
    canonical_saved_view_names,
    get_canonical_filename_patterns,
    get_column_mappings,
    get_json_field_map,
    get_node_score_weights,
    get_project_structure,
    get_rv_series_registry,
    get_ticker_standards,
    get_watchlist_names,
    node_score_components,
    normalize_glob_rules,
    legacy_alias,
    load_data_dictionary,
    master_dictionary_info,
    rv_series_catalog,
    rv_series_for_node,
    rv_series_primary,
    snapshot_field_map,
    source_system_ids,
)


class TestDataDictionary(unittest.TestCase):
    def test_loads_version(self):
        dd = load_data_dictionary()
        self.assertEqual(dd["version"], "1.0")
        info = master_dictionary_info(dd)
        self.assertEqual(info["version"], "1.0")
        self.assertEqual(info["status"], "Locked")
        self.assertEqual(info["date"], "2026-06-29")

    def test_master_sections_present(self):
        dd = load_data_dictionary()
        for key in (
            "project_structure",
            "watchlist_names",
            "file_naming_conventions",
            "json_structures",
            "column_mappings",
            "ticker_standards",
            "rv_series",
            "node_score_weights",
        ):
            self.assertIn(key, dd, key)
        self.assertEqual(get_project_structure()["repo_root"], "~/Desktop/Whinfell_BUILD_Cousins")
        views = canonical_saved_view_names()
        self.assertIn("WTM-Credit-Confirmation", views)
        self.assertIn("WTM-Rates-Credit", views)
        patterns = get_canonical_filename_patterns()
        self.assertIn("credit_vendor_snapshot", patterns["vendor_to_canonical"])
        rules = normalize_glob_rules()
        self.assertTrue(any(r.get("dataset") == "credit" for r in rules))
        jfm = get_json_field_map()
        self.assertIn("whinfell_score", jfm["hydration_bundle"]["blocks"]["global"])
        cm = get_column_mappings()
        self.assertEqual(cm["display_to_field"]["Whinfell Score"], "whinfell_score")
        ts = get_ticker_standards()
        self.assertEqual(ts["koyfin"]["format"], "uppercase_plain")
        wl = get_watchlist_names()
        self.assertEqual(wl["koyfin_saved_views"]["WTM-Credit-Confirmation"]["dataset"], "credit")

    def test_source_systems_present(self):
        ids = source_system_ids()
        self.assertIn("koyfin_snapshot_csv", ids)
        self.assertIn("barchart_core_history", ids)

    def test_ticker_resolution(self):
        self.assertEqual(canonical_asset_for_ticker("koyfin", "BTCUSD"), "btc_spot_usd")
        self.assertEqual(canonical_asset_for_ticker("barchart", "^BTCUSD"), "btc_spot_usd")

    def test_barchart_core_count(self):
        symbols = barchart_core_symbols()
        self.assertIn("^BTCUSD", symbols)
        self.assertEqual(len(symbols), 16)

    def test_barchart_all_approved_count(self):
        self.assertEqual(len(barchart_all_approved_symbols()), 78)
        self.assertEqual(len(barchart_spread_symbols()), 5)
        self.assertEqual(len(barchart_curve_symbols()), 57)

    def test_barchart_core_symbols_match_objective(self):
        expected = {
            "^BTCUSD", "^ETHUSD", "^XRPUSD", "^SOLUSD", "IBIT", "GBTC", "SOFR",
            "$HSI", "$VHSI", "$VXHY", "CBON", "KHYB", "ASHR", "DXY00", "GCY00", "HGY00",
        }
        self.assertEqual(set(barchart_core_symbols()), expected)

    def test_barchart_instrument_class_map(self):
        ic = barchart_instrument_class_map()
        self.assertEqual(ic["^BTCUSD"], "crypto_spot")
        self.assertEqual(ic["IBIT"], "etf")
        self.assertEqual(ic["GCY00"], "continuous")

    def test_legacy_alias(self):
        self.assertEqual(legacy_alias("BTCPRice"), "btc_spot_usd")

    def test_snapshot_field_map(self):
        fm = snapshot_field_map()
        self.assertEqual(fm["Last Price"], "last_price")
        self.assertEqual(fm["Volatility 1M"], "vol_1m")

    def test_rv_series_registry_locked(self):
        reg = get_rv_series_registry()
        self.assertEqual(reg["version"], "1.0")
        self.assertEqual(reg["status"], "Locked")
        catalog = rv_series_catalog()
        self.assertIn("btc_calendar_bt_near_deferred", catalog)
        self.assertEqual(catalog["hy_oas_proxy"]["quartile_direction"], "higher_is_cheaper")
        self.assertEqual(catalog["btc_calendar_bt_near_deferred"]["quartile_direction"], "higher_is_richer")
        self.assertEqual(rv_series_primary("basis"), "btc_calendar_bt_near_deferred")
        basis_rows = rv_series_for_node("basis")
        self.assertGreaterEqual(len(basis_rows), 1)
        horizons = reg["lookback_trading_days"]
        self.assertEqual(horizons["3m"], 63)

    def test_node_score_weights_interim(self):
        nsw = get_node_score_weights()
        self.assertEqual(nsw["status"], "Locked")
        liq = node_score_components("liquidity")
        self.assertEqual(len(liq), 5)
        self.assertEqual(sum(c["weight_pct"] for c in liq), 100)
        for node_id in ("breadth", "highbeta", "basis"):
            comps = node_score_components(node_id)
            self.assertEqual(len(comps), 5)
            self.assertEqual(sum(c["weight_pct"] for c in comps), 100)
        self.assertEqual(nsw["design"]["fallback_min_components"], 2)


if __name__ == "__main__":
    unittest.main()