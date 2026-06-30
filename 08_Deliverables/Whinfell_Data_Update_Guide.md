# Whinfell Data Update Guide — Step by Step

**Version:** 1.0  
**Date:** 2026-06-28  
**Authority:** Clark · BUILD Cousins desk  
**Audience:** Desk operators, junior analysts, Perplexity, Comet  
**Companion:** `Whinfell_Expanded_Operators_Guide_v1.4.md` · `Perplexity_Comet_Collection_Instructions.md` · `Whinfell_Transmission_Ladder_Teach_In.md`

---

## Quick navigation

| Section | Jump to |
|---------|---------|
| Who does what | [§1 Actor & role matrix](#1-actor--role-matrix) |
| Perplexity integration map | [§2 Perplexity integration points](#2-perplexity-integration-points) |
| End-to-end flow (diagram) | [§3 Data flow](#3-data-flow-overview) |
| One-time setup | [§4 Phase 0](#phase-0--one-time-setup) |
| Morning collect (Perplexity) | [§5 Phase 1](#phase-1--morning-data-collect-perplexity--comet) |
| Python pipeline | [§6 Phase 2](#phase-2--python-pipeline-clark-or-agent) |
| Transmission Control import | [§7 Phase 3](#phase-3--desk-import-transmission-control) |
| Research prompts A–E | [§8 Phase 4](#phase-4--research-layer-perplexity-prompts-ae) |
| Deep dive review | [§9 Phase 5](#phase-5--deep-dive--ladder-review) |
| Alternate paths | [§10 Alternates](#10-alternate--fallback-paths) |
| Troubleshooting | [§11 Troubleshooting](#11-troubleshooting) |
| Prompt index | [§12 Perplexity prompt index](#12-perplexity-prompt-index) |

---

## 1. Actor & role matrix

| Actor | Primary role | Touches data? | Touches risk? |
|-------|--------------|---------------|---------------|
| **Perplexity (collect mode)** | Browser CSV export robot — 8 bulk screens | Yes — downloads only | **No** |
| **Perplexity (research mode)** | Regime read, trade ranking, WTM EXPORT v2.1 narrative | Yes — text handoff only | **No** (recommendations only) |
| **Comet** | Supervised collect — same as Perplexity collect with Clark approval gates | Yes — downloads + terminal on approval | **No** |
| **Clark / desk lead** | Approve pipeline, import hydration, Accept/Dismiss tracer, Save State | Yes — authoritative | **Yes** |
| **Junior analyst** | Verify marks vs Koyfin/Barchart, update tracer if needed | Yes — manual overrides | With senior |
| **Python pipeline** | Rename, raw→WTM (2.2e), stage, Parquet, `latest.json` | Yes — automated | **No** |
| **Grok** | Operator narrative from `grok_payload` / WHY blocks | Read-only on saved state | **No** |

**Golden rule:** Only Clark (or designated senior) changes book posture after **Import → Accept/Dismiss → Save State**.

---

## 2. Perplexity integration points

Perplexity is **not one tool** on this desk — it has **four distinct integration points**:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│ INTEGRATION POINT 1 — FAST CSV COLLECT (daily, required)                │
│ Paste: Perplexity_Full_Collection_Prompt.txt (+ 2.2e update if needed)  │
│ Role: Export robot · 8 screens · whinfell_drop · run_batch_collect      │
│ Output: data/hydration/latest.json (via pipeline)                       │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ INTEGRATION POINT 2 — DESK IMPORT (Clark; Perplexity reminds only)      │
│ Surface: Transmission Control → Import Latest Hydration Bundle          │
│ Role: Perplexity does NOT click import — reports path + checklist       │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ INTEGRATION POINT 3 — RESEARCH PROMPTS A–E (as needed, parallel)        │
│ Paste: Comet_Browser_Operations_Blueprint.md §6 utility block            │
│ Role: Regime narrative, sizing, trade rank, income, divergence          │
│ Output: WTM EXPORT v2.1 text block (manual paste if CSV path down)      │
└─────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────┐
│ INTEGRATION POINT 4 — CHINA POLICY EXPORT (optional / manual)           │
│ Format: CHINA POLICY EXPORT v1.0 (see china_policy_track/examples)      │
│ Role: Qualitative China read when Koyfin china CSV insufficient         │
│ Output: Manual intake or china_policy CSV path                            │
└─────────────────────────────────────────────────────────────────────────┘
```

### What Perplexity must never do

- Parse or summarize CSV contents in the browser agent  
- Loop 13 Barchart tickers for **daily** collect  
- Invent Whinfell scores, regime tags, or tracer marks  
- Execute trades or change risk limits  
- Skip `whinfell_drop` or manual rename (Python handles rename + 2.2e transform)  
- Auto-click **Accept** on Suggested Tracer (Clark only)

### What Perplexity must always do (collect mode)

1. Read `comet_collection_plan.json` + `desk_urls.yaml`  
2. Export **minimum 6** files (rates + futures_intraday + futures_daily required)  
3. Save to `~/Downloads/whinfell_drop`  
4. Run `python3 run_batch_collect.py run --window today`  
5. Post **WHINFELL COLLECT REPORT** template (see §5.4)

---

## 3. Data flow overview

```text
 Koyfin (4) + Barchart (2–4)
         │  Export CSV
         ▼
 ~/Downloads/whinfell_drop
         │  run_batch_collect.py run
         │    ├─ normalize (vendor → canonical names)
         │    ├─ raw→WTM transform (2.2e)
         │    ├─ stage → staged_raw/
         │    ├─ collect → Parquet
         │    └─ hydrate → data/hydration/latest.json
         ▼
 Transmission Control
         │  Import Latest Hydration Bundle
         │  Review Suggested Tracer (amber panel)
         │  Accept OR Dismiss
         │  Save State → localStorage
         ▼
 Deep Dive page (reads hydration / saved state)
         │  Optional: Perplexity Prompts B–E on posture
         ▼
 Desk action (Clark)
```

---

# PHASE 0 — One-time setup

**Owner:** Clark (Perplexity assists navigation only)

| Step | Action | Perplexity role |
|------|--------|-----------------|
| 0.1 | Clone/open repo `~/Desktop/Whinfell_BUILD_Cousins` | None |
| 0.2 | `python3 run_csv_download.py init` | None |
| 0.3 | `mkdir -p ~/Downloads/whinfell_drop` | Confirm folder exists before first collect |
| 0.4 | Save Koyfin dashboards: `WTM-Rates-Credit`, `WTM-Equities-Breadth`, `WTM-Credit-Confirmation`, `WTM-China-Policy` | Open each once to verify names |
| 0.5 | Save Barchart lists/screens per `desk_urls.yaml` | Verify `dailymonitor0610` or Major Commodities |
| 0.6 | Paste Koyfin Share links into `whinfell_pipeline/desk_urls.yaml` (replace `REPLACE_ME`) | Read YAML; report which `needs_clark_url: true` remain |
| 0.7 | Test chain: `python3 run_batch_collect.py plan` then `status` | Read JSON plan aloud to Clark |
| 0.8 | Bookmark Transmission Control + Deep Dive launchers | None |
| 0.9 | Save Perplexity collection prompt as pinned thread | Clark pastes `Perplexity_Full_Collection_Prompt.txt` |

**Verification:** `python3 run_batch_collect.py status` shows required batch IDs documented in `comet_collection_plan.json`.

---

# PHASE 1 — Morning data collect (Perplexity / Comet)

**Target time:** 3–5 minutes browser + ~30s pipeline  
**Perplexity mode:** **CSV export robot only**

## Step 1.1 — Load machine plan

```bash
cd ~/Desktop/Whinfell_BUILD_Cousins
python3 run_batch_collect.py plan
```

Perplexity reads (do not paraphrase):

- `whinfell_pipeline/examples/comet_collection_plan.json`
- `whinfell_pipeline/desk_urls.yaml`

Optional — open wired URLs:

```bash
python3 run_batch_collect.py open
```

## Step 1.2 — The 8 exports

**Save every file to:** `~/Downloads/whinfell_drop`  
**Never save to:** `~/Downloads` root

### Koyfin — 4 exports (Perplexity executes)

| Step | ID | Navigation | Export clicks | Canonical name |
|------|-----|------------|-------------|----------------|
| 1 | `koyfin_rates` | My Dashboards → **WTM-Rates-Credit** | ⋮ → Export → CSV | `rates_YYYYMMDD_HHMM.csv` |
| 2 | `koyfin_equities` | My Dashboards → **WTM-Equities-Breadth** (canonical) | ⋮ → Export → CSV | `equities_YYYYMMDD_HHMM.csv` |
| 3 | `koyfin_credit` | My Dashboards → **WTM-Credit-Confirmation** (canonical) | ⋮ → Export → CSV | `credit_YYYYMMDD_HHMM.csv` |
| 4 | `koyfin_china` | **WTM-China-Policy** | ⋮ → Export → CSV | `china_policy_YYYYMMDD_HHMM.csv` |

**Assist URLs** (sanity check you're on desk screens):

- [USGG2Y10Y](https://app.koyfin.com/macro/USGG2Y10Y) · [DGS10](https://app.koyfin.com/macro/DGS10)
- [IWM](https://app.koyfin.com/etf/IWM.US) · [SPY](https://app.koyfin.com/etf/SPY.US)
- [HYG](https://app.koyfin.com/etf/HYG.US) · [LQD](https://app.koyfin.com/etf/LQD.US)

### Barchart — 3 required + 1 optional (Perplexity executes)

| Step | ID | Wired URL | Export | Canonical name |
|------|-----|-----------|--------|----------------|
| 5 | `barchart_futures_intraday` | [Major Commodities](https://www.barchart.com/futures/major-commodities) | Download CSV | `futures_intraday_YYYYMMDD_HHMM.csv` |
| 6 | `barchart_futures_daily` | [BTM26 Historical](https://www.barchart.com/futures/quotes/BTM26/historical-download) | Download CSV | `futures_daily_YYYYMMDD_HHMM.csv` |
| 7 | `barchart_btc_basis` | [BTM26 Spreads](https://www.barchart.com/futures/quotes/BTM26/spreads) | Download CSV | `btc_basis_YYYYMMDD.csv` |
| 8 | `barchart_options` | [BTN26 Options](https://www.barchart.com/futures/quotes/BTN26/options) | Download CSV | `options_YYYYMMDD_HHMM.csv` |

**Minimum for `ready=True`:** steps **1, 5, 6** (rates + intraday + daily).

**Raw vendor filenames are OK** after 2.2e — examples:

- `koyfin_2026-06-28.csv`
- `bitcoin-futures-prices-intraday-06-28-2026.csv`
- `btm26_daily-nearby_historical-data-06-28-2026.csv`

## Step 1.3 — Perplexity forbidden checklist (self-audit before terminal)

```text
□ I did NOT loop BT1 → ER1 → … → VI*1 for daily collect
□ I did NOT read or summarize any CSV cell contents
□ I did NOT save to ~/Downloads (only whinfell_drop)
□ I did NOT manually rename files
□ I did NOT leave duplicate "filename (1).csv" copies
```

## Step 1.4 — Run pipeline (Perplexity or Clark)

```bash
cd ~/Desktop/Whinfell_BUILD_Cousins
python3 run_batch_collect.py run --window today
```

**What this does (2.2e):**

1. Normalizes vendor filenames → canonical staged names  
2. Transforms raw headers → single-row WTM observation CSVs  
3. Copies to `staged_raw/` (never deletes drop originals)  
4. Runs collect → Parquet  
5. Writes **`data/hydration/latest.json`**

Check:

```bash
python3 run_batch_collect.py status
```

## Step 1.5 — Perplexity report template (mandatory)

Post to Clark:

```text
WHINFELL COLLECT REPORT
Date/Time: ___________
Mode: FAST BATCH (8 exports)

Exports completed:
  [ ] Step 1  koyfin_rates
  [ ] Step 2  koyfin_equities
  [ ] Step 3  koyfin_credit
  [ ] Step 4  koyfin_china
  [ ] Step 5  barchart_intraday
  [ ] Step 6  barchart_daily
  [ ] Step 7  barchart_btc_basis (optional)
  [ ] Step 8  barchart_options (optional)

Files in whinfell_drop: [list filenames]
Pipeline command run: YES / NO
  files_staged: ___
  files_quarantined: ___
  hydration_bundle: data/hydration/latest.json
  transform: raw→WTM automatic (2.2e)

Errors / warnings: ___________

Next step for Clark:
  Transmission Control → Import Latest Hydration Bundle
  → Review Suggested Tracer → Accept OR Dismiss → Save State
```

### Comet difference (supervised)

Comet uses the same steps but **asks Clark** before `run`:

> "Ready to run batch collect?"

Paste supervised block from `Perplexity_Comet_Collection_Instructions.md` § Paste prompt — Comet.

---

# PHASE 2 — Python pipeline (Clark or agent)

**Owner:** Clark approves; Perplexity may run terminal if explicitly authorized

## Path A — Fast batch (recommended)

```bash
python3 run_batch_collect.py run --window today
```

## Path B — Legacy daily chain (Downloads root)

If Clark exported to `~/Downloads` instead of `whinfell_drop`:

```bash
cd ~/Desktop/Whinfell_BUILD_Cousins
python3 run_csv_download.py daily \
  --operator desk \
  --window today \
  --hydrate-output data/hydration/latest.json
```

## Path C — Manual step-by-step (debug)

```bash
python3 run_csv_download.py init
python3 run_csv_download.py stage --operator desk --window today
python3 run_csv_download.py collect --operator desk
python3 run_csv_download.py hydrate --hydrate-output data/hydration/latest.json
```

## Path D — Clark one-liner morning script

```bash
scripts/whinfell_morning_collect.sh
```

Opens URLs → watches `whinfell_drop` → auto-runs pipeline when files land.

## Path E — Barchart API (Clark only, no browser)

```bash
export BARCHART_API_KEY="..."
python3 run_batch_collect.py fetch-api
python3 run_batch_collect.py run --window today
```

**Perplexity role:** None unless Clark provides API path explicitly.

### Pipeline outputs (verify)

| Artifact | Path | Purpose |
|----------|------|---------|
| Hydration bundle | `data/hydration/latest.json` | TC import |
| Stage manifest | `staged_raw/manifests/stage_manifest__*.json` | Audit |
| Daily manifest | `staged_raw/manifests/daily_manifest__*.json` | Audit |
| Quarantine | `staged_raw/quarantine/YYYYMMDD/` | Failed headers/names |
| Sidecar meta | `*.csv.meta.json` next to staged CSV | Lineage |

---

# PHASE 3 — Desk import (Transmission Control)

**Owner:** Clark (Perplexity **reminds only** — does not operate gates)

## Step 3.1 — Open console

```bash
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Transmission_Control.html
```

Or: `Whinfell_Transmission_Control.command`

## Step 3.2 — Import hydration bundle

1. Click **Import Latest Hydration Bundle**  
2. Select: `data/hydration/latest.json`  
   - Path: Desktop → Whinfell_BUILD_Cousins → data → hydration → latest.json  
3. Confirm status chip under button (not "No bundle imported")

**What imports automatically:**

| Field group | Source in bundle |
|-------------|------------------|
| Global intake | `global.whinfell_score`, `regime_tag`, `transmission_state`, … |
| China policy | `china.*` SQ3 inputs |
| Execution / L3 | `execution.*` basis fields when present |
| Tracer **suggestions** | `suggested_tracer` — **not written to matrix until Accept** |

## Step 3.3 — Hybrid Signal Tracer (2.2b)

```text
1. Amber panel: "Suggestions Pending"
2. Review suggested marks vs your Koyfin/Barchart read
3. Accept  → writes horizons + green "Operator Confirmed"
4. Dismiss → clears suggestions only (matrix unchanged)
5. Manual horizon edit → Override badge (document why)
```

**Perplexity role:** None. Junior analyst may **recommend** Accept/Dismiss with evidence; Clark decides.

## Step 3.4 — Command bar review

Check:

- Pipeline / freshness badge  
- Provenance: `data_as_of`, `snapshot_id`, `freshness_status`  
- Gate banner vs Whinfell Score  
- Override vs Pipeline authority  

## Step 3.5 — Save State

Click **Save State** → persists to `localStorage` key `whinfell_transmission_control_v1`.

**Deep Dive page** reads this state first, then `latest.json`, then fixture.

## Step 3.6 — Perplexity reminder to Clark

```text
Hydration imported: YES / NO
Tracer: ACCEPTED / DISMISSED / PENDING
Whinfell Score: ___
Regime Tag: ___
Freshness: ___
Ready for Prompt B (sizing): YES / NO
```

---

# PHASE 4 — Research layer (Perplexity Prompts A–E)

**Separate from CSV collect.** Use **after** Phase 3 when desk needs narrative or sizing.

**Paste from:** `Comet_Browser_Operations_Blueprint.md` §6 Saved Prompts Utility Block

| Prompt | Title | When | Perplexity output |
|--------|-------|------|-------------------|
| **A** | Transmission Read & Regime Classification | Shift start, regime change | Regime narrative + **WTM EXPORT v2.1** block |
| **B** | Posture & Gross-Risk Recommendation | Sizing decisions | Gross % + posture ladder step |
| **C** | Trade Evaluation & Ranking | Candidate trade list | Ranked trades vs transmission map |
| **D** | Income Projection | Session/week outlook | P&L outlook from book |
| **E** | Divergence & Risk Compression | Tape vs WTM mismatch | Divergence flags |

### Prompt A template (minimum)

```text
Classify current regime from Whinfell Score, transmission state, and key observation.
End with WTM EXPORT v2.1 block including:
  Whinfell Score, Transmission State, Regime Tag, Key Observation,
  SQ3 Score, Snapshot ID, Data As Of, Freshness Status.
```

### WTM EXPORT fallback (CSV path down)

If `latest.json` stale or missing, Perplexity may produce **WTM EXPORT v2.1** text from Research Import path in TC — **Clark validates** before acting.

Spec: `whinfell_pipeline/WTM_EXPORT_v2.1_SPEC.md`

### Grok operator layer (optional)

After Save State, export **Grok payload** from TC.  
Wrapper rules: `Whinfell_Grok_Operator_Prompt.txt` (WHY bullets, gate language).

**Perplexity vs Grok:**

| Tool | Role |
|------|------|
| Perplexity A–E | External research + structured export blocks |
| Grok | Internal console state narration + WHY engine |

---

# PHASE 5 — Deep dive & ladder review

**Owner:** Junior analyst + Clark  
**Perplexity role:** Optional — Prompt E if tape diverges from ladder

## Step 5.1 — Open Deep Dive

```bash
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/whinfell-transmission-ladder-deep-dive.html
```

## Step 5.2 — Reconcile marks to data you exported

| Ladder stage | Verify against export |
|--------------|----------------------|
| Liquidity & Rates | Koyfin rates / T10Y2Y 20D direction |
| Credit Confirmation | WTM-Credit-Confirmation export / HYG-LQD 5D |
| Equity Breadth | WTM-Equities-Breadth export / IWM-SPY |
| High-Beta / BTC | Koyfin spot series + Barchart intraday |
| Basis & Term Structure | Barchart spreads + intraday curve |

If marks wrong → return to TC tracer → edit → Save State → refresh Deep Dive.

## Step 5.3 — China open / event checklist

```text
□ Weakest link in summary = failure panel rank #1
□ Math section shows 5 full stage cards (not collapsed)
□ BTC/ETH posture matches gate band
□ Prompt B run if sizing question open
```

---

# 10. Alternate & fallback paths

| Situation | Path | Perplexity role |
|-----------|------|-----------------|
| Fast morning | `run_batch_collect.py run` | Full collect prompt |
| Legacy Downloads | `run_csv_download.py daily` | Move files to Downloads; report paths |
| No browser | `fetch-api` + `run` | None (Clark) |
| Partial exports | `status` → re-export missing | Re-run failed steps only |
| Analytics archive (slow) | `run_batch_collect.py plan --mode per_ticker` | **Only on Clark request** |
| CSV chain broken | Prompt A + WTM EXPORT v2.1 | Research handoff |
| China qualitative | CHINA POLICY EXPORT v1.0 | Integration point 4 |

---

# 11. Troubleshooting

| Symptom | Likely cause | Fix | Perplexity action |
|---------|--------------|-----|-------------------|
| `ready=False` | Missing rates / intraday / daily | Re-export steps 1, 5, 6 | Report which missing |
| Files in `~/Downloads` | Wrong folder | `mv *.csv ~/Downloads/whinfell_drop/` | Move + re-run |
| `warn no rule for: foo.csv` | Unknown raw name | See playbook Appendix A | Report filename to Clark |
| All quarantined | Pre-2.2e headers | Check 2.2e transform logs | Report quarantine path |
| Duplicate `(1).csv` | Double export | Delete duplicate | Keep one file |
| Wrong Koyfin export | Cross-section snapshot not time series | Use Date-column export | Re-export step 2/3 |
| ER1 confusion | Ether vs Russell | ER1 = **Ether** on CME | Do not substitute QR1 |
| Stale freshness chip | Old `latest.json` | Re-run full chain + re-import | Report `as_of` timestamp |
| Tracer suggestions wrong | Bad marks in source data | Dismiss + manual override | Do not Accept for Clark |
| Deep Dive ≠ TC weakest | Saved state vs hydration mismatch | Save State after Accept | Note both scores in report |

---

# 12. Perplexity prompt index

| When | Paste this file | Mode |
|------|-----------------|------|
| **Daily morning collect (default)** | `08_Deliverables/Perplexity_Full_Collection_Prompt.txt` | Collect robot |
| **After 2.2e ship / agent refresh** | `08_Deliverables/Perplexity_2.2e_Update_Prompt.txt` | Collect robot |
| **Short collect reminder** | `whinfell_pipeline/examples/AGENT_COLLECTION_PROMPT.txt` | Collect robot |
| **Human-readable ops** | `08_Deliverables/Perplexity_Comet_Collection_Instructions.md` | Reference |
| **Vendor CSV formats** | `08_Deliverables/Perplexity_Barchart_Koyfin_Playbook.md` | Reference when quarantined |
| **Shift regime read** | Blueprint §6 Prompt A | Research |
| **Sizing** | Blueprint §6 Prompt B | Research |
| **Trade list** | Blueprint §6 Prompt C | Research |
| **P&L outlook** | Blueprint §6 Prompt D | Research |
| **Tape divergence** | Blueprint §6 Prompt E | Research |
| **Grok desk narrative** | `Whinfell_Grok_Operator_Prompt.txt` | After Clark Save State |
| **China qualitative** | `china_policy_track/examples/sample_perplexity_export.txt` | Manual China supplement |

---

# 13. Daily timeline (China open example)

| Time (ET) | Actor | Action |
|-----------|-------|--------|
| T−60m | Perplexity | Phase 1: 8 exports → `run_batch_collect.py run` → report |
| T−45m | Clark | Phase 3: Import → review tracer → Accept/Dismiss → Save |
| T−30m | Junior | Phase 5: Deep Dive + mark reconciliation |
| T−20m | Perplexity | Prompt A (regime) + B (sizing) if Clark requests |
| T−10m | Clark | Gate check · trade menu · go/no-go |
| T+0 | Desk | Execute within posture; no Perplexity trading |

---

# 14. File reference (complete)

| File | Role |
|------|------|
| `08_Deliverables/Whinfell_Data_Update_Guide.md` | **This guide** |
| `08_Deliverables/Perplexity_Full_Collection_Prompt.txt` | Primary Perplexity collect paste |
| `08_Deliverables/Perplexity_2.2e_Update_Prompt.txt` | 2.2e transform context |
| `08_Deliverables/Perplexity_Comet_Collection_Instructions.md` | Agent instructions + Comet supervised |
| `08_Deliverables/Perplexity_Barchart_Koyfin_Playbook.md` | Vendor CSV taxonomy |
| `08_Deliverables/Fast_CSV_Collect_Guide.md` | Technical fast collect |
| `whinfell_pipeline/examples/comet_collection_plan.json` | Machine checklist |
| `whinfell_pipeline/desk_urls.yaml` | Wired URLs |
| `whinfell_pipeline/collection_manifest.yaml` | Full manifest + per-ticker mode |
| `run_batch_collect.py` | Fast batch entry point |
| `run_csv_download.py` | Legacy daily chain |
| `data/hydration/latest.json` | TC import target |
| `08_Deliverables/Whinfell_Transmission_Control.html` | Operator console |
| `08_Deliverables/whinfell-transmission-ladder-deep-dive.html` | Ladder + math review |

---

*End of guide. Perplexity: start at Phase 1 with Full Collection Prompt. Clark: start at Phase 3 after pipeline status is ready.*