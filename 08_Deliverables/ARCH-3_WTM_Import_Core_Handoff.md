# ARCH-3 — WTM-Import-Core Koyfin Watchlist Handoff

**Status:** BUILD spec shipped · **Clark action:** create watchlist in Koyfin UI  
**Date:** June 30, 2026  
**Authority:** `whinfell_pipeline/data_dictionary.yaml` → `koyfin_import_core`  
**Acceptance criteria:** `ARCH-3_WTM_Import_Core_Criteria.md` (Clark sign-off checklist)

---

## What BUILD shipped

| Artifact | Change |
|----------|--------|
| `data_dictionary.yaml` | `WTM-Import-Core` saved view · normalize rule `koyfin_wtm-import-core*` → `credit_{YYYYMMDD}_{HHMM}.csv` |
| `collection_manifest.yaml` | Batch export `koyfin_import_core` (priority 3) |
| `source_router.py` | Routes `koyfin_snapshot_csv` for Ticker + Last Price exports |
| Operator Guide v1.5 | Documents ARCH-3 as primary credit/snapshot path |

**Legacy path still works:** `WTM-Credit-Confirmation` / `koyfin_whinpump*` → same `credit_*.csv` contract.

---

## Clark: one-time Koyfin setup

1. In Koyfin, create watchlist **`WTM-Import-Core`** (exact name).
2. Add minimum tickers from Master DD `koyfin_import_core`:

   BTCUSD · ETHUSD · XRPUSD · SOLUSD · HYG · JAAA · BKLN · CWB · CBON · KHYB · SPY · QQQ · XLRE · SOFR · GC1 · HG1

3. Export CSV to `~/Downloads/whinfell_drop` (filename will normalize automatically).
4. Optional: save Koyfin URL to env `KOYFIN_VIEW_IMPORT_CORE_URL` or `desk_urls.yaml`.

---

## Verify

```bash
cd ~/Desktop/Whinfell_BUILD_Cousins
bash scripts/normalize_whinfell_drop.sh ~/Downloads/whinfell_drop
python3 run_csv_download.py daily --window 48h --overwrite
# Confirm: credit_*.csv staged · crypto_sleeve snapshot ingested · lineage_hash updated
```

---

## Report to TempLibby

When live: "WTM-Import-Core replaces WhinPump interim for daily snapshot + crypto sleeve ingest."