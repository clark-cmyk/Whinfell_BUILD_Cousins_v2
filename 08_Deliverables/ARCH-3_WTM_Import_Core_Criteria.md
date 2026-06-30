# ARCH-3 — WTM-Import-Core Acceptance Criteria (Clark)

**Status:** BUILD criteria shipped · **Clark action:** create watchlist + first export  
**Date:** June 30, 2026  
**Authority:** `whinfell_pipeline/data_dictionary.yaml` → `koyfin_import_core`  
**Handoff:** `ARCH-3_WTM_Import_Core_Handoff.md`  
**Sign-off to:** TempLibby via BUILD Cousins

---

## Purpose

`WTM-Import-Core` is the **canonical cross-section snapshot universe** for daily credit/crypto sleeve ingest. It replaces the interim **WhinPump-only** path. BUILD has wired normalize rules, source routing, and collection manifest — Clark owns the one-time Koyfin UI setup and first verified export.

---

## Acceptance checklist (all required)

| # | Criterion | Pass condition |
|---|-----------|----------------|
| **A1** | Watchlist name | Saved watchlist is exactly **`WTM-Import-Core`** (case-sensitive, hyphenated) |
| **A2** | Ticker universe | All **16** tickers from `koyfin_import_core` present (order flexible) |
| **A3** | Export shape | CSV headers include **`Ticker`** and **`Last Price`** (Koyfin snapshot export) |
| **A4** | Drop location | File saved to `~/Downloads/whinfell_drop` |
| **A5** | Normalize | `normalize_whinfell_drop.sh` renames to `credit_{YYYYMMDD}_{HHMM}.csv` |
| **A6** | Stage | `run_csv_download.py daily --window 48h` stages without quarantine |
| **A7** | Route meta | Staged `.meta.json` shows `route.source_class: koyfin_snapshot_csv` |
| **A8** | Crypto sleeve | `data/crypto/v1/latest_crypto_sleeve.json` updates BTC/ETH/XRP/SOL snapshot |
| **A9** | Hydration | `data/hydration/latest.json` imports in TC · `freshness_status: fresh` |
| **A10** | Sign-off | Clark reports to TempLibby: *"WTM-Import-Core live — replaces WhinPump interim."* |

---

## Required tickers (16)

From Master Data Dictionary `universes.koyfin_import_core.tickers`:

```
BTCUSD · ETHUSD · XRPUSD · SOLUSD · HYG · JAAA · BKLN · CWB · CBON · KHYB · SPY · QQQ · XLRE · SOFR · GC1 · HG1
```

**Minimum coverage for partial pass:** all 4 crypto spot tickers + HYG + at least one credit ETF (JAAA, BKLN, CWB, CBON, or KHYB). Full pass requires all 16.

---

## Clark: step-by-step setup

### 1. Create watchlist in Koyfin

1. Open Koyfin → **Watchlists** → **New Watchlist**
2. Name: **`WTM-Import-Core`** (exact)
3. Add all 16 tickers above
4. Save watchlist (do not rename to WhinPump or ad-hoc labels)

### 2. Export CSV

1. Open saved watchlist **`WTM-Import-Core`**
2. Export → **CSV** (cross-section / snapshot with `Ticker` + `Last Price`)
3. Save to `~/Downloads/whinfell_drop`
4. Expected vendor filename pattern: `koyfin_wtm-import-core_*.csv` or `WTM-Import-Core.csv`
5. **Do not** leave browser duplicate copies (`filename (1).csv`) — delete dupes; keep one

### 3. Optional URL bookmark

Save Koyfin view URL for Comet shortcuts:

```bash
# desk_urls.yaml or env
KOYFIN_VIEW_IMPORT_CORE_URL=<your saved view URL>
```

Manifest batch id: `koyfin_import_core` (priority 3 in `collection_manifest.yaml`).

---

## BUILD verification commands

Run after first export:

```bash
cd ~/Desktop/Whinfell_BUILD_Cousins

# Step 1 — normalize vendor filename
bash scripts/normalize_whinfell_drop.sh ~/Downloads/whinfell_drop

# Step 2 — stage + hydrate (48h window)
python3 run_csv_download.py daily \
  --downloads ~/Downloads/whinfell_drop \
  --staged-root ./staged_raw \
  --operator cwt \
  --window 48h \
  --overwrite \
  --hydrate-output data/hydration/latest.json

# Step 3 — confirm route + crypto sleeve
python3 -c "
import json, glob
from pathlib import Path
metas = sorted(Path('staged_raw').glob('source=koyfin/dataset=credit/*.meta.json'))[-1:]
m = json.loads(metas[0].read_text()) if metas else {}
print('route:', m.get('route', {}).get('source_class'))
print('output_kinds:', m.get('route', {}).get('output_kinds'))
crypto = json.loads(Path('data/crypto/v1/latest_crypto_sleeve.json').read_text())
print('crypto assets:', list((crypto.get('assets') or {}).keys())[:4])
"

# Step 4 — operator confirm against production bundle
python3 -m whinfell_pipeline.desk_operator_confirm

# Step 5 — Transmission Control import
open 08_Deliverables/Whinfell_Transmission_Control.html
# Import data/hydration/latest.json → confirm lineage_hash
```

**Pass indicators:**

- `route: koyfin_snapshot_csv`
- `output_kinds` includes `snapshot_validation`
- `desk_operator_confirm` → all checks PASS
- TC hydration banner clears · 5 node cockpits present

---

## Legacy path (still accepted)

| Path | Status | Normalize glob |
|------|--------|----------------|
| `WTM-Credit-Confirmation` / WhinPump | **legacy_interim** | `koyfin_whinpump*` |
| `WTM-Import-Core` | **canonical** | `koyfin_wtm-import-core*` |

Both map to `credit_{YYYYMMDD}_{HHMM}.csv`. After A10 sign-off, desk should prefer **WTM-Import-Core** for daily AM chain.

---

## Failure triage

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Quarantine: filename mismatch | Wrong export name | Re-export from `WTM-Import-Core` watchlist |
| Quarantine: header validation | Wide time-series export, not snapshot | Use watchlist CSV export (`Ticker` + `Last Price`) |
| Missing crypto in sleeve | Crypto tickers absent from watchlist | Add BTCUSD, ETHUSD, XRPUSD, SOLUSD |
| `route.source_class` empty | Headers don't match snapshot detect | Confirm `Ticker` + `Last Price` columns |
| Duplicate `(1).csv` in drop | Browser re-download | Delete dupes before normalize |

---

## Sign-off block (Clark → TempLibby)

```
ARCH-3 WTM-Import-Core — ACCEPTED
Date: 2026-06-30
Operator: Clark
Watchlist: WTM-Import-Core (16/16 tickers)
Watchlist URL: https://app.koyfin.com/myw/fdfaaf3c-3ccc-49f8-850e-a703ccb29851
First staged file: credit_20260630_1002.csv
Route: koyfin_snapshot_csv
lineage_hash: sha256:68ff07b54f5476fc54b99974c3418673e8920e27bc48fe225cfe5b4e933ca6cb
Notes: Trimmed export from mega-watchlist to 16 core tickers; trim Koyfin watchlist UI to 16 for future exports.
```

---

## Related BUILD artifacts

| File | Role |
|------|------|
| `whinfell_pipeline/data_dictionary.yaml` | `koyfin_import_core` tickers + normalize rule |
| `whinfell_pipeline/collection_manifest.yaml` | Batch `koyfin_import_core` |
| `whinfell_pipeline/source_router.py` | `koyfin_snapshot_csv` routing |
| `08_Deliverables/Whinfell_Expanded_Operators_Guide_v1.5.md` | Desk daily chain |
| `08_Deliverables/ARCH-3_WTM_Import_Core_Handoff.md` | Short handoff summary |