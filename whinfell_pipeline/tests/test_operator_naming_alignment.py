"""Active operator docs must not reference legacy WhinPump/Simplify navigation."""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

ACTIVE_OPERATOR_FILES = [
    REPO_ROOT / "08_Deliverables/Perplexity_Full_Collection_Prompt.txt",
    REPO_ROOT / "08_Deliverables/Perplexity_Comet_Collection_Instructions.md",
    REPO_ROOT / "08_Deliverables/Perplexity_2.2e_Update_Prompt.txt",
    REPO_ROOT / "08_Deliverables/Comet_Shortcuts_WTM.md",
    REPO_ROOT / "08_Deliverables/Whinfell_Data_Update_Guide.md",
    REPO_ROOT / "08_Deliverables/Whinfell_Transmission_Ladder_Teach_In.md",
    REPO_ROOT / "whinfell_pipeline/examples/AGENT_COLLECTION_PROMPT.txt",
    REPO_ROOT / "whinfell_pipeline/collection_manifest.yaml",
    REPO_ROOT / "whinfell_pipeline/desk_urls.yaml",
]

FORBIDDEN = re.compile(r"WhinPump|Simplify All ETFs|koyfin_WhinPump|koyfin_Simplify", re.I)


class TestOperatorNamingAlignment(unittest.TestCase):
    def test_active_operator_files_no_legacy_navigation(self):
        violations: list[str] = []
        for path in ACTIVE_OPERATOR_FILES:
            text = path.read_text(encoding="utf-8")
            for i, line in enumerate(text.splitlines(), 1):
                if FORBIDDEN.search(line):
                    violations.append(f"{path.relative_to(REPO_ROOT)}:{i}: {line.strip()}")
        self.assertEqual(violations, [], "legacy names in active operator paths:\n" + "\n".join(violations))


if __name__ == "__main__":
    unittest.main()