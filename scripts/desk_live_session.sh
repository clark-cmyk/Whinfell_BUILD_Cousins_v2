#!/usr/bin/env bash
# Desk live session — newest quarantine flows → sidecar → hydration bundle.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
HYDRATE_OUT="${HYDRATE_OUT:-$ROOT/data/hydration/latest.json}"

echo "=== Whinfell desk live session ==="
python3 -m whinfell_pipeline.desk_live_session -o "$HYDRATE_OUT"