#!/usr/bin/env bash
# CI verification entrypoint — runs Phase 2 goal verifier.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== Whinfell CI verify ==="
python3 whinfell_pipeline/verify_phase2_goal.py