# Master Data Dictionary v1.0

**Version:** 1.0  
**Date:** June 29, 2026  
**Status:** Locked  
**Machine registry:** [`whinfell_pipeline/data_dictionary.yaml`](../whinfell_pipeline/data_dictionary.yaml)  
**Loader:** [`whinfell_pipeline/data_dictionary.py`](../whinfell_pipeline/data_dictionary.py)

---

## Purpose

Single authoritative naming contract for the Whinfell Transmission Map. Eliminates refresh failures caused by inconsistent watchlist names, file patterns, JSON keys, and column labels across Comet, pipeline, and Transmission Control.

---

## 1. Project structure

| Path | Role |
|------|------|
| `~/Desktop/Whinfell_BUILD_Cousins` | Repo root |
| `~/Downloads/whinfell_drop` | Desk CSV drop (never `~/Downloads` root) |
| `data/hydration/latest.json` | Hydration bundle output |
| `08_Deliverables/Whinfell_Transmission_Control.html` | Operator cockpit |
| `whinfell_pipeline/` | Ingestion, transform, hydrate |
| `scripts/normalize_whinfell_drop.sh` | Vendor filename → canonical rename |

Full folder map: `project_structure` in YAML.

---

## 2. Watchlist names (Koyfin saved views)

| Canonical saved view | Canonical export file | Legacy alias |
|---------------------|----------------------|--------------|
| **WTM-Rates-Credit** | `rates_{YYYYMMDD}_{HHMM}.csv` | `koyfin_YYYY-MM-DD.csv` |
| **WTM-Equities-Breadth** | `equities_{YYYYMMDD}_{HHMM}.csv` | legacy vendor files (auto-normalized) |
| **WTM-Credit-Confirmation** | `credit_{YYYYMMDD}_{HHMM}.csv` | legacy vendor files (auto-normalized) |
| **WTM-China-Policy** | `china_policy_{YYYYMMDD}_{HHMM}.csv` | — |
| **WTM-Crypto-Price** | `btc_price_chart_{YYYYMMDD}_{HHMM}.csv` | — |
| **WTM-Crypto-Correl** | `{asset}_correl_chart_{YYYYMMDD}_{HHMM}.csv` | — |
| **WTM-BTC-Basis** | `btc_basis_{YYYYMMDD}.csv` | `futures-spreads-btn26-*` |

**Planned watchlists:** `WTM-Import-Core`, `WTM-Import-Curves`, `WTM-Research-Sandbox` (never auto-ingested).

**Barchart screens:** `WTM-Futures-Intraday` → `futures_intraday_*`; `WTM-Futures-Daily` → `futures_daily_*`.

---

## 2b. Phase 2 extensions (locked June 29, 2026)

| Block | Location | Purpose |
|-------|----------|---------|
| `rv_series` | `data_dictionary.yaml` | Per-series `quartile_direction`, history keys, primary flag |
| `node_score_weights` | `data_dictionary.yaml` | Interim composite score weights per ladder node |
| Interim score doc | `04_Score_Calculation/Phase2_Interim_Node_Score_Weights.md` | Human-readable weight tables (non-credit nodes) |

---

## 3. File naming conventions

**Staged contract:**
- Observation row: `{dataset}_{YYYYMMDD}_{HHMM}.csv`
- Product/flavor: `{product}_{flavor}_{YYYYMMDD}.csv`

**Normalize before stage:** `scripts/normalize_whinfell_drop.sh ~/Downloads/whinfell_drop`

**Canonical datasets:** `rates`, `equities`, `credit`, `china_policy`, `futures_intraday`, `futures_daily`, `btc_basis`, `btc_price_chart`, `*_correl_chart`, `crypto_corr_series`.

---

## 4. JSON field names and structure

### Hydration bundle (`data/hydration/latest.json`)

| Block | Canonical fields |
|-------|------------------|
| `global` | `whinfell_score`, `transmission_state`, `regime_tag`, `btc_bias` |
| `china` | `sq3_score`, `sq3_band`, `policy_strength`, `state_impulse_score` |
| `china_ladder` | `horizons`, `weakest_china_stage` |
| `crypto_sleeve` | `assets`, `charts`, `correlation_series`, `snapshot` |
| `execution` | `near_month`, `basis_spread`, `btc_bias` |

### WTM export

- Format: **WTM EXPORT v2.1** (legacy v2.0 supported on import)
- Header fields: `whinfell_score`, `transmission_state`, `regime_tag`, `btc_bias`

### Display → field mapping

| UI label | JSON field |
|----------|------------|
| Whinfell Score | `whinfell_score` |
| Transmission State | `transmission_state` |
| Regime Tag | `regime_tag` |
| Near Month | `near_month` |
| Basis Spread | `basis_spread` |

**Never use** spaced variants (`Whinfell Score`) in machine JSON — display labels only.

---

## 5. Column mappings and ticker standards

**WTM observation rows (staged ingest):**
- Koyfin: `timestamp`, `whinfell_score`, `regime_tag`, `transmission_state`, `btc_bias`
- Barchart: `timestamp`, `near_month`, `basis_spread`, `spread_type`

**Ticker format:**
- Koyfin: plain uppercase (`BTCUSD`, `HYG`)
- Barchart crypto: caret prefix (`^BTCUSD`)
- Barchart indices: dollar prefix (`$HSI`)
- Resolution: `canonical_assets` in YAML

**Legacy aliases (compatibility only):** `BTCPRice` → `btc_spot_usd`; legacy vendor filenames → canonical via `normalize_rules`.

---

## Lock policy

- Version **1.0** is locked as of June 29, 2026.
- Changes require BUILD Cousins review + TempLibby sign-off.
- Transmission Control displays version + status on every load/refresh.
- Machine tests: `python3 -m unittest whinfell_pipeline.tests.test_data_dictionary -v`