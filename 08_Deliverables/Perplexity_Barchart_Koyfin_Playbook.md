# Perplexity Playbook: Barchart & Koyfin CSV Collection

**Audience:** Perplexity (vendor CSV collection)  
**Desk lead:** Clark  
**Last updated:** 2026-06-28  
**Repo:** `Whinfell_BUILD_Cousins`

---

## Quick navigation

| Section | Jump to |
|---------|---------|
| Start here — the one rule | [§1 Two CSV shapes](#1-the-one-rule-two-different-csv-shapes) |
| Barchart file types (5) | [§2 Barchart taxonomy](#2-barchart-five-file-types) |
| Ticker shortcuts → filenames | [§3 Contract codes](#3-barchart-shortcuts-vs-download-filenames) |
| How to parse Barchart safely | [§4 Parsing rules](#4-barchart-parsing-rules) |
| Koyfin — use vs avoid | [§5 Koyfin exports](#5-koyfin-two-export-families) |
| Spot / basis joins | [§6 Spot map](#6-spot-and-basis-join-rules) |
| Whinfell staged format | [§7 WTM observation rows](#7-whinfell-staged-format-wtm-observation-rows) |
| Daily operator steps | [§8 Checklist](#8-daily-operator-checklist) |
| What fails today & why | [§9 Known gap](#9-known-gap-22e) |
| Reference code on Clark's Mac | [§10 Reference projects](#10-reference-code-on-clarks-machine) |
| **Agent instructions (Perplexity/Comet)** | [`Perplexity_Comet_Collection_Instructions.md`](Perplexity_Comet_Collection_Instructions.md) |
| **Fast collect (8 exports, not 13 loops)** | [`Fast_CSV_Collect_Guide.md`](Fast_CSV_Collect_Guide.md) |
| **Wired desk URLs** | `whinfell_pipeline/desk_urls.yaml` |

---

## 1. The one rule: two different CSV shapes

**Do not mix these.** Most collection mistakes come from treating vendor exports as pipeline-ready staged files.

| Path | CSV shape | Consumer |
|------|-----------|----------|
| **Analytics** (WhinVis / `data_parser`) | Raw vendor export — many rows, vendor column names (`Symbol`, `Latest`, `%Change`, …) | `prepare_data.py` → Parquet → dashboards |
| **Whinfell ingest** (`staged_csv.py`) | **Single WTM observation row** — Whinfell headers (`timestamp`, `basis_spread`, `whinfell_score`, …) | `run_csv_download.py stage` → observation parquet |

**Filename rename alone is not enough for Whinfell ingest.**  
`scripts/normalize_whinfell_drop.sh` fixes Layer 1 (filename). Layer 2 (headers) still fails on raw Barchart/Koyfin until raw→WTM transform ships (BUILD TODO **2.2e**).

Gold-standard staged examples:

```
whinfell_pipeline/examples/staged/
├── barchart_futures_intraday_20260627_1400.csv
├── koyfin_rates_20260627_1400.csv
└── china_policy_20260627_1400.csv
```

---

## 2. Barchart: five file types

Barchart does **not** use one universal layout. Classify by **filename**, then apply the matching parser rules.

### Type 1 — Historical (daily nearby)

| Field | Value |
|-------|-------|
| **Filename** | `{contract}_daily-nearby_historical-data-MM-DD-YYYY.csv` |
| **Example** | `btm26_daily-nearby_historical-data-06-28-2026.csv` |
| **Headers** | `Symbol, Time, Open, High, Low, Latest, Change, %Change, Volume, Open Int` |
| **Time column** | Calendar date (not intraday clock) |
| **Use for** | Basis history, realized vol, backtests |
| **Whinfell rename** | `futures_daily_{YYYYMMDD}_{HHMM}.csv` |

### Type 2 — Prices (intraday term structure)

| Field | Value |
|-------|-------|
| **Filename** | `{asset-slug}-prices-intraday-MM-DD-YYYY.csv` |
| **Example** | `bitcoin-futures-prices-intraday-06-28-2026.csv` |
| **Headers** | `Contract, Latest, Change, Open, High, Low, Previous, Volume, Open Int, Time` |
| **Key differences** | `Contract` not `Symbol`; `Time` is intraday; no `%Change`; has `Previous` |
| **Use for** | Live curve, near/far month selection |
| **Whinfell rename** | `futures_intraday_{YYYYMMDD}_{HHMM}.csv` |

### Type 3 — Spreads

| Field | Value |
|-------|-------|
| **Filename** | `futures-spreads-{contract}*.csv` |
| **Example** | `futures-spreads-btn26-06-28-2026.csv` |
| **Headers** | `Leg1, Leg2, Leg3, Leg4, Type, Latest, Change, Open, High, Low, Previous, Volume, Time` |
| **Use for** | Calendar spreads, roll structure |
| **Whinfell rename** | `btc_basis_{YYYYMMDD}.csv` (BTC spreads) or retain for analytics |

### Type 4 — Options (side-by-side)

| Field | Value |
|-------|-------|
| **Filename** | `{contract}-options-monthly-options-exp-*-side-by-side-intraday-*.csv` |
| **Example** | `btn26-options-monthly-options-exp-06-28-2026-side-by-side-intraday-*.csv` |
| **Trap** | Duplicate Call/Put column names — pandas adds `.1` suffixes |
| **Fix** | Split at midpoint, stack Call half + Put half vertically before parsing |
| **Whinfell rename** | `options_{YYYYMMDD}_{HHMM}.csv` |

### Type 5 — Vol/Greeks (side-by-side)

| Field | Value |
|-------|-------|
| **Filename** | `{contract}-volatility-greeks-exp-*.csv` |
| **Example** | `btn26-volatility-greeks-exp-06-28-2026.csv` |
| **Trap** | Same side-by-side reshape as options |
| **Whinfell rename** | `greeks_{YYYYMMDD}_{HHMM}.csv` |

---

## 3. Barchart shortcuts vs download filenames

When you type `XX1` in Barchart, the **downloaded filename** uses the **contract root**, not the shortcut.

| Barchart shortcut | Asset | Contract prefix in filename | Example file root |
|-------------------|-------|------------------------------|-------------------|
| BT1 | Bitcoin (CME) | `btm` | `btm26_*` |
| ER1 | **Ether** (CME) — *not Russell* | `erm` | `erm26_*` |
| SA1 | Solana (CME) | `sam` | `sam26_*` |
| SJ1 | XRP (CME) | `sjm` | `sjm26_*` |
| ES1 | S&P 500 E-mini | `esm` | `esm26_*` |
| GC1 | Gold | `gcm` | `gcm26_*` |
| CL1 | WTI Crude | `cl` | `cln26_*` |
| ZN1 | 10-Year T-Note | `zn` | `zn26_*` |
| SQ1 | 3-Month SOFR | `sq` | `sq26_*` |
| QR1 | **Russell 2000** E-mini | `qrm` | `qrm26_*` |
| DX1 | US Dollar Index | `dxu` | `dxu26_*` |
| OY1 | High Yield Corp Bond | `oyu` | `oyu26_*` |
| VI*1 | VIX futures | `vin` | `vin26_*` |

**Approved collection queue (13 tickers):**

```
BT1 → ER1 → SA1 → SJ1 → GC1 → ES1 → ZN1 → CL1 → SQ1 → OY1 → QR1 → DX1 → VI*1
```

**Also collect separately:** **IBIT** (Bitcoin ETF) — from Koyfin, not Barchart futures.

**Optional:** NQ1 (Nasdaq E-mini) if desk wants broader equity coverage.

**Month codes can differ across file types** — e.g. historical `cln26` vs options `clq26`. That is normal; do not assume one contract month across all five file types.

---

## 4. Barchart parsing rules

Battle-tested in WhinVis (`utils/loaders.py`) and `data_parser` (`src/parsers/`).

### Read & clean

1. **Strip footer** — last line is `"Downloaded from Barchart…"`.
   - Primary: `pd.read_csv(path, engine="python", skipfooter=1, on_bad_lines="skip")`
   - Fallback: drop lines containing `"Downloaded from Barchart"`
2. **Parse footer timestamp** — regex `as of MM-DD-YYYY` → `download_ts`; fallback to file mtime.
3. **Normalize headers** — strip quotes from `"Open Int"`, trim whitespace.

### Coerce types

4. **`%Change`** — strip `%` and `+`, then numeric.
5. **Map `Latest` → `Close`** — canonical name in all downstream Parquet.
6. **`Time`** — `pd.to_datetime(..., errors="coerce")`; drop rows with null Time.

### Validate & metadata

7. **Minimum columns:** `Symbol` (or `Contract`), `Time`, `Latest`/`Close`.
8. **Attach metadata:** `source_file`, `download_ts` on every row.
9. **Dedupe:** `(Symbol, Time)` — keep last.

### Skip noise files

- `*.crdownload`
- `Unconfirmed*`
- Duplicate browser copies: `filename (1).csv`
- Do not feed `koyfin_*` files into Barchart parser scan paths

### Options / Vol-Greeks reshape (Types 4 & 5)

Barchart exports Call and Put chains **side by side** with repeated header names. Before parsing:

1. Read raw CSV (no column rename yet).
2. Split columns at midpoint into Call half and Put half.
3. Stack vertically; tag `OptionSide` = Call / Put.
4. Then apply column aliases (`Latest` → `Close`, etc.).

Reference: `data_parser/src/columns.py` → `reshape_side_by_side()`.

---

## 5. Koyfin: two export families

### USE — historical time-series export

| Field | Value |
|-------|-------|
| **Filename** | `koyfin_2026-06-28.csv` or `koyfin_YYYY-MM-DD.csv` |
| **Required** | `Date` column + `{TICKER} Close` columns |
| **Examples** | `BTCUSD Close`, `ETHUSD Close`, `SPY Close`, `US10Y Close`, `IBIT Close` |
| **Use for** | Spot joins, basis, global macro, ETF prices |
| **Whinfell rename** | `rates_{YYYYMMDD}_{HHMM}.csv` |

### DO NOT USE for time-series pipeline

| Filename pattern | Why |
|------------------|-----|
| Legacy cross-section snapshots | Not time-series — use WTM-* saved views instead |
| Legacy credit snapshot exports | Normalize only — export WTM-Credit-Confirmation |
| `Whinfell*` | Desk snapshot, not time series |

These may still help desk glance or observation **text**, but WhinVis explicitly skips them when loading daily spot.

**Whinfell rename (if desk still drops them):**

- Legacy equities vendor files → `equities_{YYYYMMDD}_{HHMM}.csv` (see `normalize_rules` in data_dictionary.yaml)
- Legacy credit vendor files → `credit_{YYYYMMDD}_{HHMM}.csv` (see `normalize_rules` in data_dictionary.yaml)

### WhinSig-only — Flow (D) exports (separate track)

- Columns like `IBIT Flow (D)`, `SPY Flow (D)`
- Handled by `whinsig/src/flows_merger.py`
- **Not** the Whinfell basis pipeline — ignore unless doing flow/AUM work

---

## 6. Spot and basis join rules

When computing futures vs cash basis (WhinVis / `data_parser` analytics):

| Ticker | Koyfin spot column | Basis formula |
|--------|-------------------|---------------|
| BT | `BTCUSD Close` | `(Latest - spot) / spot × 100` |
| ER | `ETHUSD Close` | same |
| SA | `SOLUSD Close` | same |
| SJ | `XRPUSD Close` | same |
| GC | `GC1 Close` | same |
| CL | `CL1 Close` | same |
| ES | `SPY Close` | proxy — ES notional ~10× SPY |
| DX | `UUP Close` | USD proxy via ETF |
| QR | `IWM Adj. Close` | Russell proxy |
| OY | `HYG Close` | HY credit proxy |
| **ZN** | `US10Y Close` | **Yield-based** — do **not** use simple price spread |
| SQ | `SOFR Close` | Rate-based; basis is indicative only |

**ZN special case:** 10-Year T-Note futures have no clean cash price analogue. Use implied-yield basis engine (`data_parser/src/spot.py` → `zn_implied_yield_pct`). Never compute `(Latest - US10Y) / US10Y` as a price basis.

---

## 7. Whinfell staged format (WTM observation rows)

After rename, Whinfell `staged_csv.py` expects **Whinfell headers**, not vendor headers. It reads the **last row** as the observation payload.

### Barchart → execution observation

**Path:** `staged_raw/source=barchart/dataset={futures_intraday|futures_daily|options|greeks}/`

```csv
observation_id,timestamp,near_month,far_month,basis_spread,ref_low,ref_mid,ref_high
exec-2026-06-28-barchart-01,2026-06-28T14:05:00,Jul,Sep,1.25,0.8,1.1,1.4
```

**Required headers:** `timestamp` + (`near_month` or `basis_spread`)

### Koyfin → global observation

**Path:** `staged_raw/source=koyfin/dataset={rates|credit|equities}/`

```csv
observation_id,timestamp,whinfell_score,transmission_state,regime_tag,key_observation
global-2026-06-28-koyfin-01,2026-06-28T14:00:00,58,stressed,Fragile Risk-On,Credit mixed; breadth narrowing.
```

**Required headers:** `timestamp` + (`whinfell_score`, `regime_tag`, or `key_observation`)

### Filename contract (Layer 1)

```
{dataset}_{YYYYMMDD}_{HHMM}.csv
```

Examples: `futures_daily_20260628_1030.csv`, `rates_20260628_1400.csv`

Alternate (product flavor):

```
{product}_{flavor}_{YYYYMMDD}.csv
```

Example: `btc_basis_20260628.csv`

---

## 8. Daily operator checklist

### Drop folder

```
~/Downloads/whinfell_drop
```

### Step 1 — Collect (Barchart)

Per ticker in the approved queue, download at minimum:

- [ ] Historical (`*_daily-nearby_historical-data-*`)
- [ ] Prices intraday (`*-prices-intraday-*`)

Optional when available:

- [ ] Spreads (`futures-spreads-*`)
- [ ] Options side-by-side (`*-options-*-side-by-side-intraday-*`)
- [ ] Vol/Greeks (`*-volatility-greeks-*`)

### Step 2 — Collect (Koyfin)

- [ ] Export `koyfin_YYYY-MM-DD.csv` with `Date` + Close columns
- [ ] Include `IBIT Close` (and other approved ETF closes if desk requests)
- [ ] Do **not** substitute non-WTM watchlist snapshots for time-series work

### Step 3 — Rename filenames

```bash
cd ~/Desktop/Whinfell_BUILD_Cousins
scripts/normalize_whinfell_drop.sh ~/Downloads/whinfell_drop
```

### Step 4 — Stage (expect header quarantine until 2.2e)

```bash
python3 run_csv_download.py stage --downloads ~/Downloads/whinfell_drop --operator desk --window today
```

### Step 5 — Until 2.2e ships

For live Whinfell ingest, use one of:

- Transmission Control **WTM EXPORT**
- Comet collector shaped exports
- Manually craft single-row CSVs matching `whinfell_pipeline/examples/staged/`

Keep raw vendor CSVs for WhinVis-style analytics regardless.

### Step 6 — Clark re-hydrates Transmission Control

After pipeline produces hydration bundle:

- `data/hydration/latest.json`
- Or copies on Desktop/Downloads: `Whinfell_Hydration_latest.json`

---

## 9. Known gap (2.2e)

| Layer | Status | What happens |
|-------|--------|--------------|
| **Layer 1 — Filename** | ✅ Fixed | `normalize_whinfell_drop.sh` maps vendor names → staged contract |
| **Layer 2 — Headers** | ❌ Open | Raw Barchart/Koyfin fail `staged_csv.py` validation |
| **Fix needed** | BUILD TODO **2.2e** | `raw_csv_transform.py` — port `data_parser` logic OR emit WTM observation rows from latest vendor snapshot |

**Symptom:** Files quarantine after rename with errors like `missing required headers: timestamp, near_month or basis_spread`.

**This is expected** until 2.2e ships. Collection is still valuable — raw files feed analytics; shaped observations feed ingest.

---

## 10. Reference code on Clark's machine

| Project | Path | What to read |
|---------|------|--------------|
| **data_parser** | `~/Desktop/dashboards/data_parser/` | Canonical 5-type parser |
| | `config/column_map.yaml` | Header aliases per file type |
| | `config/tickers.yaml` | Filename globs per ticker |
| | `config/spot_sources.yaml` | Spot column map |
| | `src/parsers/historical.py` | Footer strip, coercion |
| | `src/columns.py` | Side-by-side options reshape |
| **WhinVis** | `~/Desktop/dashboards/whinvis/` | Basis dashboard consumer |
| | `utils/loaders.py` | `parse_barchart_csv`, Koyfin daily finder |
| | `prepare_data.py` | Raw → Parquet pipeline |
| **WhinSig** | `~/Desktop/dashboards/whinsig/` | Koyfin Flow (D) only |
| | `src/flows_merger.py` | Flow column detection |
| **Whinfell** | `~/Desktop/Whinfell_BUILD_Cousins/` | Ingest contract |
| | `whinfell_pipeline/staged_csv.py` | Header validation rules |
| | `scripts/normalize_whinfell_drop.sh` | Filename rename rules |
| | `whinfell_pipeline/examples/staged/` | Gold-standard WTM rows |

---

## Appendix A — `normalize_whinfell_drop.sh` rename map

| Raw filename pattern | Renamed to |
|---------------------|------------|
| `btm26_daily-nearby_historical-data-*` | `futures_daily_{YYYYMMDD}_{HHMM}.csv` |
| `*-prices-intraday-*` (via script rules) | `futures_intraday_{YYYYMMDD}_{HHMM}.csv` |
| `btn26-options-monthly-options-exp-*side-by-side-intraday*` | `options_{YYYYMMDD}_{HHMM}.csv` |
| `btn26-volatility-greeks-exp-*` | `greeks_{YYYYMMDD}_{HHMM}.csv` |
| `futures-spreads-btn26-*` | `btc_basis_{YYYYMMDD}.csv` |
| `koyfin_YYYY-MM-DD.csv` | `rates_{YYYYMMDD}_{HHMM}.csv` |
| `equities_vendor_snapshot` (normalize_rules) | `equities_{YYYYMMDD}_{HHMM}.csv` |
| `credit_vendor_snapshot` (normalize_rules) | `credit_{YYYYMMDD}_{HHMM}.csv` |

Files already matching `futures_intraday_*`, `rates_*`, etc. are skipped.

---

## Appendix B — Common mistakes

| Mistake | Fix |
|---------|-----|
| Treating `ER1` as Russell | ER1 = Ether (`erm*` files). Russell = `QR1` (`qrm*`). |
| Using Koyfin Simplify for history | Export `koyfin_YYYY-MM-DD.csv` with `Date` column instead. |
| Expecting ingest after rename only | Need WTM observation row (2.2e) or manual/Comet shaped export. |
| One parser for all Barchart files | Classify by filename into 5 types first. |
| Parsing options without reshape | Side-by-side Call/Put must be split and stacked. |
| ZN basis as price spread | Use yield-based logic only. |
| Forgetting IBIT | ETF — Koyfin `IBIT Close`, not Barchart futures. |
| Keeping `*.crdownload` or `(1).csv` dupes | Delete or skip before drop. |

---

## Appendix C — Who to ask

| Question | Ask |
|----------|-----|
| Ticker queue / priorities | Clark |
| WTM observation text / scores | Clark + Transmission Control |
| Parser logic / 2.2e transform | Build track (Whinfell pipeline) |
| Raw file analytics / basis charts | WhinVis (`data_parser`) |

---

*End of playbook.*