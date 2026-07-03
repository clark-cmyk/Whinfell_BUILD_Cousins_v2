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

# Ensure no Jekyll processing on GitHub Pages (critical for reliable asset serving)
touch "$OUT/.nojekyll"

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
# --- INLINE ASSETS FOR SINGLE-FILE RELIABILITY ON GITHUB PAGES ---
# Eliminates relative asset 404s for JS/CSS. The main desk becomes one reliable file.
echo "build_desk_preview: inlining CSS + JS into index.html ..."

python3 << 'PYEOF'
import os

out_dir = "_desk_preview_out"
index_path = os.path.join(out_dir, "index.html")
css_path = os.path.join(out_dir, "basis_watch.css")
files = [
    ("desk_china_ladder_models.js", os.path.join(out_dir, "desk_china_ladder_models.js")),
    ("basis_watch_analytics.js", os.path.join(out_dir, "basis_watch_analytics.js")),
    ("basis_watch_panel.js", os.path.join(out_dir, "basis_watch_panel.js")),
]

with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Inline CSS - replace link with full style block
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()
    style_block = '<style id="inlined-basis-watch">\n/* INLINED from basis_watch.css for GitHub Pages reliability */\n' + css_content + '\n</style>'
    # Remove original link tag(s)
    html = html.replace('<link rel="stylesheet" href="basis_watch.css" />', style_block)
    html = html.replace("basis_watch.css", "/* inlined */", 1)  # safety

# Inline the three support scripts by replacing their tags with full content in order.
# These must run before the huge main <script> block.
for label, p in files:
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            js = f.read()
        inline = f'\n<script data-inlined="true" id="inlined-{label.split(".")[0]}">\n/* INLINED {label} */\n{js}\n</script>\n'
        # Remove the external tag (exact common form)
        tag = f'<script src="{label}"></script>'
        if tag in html:
            html = html.replace(tag, inline, 1)
        else:
            # try single quotes or self-closing variations
            for t in [f"<script src='{label}'></script>", f'<script src="{label}"/>', f"<script src='{label}'/>"]:
                if t in html:
                    html = html.replace(t, inline, 1)
                    break

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print("  SUCCESS: index.html is now self-contained (CSS + 3 JS inlined)")
PYEOF

# Verify core app code is present (appState / renderAll)
if grep -q 'window\.appState = appState' "$OUT/index.html" && (grep -q 'function renderAll()' "$OUT/index.html" || grep -q 'window\.renderAll = renderAll' "$OUT/index.html"); then
  echo "  Verified: window.appState and renderAll present in the built index.html"
else
  echo "  WARNING: core globals may be missing after inlining" >&2
fi

echo "build_desk_preview: OK → $OUT"
echo "  index.html + desk assets + data/hydration/latest.json"
du -sh "$OUT" | awk '{print "  size:", $1}'