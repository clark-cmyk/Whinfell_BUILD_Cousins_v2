# Whinfell Expanded Operator's Guide v1.4

**Version:** 1.4  
**Date:** June 27, 2026  
**Authority:** TempLibby, Template Team · Comet Runbook Integration  
**Status:** Production — Daily CSV Chain Shipped  
**Primary file:** `Whinfell_Transmission_Control.html`  
**Quick ref:** `Whinfell_Quick_Reference_Card_v1.4.docx`  
**Runbook entry:** `run_csv_download.py`  
**Browser blueprint:** `08_Deliverables/Comet_Browser_Operations_Blueprint.md`

---

## 1. System Architecture

| Layer | Tool | Role |
|-------|------|------|
| **Research & Analysis** | Perplexity (Prompts A–E) | Regime read, sizing, trade eval, income, divergence |
| **Execution & State** | Transmission Control (HTML) | Intake, gates, gross risk, tracer, BTC modules |
| **Live Data** | Koyfin + Barchart (browser tabs) | Transmission map, futures/basis |
| **CSV Collector** | Comet + `run_csv_download.py` | Download → stage → Parquet → hydration |

**No iframes.** Control surface opens live data in dedicated tabs.

---

## 2. Open Commands

```bash
# Primary execution layer (Phase 2.2)
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Transmission_Control.html

# Quick Reference Card (print at desk)
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Quick_Reference_Card_v1.4.docx

# Legacy full cockpit (optional)
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Operator_Dashboard.html
```

---

## 3. Daily CSV Chain (Comet Runbook — Primary Path)

**One command (recommended — use 48h window, not `today`):**

```bash
cd ~/Desktop/Whinfell_BUILD_Cousins
bash scripts/normalize_whinfell_drop.sh ~/Downloads/whinfell_drop
python3 run_csv_download.py daily \
  --operator cwt \
  --window 48h \
  --downloads ~/Downloads/whinfell_drop \
  --staged-root ./staged_raw \
  --hydrate-output data/hydration/latest.json \
  --overwrite
```

Then in Transmission Control: **Import** `data/hydration/latest.json` → confirm import using **`lineage_hash`** (not file timestamp) → review **Suggested Tracer** → **Accept** or **Dismiss** → **Save State**.

**Morning shortcut:** `./whinfell_daily_am.sh` or `python3 Whinfell_Daily_Launcher.py` (both run normalize + 48h chain)

### Step-by-step (manual control)

```bash
# One-time folder setup
python3 run_csv_download.py init

# Copy browser CSV exports from ~/Downloads → staged_raw/ (never moves originals)
python3 run_csv_download.py stage --operator desk --window today

# Ingest staged CSVs → Parquet + execution sidecar (archives processed CSVs)
python3 run_csv_download.py collect

# Build hydration bundle for Transmission Control
python3 run_csv_download.py hydrate --hydrate-output data/hydration/latest.json
```

### Staged folder contract (`staged_raw/`)

| Folder | Datasets |
|--------|----------|
| `source=koyfin/dataset=rates/` | + `credit`, `equities`, `flows` |
| `source=barchart/dataset=futures_intraday/` | + `futures_daily`, `options`, `greeks` |
| `source=china_policy/` | CSV at source root |

**Filename patterns (required):**

- `{dataset}_{YYYYMMDD}_{HHMM}.csv` — e.g. `rates_20260627_1400.csv`, `flows_20260629_1017.csv`
- `{product}_{flavor}_{YYYYMMDD}.csv` — e.g. `btc_basis_20260627.csv`

**Pre-stage rename:** Raw Barchart/Koyfin/WTM export names → canonical contract via `scripts/normalize_whinfell_drop.sh` (includes `WTM-Flows*.csv`, `WTM-Global-Rates.csv`, `WTM-Equities-Breath.csv`, etc.).

### Sidecars, quarantine, manifests

| Artifact | Location | Purpose |
|----------|----------|---------|
| `.meta.json` | Next to each staged CSV | Operator, sha256, source/dataset, validation status |
| `quarantine/` | `staged_raw/quarantine/YYYYMMDD/` | Bad filenames or header failures (copy preserved) |
| `stage_manifest__*.json` | `staged_raw/manifests/` | Stage run audit trail |
| `daily_manifest__*.json` | `staged_raw/manifests/` | Full daily chain result |

### Alternate ingest path (unchanged)

```bash
python3 -m whinfell_pipeline.ingest --staged
python3 -m whinfell_pipeline.hydrate -o data/hydration/latest.json
```

---

## 4. Comet Browser Operations Blueprint

Full spec: `08_Deliverables/Comet_Browser_Operations_Blueprint.md`

### One-time setup checklist

1. `scripts/init_daily_csv.sh` — staged folders + `data/hydration/`
2. Save **Koyfin backup views:** `WTM-Rates-Credit`, `WTM-Equities-Breadth`, `WTM-Credit-Confirmation`, `WTM-China-Policy`
3. Save **Barchart backup views:** `WTM-Futures-Intraday`, `WTM-Futures-Daily`, `WTM-BTC-Basis`, `WTM-Options-Greeks`
4. Add **Comet memorized shortcuts:** `wtm control`, `wtm koyfin rates`, `wtm barchart futures`, `wtm daily csv`, `wtm hydrate import`, `wtm morning`
5. Bookmark Transmission Control · print Quick Reference v1.4 · run one test daily chain

### Koyfin backup views → CSV exports

| View | Export filename |
|------|-----------------|
| WTM-Rates-Credit | `rates_YYYYMMDD_HHMM.csv` |
| WTM-Equities-Breadth | `equities_YYYYMMDD_HHMM.csv` |
| WTM-Credit-Confirmation | `credit_YYYYMMDD_HHMM.csv` |
| WTM-China-Policy | `china_policy_YYYYMMDD_HHMM.csv` |

### Barchart backup views → CSV exports

| View | Export filename |
|------|-----------------|
| WTM-Futures-Intraday | `futures_intraday_YYYYMMDD_HHMM.csv` |
| WTM-Futures-Daily | `futures_daily_YYYYMMDD_HHMM.csv` |
| WTM-BTC-Basis | `btc_basis_YYYYMMDD.csv` |
| WTM-Options-Greeks | `options_YYYYMMDD_HHMM.csv` |

### Supervised Comet control (Clark)

Paste the supervised collection prompt from the blueprint at shift start. Comet assists exports and reminds Clark to approve before `run_csv_download.py daily`. **No auto-trading.**

### Saved Prompts Utility Block

Copy from blueprint §6 for Comet/Perplexity — Prompts A–E plus hydration reminder.

---

## 5. Daily Workflow (Research + Pipeline)

| Step | Action |
|------|--------|
| 1 | Export CSVs from Koyfin / Barchart / China collector into **Downloads** |
| 2 | Run `python3 run_csv_download.py daily` (or stage → collect → hydrate) |
| 3 | **Import Latest Hydration Bundle** in Transmission Control (`data/hydration/latest.json`) |
| 4 | Review command bar (Pipeline badge) · freshness chip · provenance |
| 5 | **Accept** or **Dismiss** Suggested Tracer — matrix never auto-fills |
| 6 | Run Prompts B–E as needed · **Save State** |

Perplexity **WTM EXPORT v2.1** import remains valid for research handoff when CSV path is unavailable.

---

## 6. WTM EXPORT v2.1 (Canonical Handoff)

Spec: `whinfell_pipeline/WTM_EXPORT_v2.1_SPEC.md`

Includes Global core, China SQ3, optional Signal Tracer lines, provenance (Snapshot ID, Lineage Hash, Data As Of, Freshness).  
Parquet hydration strips embedded tracer lines — suggestions surface in the amber panel only (`confirm_required`).

---

## 7. Gate Rules

| Score | Gate | BTC Access | Banner |
|-------|------|------------|--------|
| &lt; 50 | NO NEW BTC RISK | Blocked | Red |
| 50–64 | Tight Risk Band | Reduced sizing | Amber |
| ≥ 65 | Allowed | Full access | Green |

**Posture ladder:** Full (80+) · Selective (65–79) · Light (50–64) · Defensive (&lt;50) · Flat

---

## 8. Hybrid Signal Tracer (2.2b)

- Import surfaces **Suggestions Pending** — never writes horizon matrix until **Accept**
- **Dismiss** clears suggestions only
- **Manual Override** or horizon edits set amber matrix + command bar **Override**
- Intake/gross/L3-only edits flip command bar **Override** without changing tracer flow

---

## 9. WTM Prompts

| ID | Title | Use When |
|----|-------|----------|
| A | Transmission Read & Regime Classification | Shift start, regime change |
| B | Posture & Gross-Risk Recommendation | Sizing decisions |
| C | Trade Evaluation & Ranking | Candidate trade list |
| D | Income Projection from Current Book | Session/week P&L outlook |
| E | Divergence & Risk Compression | Tape vs WTM mismatch |
| L2 | BTC Options Workflow | Vol surface / structures |
| L3 | BTC Calendar Arb Agent | Calendar spreads |

---

## 10. Persistence

- **Save State** → `localStorage` key `whinfell_transmission_control_v1`
- Snapshots stored in schema v3 (max 12)
- Daily manifests in `staged_raw/manifests/` for desk audit

---

## 11. Troubleshooting

| Symptom | Check |
|---------|-------|
| File quarantined | Filename pattern + required CSV headers (see `staged_raw/README.md`) |
| `files_found=0` on collect | Re-run `stage` or confirm CSVs not already archived |
| Stale freshness chip | Re-run daily chain; confirm latest Parquet row timestamp |
| Override badge stuck | Re-import hydration to reset pipeline authority |

---

## 12. Support

| Role | Contact |
|------|---------|
| System owner | TempLibby |
| Build support | BUILD Cousins (Bridge) |
| CSV collector | Comet runbook · `run_csv_download.py` |

**Ship:** Phase 2.2 Final — Comet browser blueprint + daily CSV chain · June 27, 2026