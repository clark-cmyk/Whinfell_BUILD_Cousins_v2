#!/usr/bin/env bash
# Build static desk preview for GitHub Pages (free — no Vercel/Netlify required).
# Output: ./_desk_preview_out/  (gitignored; CI builds the same layout in Actions)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${ROOT}/_desk_preview_out"
TC="${ROOT}/08_Deliverables/Whinfell_Transmission_Control.html"
HYDRATE="${ROOT}/data/hydration/latest.json"

for f in "$TC" "${ROOT}/08_Deliverables/desk_china_ladder_models.js" "${ROOT}/08_Deliverables/data_dictionary_meta.json"; do
  if [[ ! -f "$f" ]]; then
    echo "build_desk_preview: missing required file: $f" >&2
    exit 1
  fi
done

rm -rf "$OUT"
mkdir -p "$OUT/data/hydration"

cp "$TC" "$OUT/index.html"
cp "${ROOT}/08_Deliverables/desk_china_ladder_models.js" "$OUT/"
cp "${ROOT}/08_Deliverables/data_dictionary_meta.json" "$OUT/"
if [[ -f "${ROOT}/08_Deliverables/whinfell-transmission-ladder-deep-dive.html" ]]; then
  cp "${ROOT}/08_Deliverables/whinfell-transmission-ladder-deep-dive.html" "$OUT/"
fi

HYDRATE_LOG="${ROOT}/data/hydration/hydration_log.json"
if [[ -f "$HYDRATE" ]]; then
  cp "$HYDRATE" "$OUT/data/hydration/latest.json"
  if [[ -f "$HYDRATE_LOG" ]]; then
    cp "$HYDRATE_LOG" "$OUT/data/hydration/hydration_log.json"
  fi
else
  echo "build_desk_preview: warn — no data/hydration/latest.json; deploying UI-only" >&2
  mkdir -p "$OUT/data/hydration"
  echo '{"hydration_version":"0","validation_status":"missing"}' > "$OUT/data/hydration/latest.json"
fi

# Optional cache-bust marker for operators
date -u +"%Y-%m-%dT%H:%M:%SZ" > "$OUT/BUILD_STAMP.txt"
grep -o "TC_CONSOLE_BUILD = '[^']*'" "$TC" | head -1 >> "$OUT/BUILD_STAMP.txt" 2>/dev/null || true

echo "build_desk_preview: OK → $OUT"
echo "  index.html + desk assets + data/hydration/latest.json"
du -sh "$OUT" | awk '{print "  size:", $1}'