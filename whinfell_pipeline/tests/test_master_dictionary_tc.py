"""Transmission Control Master Data Dictionary badge — source + headless render."""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

TC_HTML = REPO_ROOT / "08_Deliverables" / "Whinfell_Transmission_Control.html"


class TestMasterDictionaryTransmissionControl(unittest.TestCase):
    def test_html_contains_dd_badge_element(self):
        text = TC_HTML.read_text(encoding="utf-8")
        self.assertIn('id="ddVersionBadge"', text)
        self.assertIn("Master Data Dictionary v1.0", text)

    def test_html_defines_render_function(self):
        text = TC_HTML.read_text(encoding="utf-8")
        self.assertIn("function renderDataDictionaryBadge()", text)
        self.assertIn("MASTER_DATA_DICTIONARY_VERSION = '1.0'", text)
        self.assertIn("MASTER_DATA_DICTIONARY_STATUS = 'Locked'", text)

    def test_render_all_calls_dd_badge(self):
        text = TC_HTML.read_text(encoding="utf-8")
        m = re.search(r"function renderAll\(\)\s*\{([^}]+renderDataDictionaryBadge)", text, re.DOTALL)
        self.assertIsNotNone(m, "renderAll must call renderDataDictionaryBadge on refresh")


if __name__ == "__main__":
    unittest.main()