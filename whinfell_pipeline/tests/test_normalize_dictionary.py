"""Normalize path driven by Master Data Dictionary normalize_rules."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from whinfell_pipeline.batch_collect import infer_canonical_name, normalize_drop_dir
from whinfell_pipeline.data_dictionary import raw_patterns_for_dataset
from whinfell_pipeline.sync_dictionary_meta import build_meta_payload


class TestNormalizeDictionary(unittest.TestCase):
    def test_credit_vendor_glob_from_dictionary(self):
        patterns = raw_patterns_for_dataset("credit")
        self.assertTrue(any("whinpump" in p.lower() for p in patterns))

    def test_infer_credit_from_vendor_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "koyfin_WhinPump_20260629.csv"
            path.write_text("Ticker,Last Price\n", encoding="utf-8")
            dest = infer_canonical_name(path.name, path)
            self.assertIsNotNone(dest)
            self.assertTrue(dest.startswith("credit_"))
            self.assertTrue(dest.endswith(".csv"))

    def test_normalize_dry_run_twice_consistent(self):
        with tempfile.TemporaryDirectory() as tmp:
            drop = Path(tmp)
            src = drop / "koyfin_WhinPump_test.csv"
            src.write_text("x", encoding="utf-8")
            r1 = normalize_drop_dir(drop, dry_run=True)
            r2 = normalize_drop_dir(drop, dry_run=True)
            self.assertEqual(r1.renamed, r2.renamed)
            self.assertGreaterEqual(r1.renamed, 1)
            self.assertTrue(any("credit_" in a for a in r1.actions))

    def test_meta_payload_matches_dictionary(self):
        payload = build_meta_payload()
        self.assertEqual(payload["version"], "1.0")
        self.assertEqual(payload["status"], "Locked")
        self.assertTrue(payload["validated"])


if __name__ == "__main__":
    unittest.main()