#!/usr/bin/env bash
# Rename raw Barchart/Koyfin downloads → canonical staged filename contract.
# Authority: Master Data Dictionary v1.0 — rules from whinfell_pipeline/data_dictionary.yaml
# Usage: scripts/normalize_whinfell_drop.sh [drop_dir] [--dry-run]
# Default drop_dir: ~/Downloads/whinfell_drop
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
DROP="${1:-$HOME/Downloads/whinfell_drop}"
DRY=""
if [[ "${2:-}" == "--dry-run" ]] || [[ "${1:-}" == "--dry-run" ]]; then
  DRY="--dry-run"
  if [[ "${1:-}" == "--dry-run" ]]; then
    DROP="${2:-$HOME/Downloads/whinfell_drop}"
  fi
fi

cd "$REPO"
exec python3 run_batch_collect.py normalize --drop "$DROP" $DRY