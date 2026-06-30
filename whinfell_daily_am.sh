#!/bin/zsh
set -euo pipefail

cd ~/Desktop/Whinfell_BUILD_Cousins

bash scripts/normalize_whinfell_drop.sh ~/Downloads/whinfell_drop

python3 run_csv_download.py daily \
  --operator cwt \
  --window 48h \
  --downloads ~/Downloads/whinfell_drop \
  --staged-root ./staged_raw \
  --hydrate-output data/hydration/latest.json \
  --overwrite

open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Transmission_Control.html

# Optional — update free GitHub Pages desk preview for Wes (no cost):
# bash scripts/publish_desk_preview.sh