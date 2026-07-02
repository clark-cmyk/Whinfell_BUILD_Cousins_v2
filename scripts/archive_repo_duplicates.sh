#!/usr/bin/env bash
# Move macOS " 2" duplicate copies and incomplete downloads into Archive.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ARCHIVE="$ROOT/Archive/repo_cleanup_$(date -u +%Y%m%d)"
mkdir -p "$ARCHIVE"

dup_count=0
while IFS= read -r -d '' f; do
  rel="${f#./}"
  dest="$ARCHIVE/$rel"
  mkdir -p "$(dirname "$dest")"
  mv "$f" "$dest"
  dup_count=$((dup_count + 1))
done < <(find "$ROOT" -name '* 2.*' -not -path "$ROOT/Archive/*" -not -path "$ROOT/.git/*" -print0)

cr_count=0
while IFS= read -r -d '' f; do
  rel="${f#$ROOT/}"
  dest="$ARCHIVE/$rel"
  mkdir -p "$(dirname "$dest")"
  mv "$f" "$dest"
  cr_count=$((cr_count + 1))
done < <(find "$ROOT" -name '*.crdownload' -not -path "$ROOT/Archive/*" -not -path "$ROOT/.git/*" -print0)

echo "archive_repo_duplicates: moved $dup_count duplicate(s), $cr_count .crdownload file(s) → $ARCHIVE"