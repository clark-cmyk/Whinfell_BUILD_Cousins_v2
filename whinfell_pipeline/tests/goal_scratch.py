"""Resolve goal-mode scratch dir for captured verification evidence."""

from __future__ import annotations

import os
from pathlib import Path

_DEFAULT = Path(
    "/var/folders/qn/gdsdhg9j3f77wk7fn889zbq40000gn/T/grok-goal-9f124befa95c/implementer"
)


def goal_scratch() -> Path:
    path = Path(os.environ.get("GROK_GOAL_SCRATCH", str(_DEFAULT)))
    path.mkdir(parents=True, exist_ok=True)
    return path