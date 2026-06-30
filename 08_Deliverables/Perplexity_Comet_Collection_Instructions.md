# Perplexity & Comet — CSV Collection Instructions

**Authority:** Clark · BUILD Cousins desk  
**Audience:** Perplexity, Comet, and any browser-collection agent  
**Tone:** Follow exactly. Do not improvise.  
**Updated:** 2026-06-28

---

## Read this first (peasant-proof summary)

You are **not** a data scientist on this task. You are a **CSV export robot**.

| DO | DON'T |
|----|-------|
| Open **8 saved screens** | Loop 13 tickers one-by-one |
| Click **Export / Download CSV** | Read, parse, or summarize CSV contents |
| Save to **`~/Downloads/whinfell_drop`** | Save to `~/Downloads` root |
| Run **`python3 run_batch_collect.py run`** | Rename files by hand |
| Report file names + counts | Guess at Whinfell scores or regime |

**8 exports ≈ 3 minutes. 13 ticker loops ≈ 30 minutes. Pick the fast path.**

---

## Your mission (daily)

1. Export **8 bulk CSVs** from saved Koyfin/Barchart views (table below).
2. Save every file to **`~/Downloads/whinfell_drop`**.
3. Run the Whinfell batch tool (one terminal command).
4. Tell Clark: files staged, quarantined, hydration path.

Clark handles Transmission Control import. You do **not** trade.

---

## Step 0 — Load the machine plan

```bash
cd ~/Desktop/Whinfell_BUILD_Cousins
python3 run_batch_collect.py plan
```

Frozen copy (paste into your context):

`whinfell_pipeline/examples/comet_collection_plan.json`

Wired URLs live in:

`whinfell_pipeline/desk_urls.yaml`

---

## Step 1 — The 8 exports (ONLY these for daily)

### Koyfin (4 exports)

| # | Saved view name | Wired URL / navigation | Save as (tool renames if needed) |
|---|-----------------|------------------------|----------------------------------|
| 1 | **WTM-Rates-Credit** | [app.koyfin.com](https://app.koyfin.com/) → My Dashboards → WTM-Rates-Credit | `rates_YYYYMMDD_HHMM.csv` |
| 2 | **WTM-Equities-Breadth** | My Dashboards → WTM-Equities-Breadth (canonical) | `equities_YYYYMMDD_HHMM.csv` |
| 3 | **WTM-Credit-Confirmation** | My Dashboards → WTM-Credit-Confirmation (canonical) | `credit_YYYYMMDD_HHMM.csv` |
| 4 | **WTM-China-Policy** | My Dashboards → WTM-China-Policy | `china_policy_YYYYMMDD_HHMM.csv` |

**Koyfin export clicks:** Open view → `⋮` menu → **Export** → **CSV** → save to `whinfell_drop`.

**Assist links** (verify you're on the right desk):

- Rates: [USGG2Y10Y](https://app.koyfin.com/macro/USGG2Y10Y) · [DGS10](https://app.koyfin.com/macro/DGS10)
- Equities: [IWM](https://app.koyfin.com/etf/IWM.US) · [SPY](https://app.koyfin.com/etf/SPY.US)
- Credit: [HYG](https://app.koyfin.com/etf/HYG.US) · [LQD](https://app.koyfin.com/etf/LQD.US)
- Spot series (optional): [BTCUSD](https://app.koyfin.com/crypto/BTCUSD) · [IBIT](https://app.koyfin.com/etf/IBIT.US)

> **Koyfin share links:** Clark can paste dashboard Share URLs into `desk_urls.yaml` to skip navigation. Until then, use dashboard names above.

### Barchart (3 required + 1 optional)

| # | Saved screen | Wired URL | Save as |
|---|--------------|-----------|---------|
| 5 | **WTM-Futures-Intraday** | [Major Commodities](https://www.barchart.com/futures/major-commodities) or list **dailymonitor0610** | `futures_intraday_YYYYMMDD_HHMM.csv` |
| 6 | **WTM-Futures-Daily** | [BTM26 Historical Download](https://www.barchart.com/futures/quotes/BTM26/historical-download) | `futures_daily_YYYYMMDD_HHMM.csv` |
| 7 | **WTM-BTC-Basis** (optional) | [BTM26 Spreads](https://www.barchart.com/futures/quotes/BTM26/spreads) | `btc_basis_YYYYMMDD.csv` |
| 8 | **WTM-Options-Greeks** (optional) | [BTN26 Options](https://www.barchart.com/futures/quotes/BTN26/options) | `options_YYYYMMDD_HHMM.csv` |

**Barchart export clicks:** Open screen → **Download CSV** (top-right of table).

**Assist links:**

- [My Lists](https://www.barchart.com/my/lists) (dailymonitor0610)
- [BTM26 quote](https://www.barchart.com/futures/quotes/BTM26)
- [ESM26 historical](https://www.barchart.com/futures/quotes/ESM26/historical-download)
- [Crypto futures hub](https://www.barchart.com/futures/crypto)

---

## Step 2 — Open all URLs at once (optional)

```bash
python3 run_batch_collect.py open
```

Opens wired Barchart URLs + Koyfin home. Export each tab. **Do not** open 13 separate ticker pages.

---

## Step 3 — Run the tool (mandatory)

```bash
mkdir -p ~/Downloads/whinfell_drop
cd ~/Desktop/Whinfell_BUILD_Cousins
python3 run_batch_collect.py run --window today
```

This **automatically**:

- Renames `koyfin_2026-06-28.csv` → `rates_*`
- Renames `btm26_daily-nearby_historical-*` → `futures_daily_*`
- Renames `bitcoin-futures-prices-intraday-*` → `futures_intraday_*`
- Stages → collects → builds `data/hydration/latest.json`

Check status:

```bash
python3 run_batch_collect.py status
```

---

## Step 4 — Report to Clark (copy this template)

```
WHINFELL COLLECT REPORT
Date: YYYY-MM-DD HH:MM
Drop dir: ~/Downloads/whinfell_drop

Exports completed:
- [ ] koyfin_rates
- [ ] koyfin_equities
- [ ] koyfin_credit
- [ ] koyfin_china (if applicable)
- [ ] barchart_futures_intraday
- [ ] barchart_futures_daily
- [ ] barchart_btc_basis (optional)

Pipeline:
- files_staged: ___
- files_quarantined: ___
- hydration_bundle: data/hydration/latest.json

Errors (if any):
- ...

Next for Clark: Transmission Control → Import Latest Hydration Bundle
```

---

## Paste prompt — Perplexity

**Full prompt (recommended — includes problem statement):**  
`08_Deliverables/Perplexity_Full_Collection_Prompt.txt`

**Short version:**

```
WHINFELL FAST COLLECT MODE

You are a CSV export robot. Not an analyst.

RULES:
1. Read whinfell_pipeline/examples/comet_collection_plan.json
2. Export ONLY the 8 batch steps — never loop BT1→ER1→…→VI*1 individually
3. Save ALL CSVs to ~/Downloads/whinfell_drop
4. Do NOT parse or summarize CSV contents
5. Run: cd ~/Desktop/Whinfell_BUILD_Cousins && python3 run_batch_collect.py run --window today
6. Report staged/quarantined counts + hydration path using the report template

URLs: whinfell_pipeline/desk_urls.yaml
Playbook: 08_Deliverables/Perplexity_Barchart_Koyfin_Playbook.md
```

---

## Paste prompt — Comet (supervised)

```
WHINFELL DESK COLLECTOR — SUPERVISED FAST MODE

Before any terminal command, ask Clark: "Ready to run batch collect?"

SEQUENCE:
1. python3 run_batch_collect.py plan  (read steps)
2. python3 run_batch_collect.py open  (optional — opens wired URLs)
3. Export each step to ~/Downloads/whinfell_drop — export only, no parsing
4. On Clark approval: python3 run_batch_collect.py run --window today
5. Report files_staged, files_quarantined, hydration path

FORBIDDEN:
- Per-ticker Barchart loops (13 tickers)
- Parsing CSV in browser
- Skipping whinfell_drop folder
- Auto-trading or risk changes

If quarantined: show errors from staged_raw/quarantine/ and stage_manifest JSON.
```

---

## When Clark asks for analytics archive (rare)

Only then loop per-ticker historical URLs from `collection_manifest.yaml` → `tickers:` section.

```bash
python3 run_batch_collect.py plan --mode per_ticker
```

This is **slow** and **not** the daily path.

---

## API fast path (Clark only)

If `BARCHART_API_KEY` is set:

```bash
export BARCHART_API_KEY="..."
python3 run_batch_collect.py fetch-api
python3 run_batch_collect.py run
```

No browser. ~30 seconds for all historical series.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Files in wrong folder | Move to `~/Downloads/whinfell_drop` |
| `warn no rule for: foo.csv` | Raw name unknown — check playbook §Appendix A or tell Clark |
| All files quarantined | Expected until 2.2e transform — collection still valid for analytics |
| `ready=False` on status | Missing rates, futures_intraday, or futures_daily |
| Duplicate ` (1).csv` | Delete duplicate; keep one copy |
| Opened wrong Koyfin export | Use Date-column time series — not cross-section watchlist snapshots |

---

## File map

| File | Purpose |
|------|---------|
| `08_Deliverables/Perplexity_Comet_Collection_Instructions.md` | **This doc** — start here |
| `08_Deliverables/Fast_CSV_Collect_Guide.md` | Short technical guide |
| `08_Deliverables/Perplexity_Barchart_Koyfin_Playbook.md` | Vendor CSV formats |
| `whinfell_pipeline/desk_urls.yaml` | Wired URLs + navigation |
| `whinfell_pipeline/examples/comet_collection_plan.json` | Agent JSON checklist |
| `whinfell_pipeline/examples/AGENT_COLLECTION_PROMPT.txt` | One-block paste prompt |
| `scripts/whinfell_morning_collect.sh` | Clark one-command morning |

---

## Clark one-liner

```bash
scripts/whinfell_morning_collect.sh
```

---

*End of instructions. Follow the plan. Do not freestyle.*