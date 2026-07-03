#!/usr/bin/env bash
# Build static desk preview for GitHub Pages (free — no Vercel/Netlify required).
# Output: ./_desk_preview_out/  (gitignored; CI builds the same layout in Actions)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${ROOT}/_desk_preview_out"
TC="${ROOT}/08_Deliverables/Whinfell_Transmission_Control.html"
HYDRATE="${ROOT}/data/hydration/latest.json"

BW="${ROOT}/08_Deliverables/Whinfell_BasisWatch.html"
BWC="${ROOT}/08_Deliverables/basis_watch.css"
for f in "$TC" "$BW" "$BWC" "${ROOT}/08_Deliverables/desk_china_ladder_models.js" "${ROOT}/08_Deliverables/basis_watch_panel.js" "${ROOT}/08_Deliverables/basis_watch_analytics.js" "${ROOT}/08_Deliverables/data_dictionary_meta.json"; do
  if [[ ! -f "$f" ]]; then
    echo "build_desk_preview: missing required file: $f" >&2
    exit 1
  fi
done

rm -rf "$OUT"
mkdir -p "$OUT/data/hydration"

cp "$TC" "$OUT/index.html"
cp "$BW" "$OUT/Whinfell_BasisWatch.html"
cp "$BWC" "$OUT/basis_watch.css"
cp "${ROOT}/08_Deliverables/desk_china_ladder_models.js" "$OUT/"
cp "${ROOT}/08_Deliverables/basis_watch_panel.js" "$OUT/"
cp "${ROOT}/08_Deliverables/basis_watch_analytics.js" "$OUT/"
cp "${ROOT}/08_Deliverables/data_dictionary_meta.json" "$OUT/"
BARCHART_CURVE="${ROOT}/data/barchart/v1/barchart_curve_history.json"
if [[ -f "$BARCHART_CURVE" ]]; then
  mkdir -p "$OUT/data/barchart/v1"
  cp "$BARCHART_CURVE" "$OUT/data/barchart/v1/barchart_curve_history.json"
  mkdir -p "$OUT/data/barchart"
  cp "$BARCHART_CURVE" "$OUT/data/barchart/barchart_curve_history.json"
fi
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

for req in desk_china_ladder_models.js basis_watch_analytics.js basis_watch_panel.js basis_watch.css data_dictionary_meta.json; do
  if [[ ! -f "$OUT/$req" ]]; then
    echo "build_desk_preview: missing output asset: $OUT/$req" >&2
    exit 1
  fi
done
if ! grep -q 'src="desk_china_ladder_models.js"' "$OUT/index.html"; then
  echo "build_desk_preview: index.html missing desk_china_ladder_models.js script tag" >&2
  exit 1
fi

echo "build_desk_preview: OK → $OUT"
echo "  index.html + desk assets + data/hydration/latest.json"
du -sh "$OUT" | awk '{print "  size:", $1}'