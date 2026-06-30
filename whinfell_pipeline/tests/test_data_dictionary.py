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
    get_project_structure,
    get_ticker_standards,
    get_watchlist_names,
    normalize_glob_rules,
    legacy_alias,
    load_data_dictionary,
    master_dictionary_info,
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


if __name__ == "__main__":
    unittest.main()