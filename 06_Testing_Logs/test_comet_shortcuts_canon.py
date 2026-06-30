"""Verify Comet shortcut canon in 08_Deliverables/Comet_Shortcuts_WTM.md."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SHORTCUTS_PATH = REPO_ROOT / "08_Deliverables" / "Comet_Shortcuts_WTM.md"
ACTIVATION_PATH = REPO_ROOT / "08_Deliverables" / "BUILD_Cousins_Session_Activation.md"

CANON_SHORTCUTS = frozenset({"/roles", "/role", "/goal", "/arena", "/plan", "/wtm-morning", "/barchart-hydration"})
AUTHORITY_FILES = (
    "whinfell_pipeline/collection_manifest.yaml",
    "whinfell_pipeline/data_dictionary.yaml",
    "whinfell_pipeline/desk_urls.yaml",
)


def load_shortcuts_text() -> str:
    return SHORTCUTS_PATH.read_text(encoding="utf-8")


def defined_shortcut_tokens(text: str) -> set[str]:
    """Return shortcut tokens declared as headings in Comet_Shortcuts_WTM.md."""
    tokens: set[str] = set()
    for line in text.splitlines():
        m = re.match(r"^#{1,3}\s+`?(/[\w-]+)`?\s*$", line.strip())
        if m:
            tokens.add(m.group(1))
        m2 = re.match(r"^###\s+`?(/[\w-]+)`?\s*$", line.strip())
        if m2:
            tokens.add(m2.group(1))
    return tokens


class TestCometShortcutsCanon(unittest.TestCase):
    def test_shortcuts_file_exists(self):
        self.assertTrue(SHORTCUTS_PATH.is_file())

    def test_required_shortcuts_defined(self):
        text = load_shortcuts_text()
        for shortcut in ("/roles", "/role", "/goal", "/arena", "/plan"):
            self.assertIn(shortcut, text, f"missing {shortcut} block")

    def test_compound_wtm_morning_present(self):
        text = load_shortcuts_text()
        self.assertIn("/wtm-morning", text)
        self.assertIn("/roles", text)
        self.assertIn("/goal", text)
        self.assertIn("/arena", text)
        self.assertIn("/plan", text)

    def test_no_invented_shortcut_headings(self):
        text = load_shortcuts_text()
        declared = defined_shortcut_tokens(text)
        extras = declared - CANON_SHORTCUTS
        self.assertEqual(extras, set(), f"invented shortcuts: {sorted(extras)}")

    def test_authority_files_exist_on_disk(self):
        text = load_shortcuts_text()
        for rel_path in AUTHORITY_FILES:
            self.assertIn(rel_path, text)
            self.assertTrue((REPO_ROOT / rel_path).is_file(), rel_path)

    def test_forbidden_actions_documented(self):
        text = load_shortcuts_text()
        self.assertIn("editing pipeline code", text.lower())
        self.assertIn("trades", text.lower())

    def test_session_activation_self_identifies(self):
        self.assertTrue(ACTIVATION_PATH.is_file())
        text = ACTIVATION_PATH.read_text(encoding="utf-8")
        self.assertIn("BUILD Cousins", text)
        self.assertIn("~/Desktop/Whinfell_BUILD_Cousins", text)
        self.assertIn("support-only", text.lower())


if __name__ == "__main__":
    unittest.main()