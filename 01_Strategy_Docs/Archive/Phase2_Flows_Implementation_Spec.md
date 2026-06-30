# Phase 2 — Funds Flows Implementation Specification

**Version:** 1.1 (ready for desk lock)  
**Date:** June 29, 2026  
**Authors:** BUILD Cousins (Blueprint + Bridge + Clarity + Integration Dynamo)  
**Status:** **Authoritative companion spec** for flows architecture — blocks PR-1 and PR-3 until §8 sign-off  
**Document role:** Standalone implementation authority; [Phase2_Node_Cockpit_Data_Model.md](Phase2_Node_Cockpit_Data_Model.md) holds §9.1 pointer only (no field overload)  
**Prerequisites:** [Phase2_Funds_Flow_Sponsorship_Design.md](Phase2_Funds_Flow_Sponsorship_Design.md) v1.0, [Funds_Flow_Ingest_Arena_Debate.md](../08_Deliverables/Funds_Flow_Ingest_Arena_Debate.md) (Option D accepted)

**Companion docs:** [Phase2_Node_Cockpit_Data_Model.md](Phase2_Node_Cockpit_Data_Model.md) · [Master_Data_Dictionary_v1.0.md](Master_Data_Dictionary_v1.0.md)

---

## Confirmation of scope

This document specifies **implementation-level detail** for the flows module: canonical data shapes, parser contracts, node cockpit integration, degradation modes, ownership boundaries, and Master DD deltas. It is written so an engineer can implement PR-1 (registry) and PR-3 (ingest + builder) without inferring behavior from UI mockups alone.

**Locked ingest decision:** **Option D (Hybrid)** — primary `flows_{YYYYMMDD}_{HHMM}.csv` time-series; fallback credit cross-section for 1D only.

**Authority rule (unchanged):** Flows affect `confidence`, `directional.rationale`, `relative_value.rationale`, `interpretation.*`, and export narrative only. They **never** mutate `composite_score`, gate, or transmission state.

---

## Architecture overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│ INGEST (PR-3a / PR-3b)                                                  │
│  flows_*.csv ──► flows_parser.py ──► data/flows/v1/latest_flows.json   │
│  credit raw  ──► flows_fallback.py ──► (merged into sidecar, 1D only)  │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────────┐
│ BUILD (PR-2 extension)                                                  │
│  funds_flows.py: sidecar + basket registry ──► node_cockpit.funds_flows │
│  node_cockpits.py: apply confidence_delta, merge rationale snippets     │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────────┐
│ HYDRATION BUNDLE v1.2.0                                                 │
│  node_cockpits.{node_id}.funds_flows                                    │
│  flows_sidecar (optional top-level mirror for debugging)                │
└───────────────────────────────┬─────────────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────────────┐
│ UI (PR-4)                                                               │
│  FundsFlowSponsorshipCard(cockpit.funds_flows) — read-only              │
└─────────────────────────────────────────────────────────────────────────┘
```

**Module boundaries:**

| Module | File(s) | Owns |
|--------|---------|------|
| Registry | `data_dictionary.yaml`, `data_dictionary.py` | Baskets, thresholds, column patterns, file naming |
| Parser (primary) | `whinfell_pipeline/flows_parser.py` | `flows_*.csv` → sidecar daily series |
| Parser (fallback) | `whinfell_pipeline/flows_fallback.py` | Credit cross-section → 1D snapshots |
| Sidecar | `data/flows/v1/latest_flows.json` | Canonical flow store between ingest and hydrate |
| Builder | `whinfell_pipeline/funds_flows.py` | Sidecar → per-node `funds_flows` view model |
| Integration | `whinfell_pipeline/node_cockpits.py` | Attach block, apply confidence, rationale merge |
| Export | `whinfell_pipeline/export_contract.py` | WTM NODE COCKPIT flow lines |
| UI | `Whinfell_Transmission_Control.html` (or module) | `FundsFlowSponsorshipCard` render only |

---

## 1. Flows data model

### 1.1 Three-layer model

| Layer | Artifact | Lifetime | Purpose |
|-------|----------|----------|---------|
| **L0 Raw** | `flows_*.csv`, raw credit CSV | Per drop | Vendor columns; not stored in hydration |
| **L1 Sidecar** | `data/flows/v1/latest_flows.json` | Latest snapshot + history tail | Ticker-level daily series; ingest output |
| **L2 Node view** | `node_cockpit.funds_flows` | Per hydrate | Basket-filtered, verdict-computed, UI-ready |

Never render L1 in TC directly. UI consumes **L2 only**.

---

### 1.2 L1 — Sidecar `latest_flows.json`

**Path:** `data/flows/v1/latest_flows.json`  
**Written by:** `batch_collect.py` / `flows_parser.py` after successful `flows_*.csv` stage (PR-3a); partial merge from fallback (PR-3b).

```json
{
  "version": "1.0.0",
  "as_of": "2026-06-29",
  "source_file": "flows_20260629_1525.csv",
  "source_channel": "koyfin_wtm_flows",
  "ingest_mode": "timeseries_primary",
  "units": {
    "flow_usd": "millions_usd",
    "aum_usd": "millions_usd",
    "flow_pct_aum": "percent"
  },
  "history_sessions": 752,
  "tickers": {
    "HYG": {
      "ticker": "HYG",
      "asset_id": "hyg",
      "canonical_asset_resolved": true,
      "latest": {
        "date": "2026-06-29",
        "flow_usd_1d": -120.5,
        "aum_usd": 14505.42,
        "flow_pct_aum_1d": -0.83
      },
      "rolling": {
        "flow_usd_5d": -310.2,
        "flow_pct_aum_5d": -2.14,
        "sessions_in_5d": 5,
        "persistence_score_20d": 0.65
      },
      "series_tail": [
        {"date": "2026-06-25", "flow_usd_1d": -50.1, "aum_usd": 14480.0, "flow_pct_aum_1d": -0.35}
      ]
    }
  },
  "fallback_overlay": {
    "active": false,
    "source": null,
    "tickers_patched": []
  },
  "warnings": []
}
```

#### L1 field catalog

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `version` | string | yes | Sidecar schema version `1.0.0` |
| `as_of` | date | yes | Latest session date in primary file |
| `source_file` | string | yes | Canonical staged filename |
| `source_channel` | enum | yes | `koyfin_wtm_flows` \| `credit_cross_section_fallback` \| `hybrid` |
| `ingest_mode` | enum | yes | `timeseries_primary` \| `fallback_1d_only` \| `disabled` |
| `units.flow_usd` | string | yes | Locked: `millions_usd` |
| `units.aum_usd` | string | yes | Locked: `millions_usd` |
| `tickers.{T}.asset_id` | string | yes | From `canonical_assets`; empty if unresolved |
| `tickers.{T}.latest.flow_usd_1d` | number | if known | Raw daily flow (millions USD) |
| `tickers.{T}.latest.aum_usd` | number | if known | AUM (millions USD) |
| `tickers.{T}.latest.flow_pct_aum_1d` | number | if known | **Canonical display metric** for 1D |
| `tickers.{T}.rolling.flow_usd_5d` | number | if ≥2 sessions | Sum of last 5 sessions' `flow_usd_1d` |
| `tickers.{T}.rolling.flow_pct_aum_5d` | number | if ≥2 sessions | Sum of last 5 sessions' `flow_pct_aum_1d` |
| `tickers.{T}.rolling.sessions_in_5d` | int | yes | Count used (max 5) |
| `tickers.{T}.rolling.persistence_score_20d` | number | if ≥5 sessions | Fraction of last 20 sessions where sign matches 5D sign |

#### Computation rules (L1)

```python
# Per session row (primary parser)
flow_pct_aum_1d = (flow_usd_1d / aum_usd) * 100.0   # if aum_usd > 0

# 5D cumulative (% AUM) — NOT average; sum of daily % AUM (desk convention)
flow_pct_aum_5d = sum(flow_pct_aum_1d for last 5 trading rows)

# 5D USD — sum of raw flows
flow_usd_5d = sum(flow_usd_1d for last 5 trading rows)

# persistence_score_20d
sign_5d = sign(flow_pct_aum_5d)
persistence_score_20d = count(sign(flow_pct_aum_1d_i) == sign_5d for last 20 rows) / min(20, n_rows)
```

**Precedence:** If vendor supplies `{TICKER} Flow % AUM (D)` column, use it for `flow_pct_aum_1d` and back-solve `flow_usd_1d` only when needed for audit (`flow_usd_1d = flow_pct_aum_1d / 100 * aum_usd`).

**Relationships:**

- One **ticker** maps to zero or one `asset_id` via `canonical_asset_for_ticker("koyfin", ticker)`.
- **Node affiliation** is not stored in L1 — tickers are global. Node mapping happens in L2 via `funds_flow_baskets`.
- `series_tail` retains last 20 sessions per ticker for persistence recompute and optional UI sparkline.

---

### 1.3 L2 — `node_cockpit.funds_flows`

Attached to each of five cockpits during `build_node_cockpit()`.

```json
{
  "funds_flows": {
    "enabled": true,
    "source": "derived",
    "flows_meta": {
      "flows_status": "ok",
      "flows_source": "wtm_flows_timeseries",
      "flows_degraded": false,
      "flows_confidence_penalty": 0,
      "fallback_reason": "",
      "degrade_mode": "full"
    },
    "degrade_mode": "full",
    "as_of": "2026-06-29",
    "horizon_display": "5d",
    "basket_id": "credit_hy_ig",
    "basket_label": "Credit ETF Sponsorship",
    "node_id": "credit",
    "aggregate": {
      "flow_pct_aum_1d": 0.08,
      "flow_pct_aum_5d": 0.31,
      "flow_usd_1d": -120.5,
      "flow_usd_5d": -310.2,
      "positive_count": 3,
      "total_count": 4,
      "populated_count": 4,
      "verdict": "supportive",
      "confidence_delta": 1,
      "concentration_flag": false,
      "primary_ticker": "HYG",
      "primary_flow_pct_aum_5d": 0.31
    },
    "etfs": [
      {
        "ticker": "HYG",
        "asset_id": "hyg",
        "node_affiliation": "credit",
        "basket_role": "primary",
        "basket_weight": 0.35,
        "flow_pct_aum_1d": 0.08,
        "flow_pct_aum_5d": 0.31,
        "flow_usd_1d": -120.5,
        "flow_usd_5d": -310.2,
        "persistence_score": 0.67,
        "data_status": "ok"
      },
      {
        "ticker": "LQD",
        "asset_id": "jaaa",
        "node_affiliation": "credit",
        "basket_role": "supporting",
        "basket_weight": 0.30,
        "flow_pct_aum_1d": 0.02,
        "flow_pct_aum_5d": null,
        "flow_usd_1d": 45.0,
        "flow_usd_5d": null,
        "persistence_score": null,
        "data_status": "partial_1d_only"
      }
    ],
    "interpretation": {
      "supports_node_thesis": true,
      "divergence_flag": false,
      "summary": "HYG 5D inflows confirm constructive credit transmission.",
      "caution_line": "",
      "change_mind_trigger": "HYG 5D % AUM turns negative while spread RV still rich.",
      "degrade_notice": ""
    }
  }
}
```

#### L2 field catalog

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | bool | `false` only when entire node basket has zero populated ETFs |
| `degrade_mode` | enum | `full` \| `partial_basket` \| `fallback_1d_credit` \| `unavailable` — see §3 |
| `node_affiliation` (on etfs[]) | string | Always equals parent `node_id` |
| `basket_role` | enum | `primary` \| `supporting` \| `proxy` |
| `basket_weight` | number | From Master DD; used in aggregate weighted mean |
| `data_status` | enum | `ok` \| `partial_1d_only` \| `missing` |
| `aggregate.populated_count` | int | ETFs with at least 1D data |
| `interpretation.degrade_notice` | string | Operator-facing banner text; empty when `flows_meta.flows_status: ok` |
| `flows_meta` | object | **Machine-readable degrade contract** — UI reads before rendering verdict; see §3.0 |

#### `flows_meta` — machine-readable degrade contract (required on every L2 block)

Mirrors freshness/provenance pattern in Transmission Control: operators and UI must distinguish **true neutral** from **data unavailable** without inferring from verdict alone.

| Field | Type | Required | Values | Description |
|-------|------|----------|--------|-------------|
| `flows_status` | enum | yes | `ok` \| `partial` \| `fallback_1d` \| `unavailable` | Coarse health — drives card chrome |
| `flows_source` | enum | yes | `wtm_flows_timeseries` \| `credit_cross_section` \| `none` | Which ingest path supplied data |
| `flows_degraded` | bool | yes | | `true` when not `flows_status: ok` |
| `flows_confidence_penalty` | int | yes | 0–2 | Suppresses positive `confidence_delta`; see §3.3 |
| `fallback_reason` | string | yes | Machine code or empty | Stable key for UI/export; not free prose |
| `degrade_mode` | enum | yes | Same as §3.1 | **Alias** of `flows_status` for backward compat |

**`fallback_reason` codes (locked):**

| Code | When |
|------|------|
| `` | `flows_status: ok` |
| `missing_wtm_flows_file` | No `flows_*.csv` staged this session |
| `credit_cross_section_1d_only` | PR-3b fallback active |
| `missing_basket_etfs` | WTM-Flows present but basket incomplete |
| `ticker_columns_absent` | File staged; required tickers missing from headers |
| `non_credit_node_no_fallback` | Global fallback mode; this node has no 1D source |

**Mapping table (`flows_meta` derivation):**

| `degrade_mode` | `flows_status` | `flows_source` | `flows_degraded` | `flows_confidence_penalty` | `fallback_reason` |
|----------------|----------------|----------------|------------------|---------------------------|-------------------|
| `full` | `ok` | `wtm_flows_timeseries` | `false` | `0` | `` |
| `partial_basket` | `partial` | `wtm_flows_timeseries` | `true` | `0` | `missing_basket_etfs` |
| `fallback_1d_credit` | `fallback_1d` | `credit_cross_section` | `true` | `1` | `credit_cross_section_1d_only` |
| `unavailable` | `unavailable` | `none` | `true` | `0` | `missing_wtm_flows_file` or `non_credit_node_no_fallback` |

**UI rule:** When `flows_degraded: true`, render amber meta chip (like freshness dot) **before** verdict badge. Verdict `neutral` with `flows_status: unavailable` must **not** use supportive/neutral styling — use collapsed placeholder instead.

**`flows_confidence_penalty` semantics:**

| Value | Effect on `confidence_delta` |
|-------|---------------------------|
| `0` | Apply computed delta (−1 / 0 / +1) |
| `1` | Clamp delta to `≤ 0` (no confidence boost in degraded mode) |
| `2` | Force delta `0` (reserved: primary ETF missing 5D in `partial`) |

#### `basket_role` definitions

| Role | Meaning | Example |
|------|---------|---------|
| `primary` | Drives aggregate interpretation and card highlight | HYG on Credit |
| `supporting` | Included in breadth / weighted aggregate | LQD, BKLN on Credit |
| `proxy` | Indirect sponsor where direct instrument unavailable | IBIT on Basis (futures have no AUM) |

Exactly **one** `primary` per node basket (`primary: true` in Master DD). Others default to `supporting`; Basis BTC vehicles may be marked `proxy` where noted in registry.

#### Link to `canonical_assets`

Resolution order in `funds_flows.py`:

1. Read `asset_id` from `funds_flow_baskets.nodes.{node}.etfs[].asset_id` (locked in YAML).
2. Validate against `canonical_assets[asset_id].sources.koyfin` ticker match.
3. If mismatch, log warning; set `canonical_asset_resolved: false` on L1 ticker row.
4. UI displays `ticker` always; `asset_id` used for chart links and export only.

**New canonical assets required (PR-1):** `shy`, `ief`, `tlt`, `bil`, `iwm`, `rsp`, `ibit`, `bito`, `gbtc` (extend existing `hyg`, `jaaa`, `spy`, `qqq`, `bkln`, `cwb`).

---

## 2. Node-level integration

### 2.1 Consumption flow

```python
# node_cockpits.build_node_cockpit() — after directional + relative_value built
funds_flows = build_funds_flows(
    node_id=node_id,
    node_cockpit_draft=cockpit,  # needs directional, relative_value, rv_basis
    flows_sidecar=load_flows_sidecar(),
    basket_spec=funds_flow_basket_for_node(node_id),
)
cockpit["funds_flows"] = funds_flows
cockpit["confidence"] = apply_confidence_delta(cockpit["confidence"], funds_flows)
cockpit["directional"]["rationale"] = merge_flow_rationale(cockpit["directional"]["rationale"], funds_flows)
cockpit["relative_value"]["rationale"] = merge_flow_rationale(cockpit["relative_value"]["rationale"], funds_flows)
```

**`merge_flow_rationale` rule:** Append one sentence max when `verdict in (supportive, diverging)`:

```
"{summary}" (Flows: {verdict}.)
```

Never replace the primary node rationale — suffix only.

---

### 2.2 Credit Confirmation — worked example

**Node thesis (from cockpit):**

- `directional.posture`: `long` (constructive HY)
- `relative_value.posture`: `long_spread` (HYG/LQD cheap vs history)
- `rv_basis.active_series`: `hy_oas_proxy` richness `cheap`

**Flow basket:** HYG (primary), LQD, BKLN, CWB

| ETF | 1D % AUM | 5D % AUM | Role |
|-----|----------|----------|------|
| HYG | +0.08 | +0.31 | primary |
| LQD | +0.02 | +0.09 | supporting |
| BKLN | +0.01 | +0.04 | supporting |
| CWB | -0.01 | -0.02 | supporting |

**Aggregate (weighted):** `flow_pct_aum_5d ≈ +0.18`, breadth 3/4 positive → base verdict `supportive`.

**Sponsorship overlay:** Node bullish + RV long_spread + flows positive → `supports_node_thesis: true`, `divergence_flag: false`, `confidence_delta: +1`.

**Card display:**

```
Funds Flow Sponsorship          Supportive
1D +0.05% AUM · 5D +0.18% AUM · 3/4 positive
HYG *  +0.08%  +0.31%  ▂▄▅▆
LQD    +0.02%  +0.09%  ▂▃▄
...
HYG 5D inflows confirm constructive credit transmission.
```

**Contradiction example:** Same node thesis but HYG 5D `-0.25%` → verdict `diverging`, `confidence_delta: -1`, caution: `Price/RV improving faster than allocator sponsorship.`

---

### 2.3 Equity Breadth — worked example

**Node thesis:**

- `directional.posture`: `neutral`
- `relative_value.posture`: `long_spread` (IWM/SPY participation — small caps cheap)
- Breadth signal: IWM lagging on tracer

**Flow basket:** IWM (primary), SPY, QQQ, RSP

| ETF | 5D % AUM | Interpretation |
|-----|----------|----------------|
| IWM | -0.15 | Primary outflow — contradicts long_spread |
| SPY | +0.05 | Cap-weight inflow |
| RSP | -0.02 | Equal-weight flat |

**Aggregate:** Mixed signs, breadth 1/4 positive → verdict `mixed`. Primary IWM negative while RV says long IWM → `divergence_flag: true`, `confidence_delta: -1`.

**Card copy:** `Small-cap flows do not confirm participation pair — cap-weight holding inflows.`

**Sponsorship logic note for Breadth:** When `relative_value.structure` contains IWM/SPY, **primary ETF (IWM) sign weighs 2×** in divergence check vs aggregate alone.

---

### 2.4 `FundsFlowSponsorshipCard` — view model contract

UI receives `cockpit.funds_flows` only. No sidecar reads in browser.

**Render order (regime-first parity):** `flows_meta` chip → degrade banner → verdict → aggregate → ETF rows → interpretation.

#### Mandatory fields (card must not render without these)

| Field | Why mandatory |
|-------|----------------|
| `flows_meta.flows_status` | Distinguishes ok vs unavailable vs fallback |
| `flows_meta.flows_source` | Provenance line in card footer |
| `flows_meta.flows_degraded` | Chrome color (neutral vs amber) |
| `enabled` | Hide vs show card |
| `aggregate.verdict` | When `enabled` and not `unavailable` |
| `interpretation.degrade_notice` | When `flows_degraded: true` |

#### Optional fields (omit section when absent)

| Field | Section |
|-------|---------|
| `aggregate.flow_pct_aum_5d` | 5D aggregate column — hidden when `fallback_1d` |
| `etfs[].flow_pct_aum_5d` | Per-row 5D |
| `etfs[].persistence_score` | Sparkline / persistence dot |
| `interpretation.caution_line` | Second line |
| `interpretation.change_mind_trigger` | Fullscreen variant only |
| `aggregate.flow_usd_*` | Debug/export only; hidden in default rail |

| Prop / section | Source field | Render rule |
|----------------|--------------|-------------|
| Meta chip | `flows_meta.*` | `ok` hidden; else amber: `{flows_status} · {flows_source}` |
| Header | static | `Funds Flow Sponsorship` |
| Verdict badge | `aggregate.verdict` | **Only if** `flows_status` ∈ `ok`, `partial`, `fallback_1d` |
| Aggregate line | `aggregate.*`, `horizon_display` | `1D {x}% AUM · 5D {y}% AUM · {pos}/{total} positive` |
| Degrade banner | `interpretation.degrade_notice` | Amber single line; driven by `fallback_reason` template |
| ETF rows | `etfs[]` max 5 | Sort: primary first, then by `abs(flow_pct_aum_5d)` desc |
| Row highlight | `basket_role === 'primary'` | Left border `*` |
| 5D column | `flow_pct_aum_5d` | Show `—` when null; tooltip from `data_status` |
| Interpretation | `interpretation.summary` | One line, neutral type |
| Caution | `interpretation.caution_line` | Only when `divergence_flag` |
| Footer | `flows_meta.flows_source`, `as_of` | `Source: WTM-Flows · 2026-06-29` |

**Compare mode:** `renderFundsFlowSponsorshipCard(cockpit, { variant: 'compare', horizon: sharedHorizon })` — omits sparklines, fixed height 120px.

**Fullscreen Why:** `variant: 'expanded'` — adds `change_mind_trigger` + full ETF table + `degrade_mode` diagnostic line (operator/debug).

---

### 2.5 Sponsorship logic (deterministic)

Implemented in `funds_flows.assign_verdict()`:

**Inputs:**

- `aggregate` flow metrics (1D, 5D, breadth, concentration)
- `node.directional.posture`, `node.relative_value.posture`
- `node.rv_basis.richness_label` (active series)
- `thresholds` from Master DD

**Algorithm (ordered):**

1. If `degrade_mode == fallback_1d_credit` → cap verdict at `neutral` or `mixed` (never `supportive` or `diverging` on 5D rules).
2. Compute `base_verdict` from flow-only table (design doc § interpretation).
3. If `directional` in (`long`, `long_spread`) and `flow_pct_aum_5d < divergence_5d` → `diverging`.
4. If `directional` in (`short`, `short_spread`) and `flow_pct_aum_5d > supportive_5d` → `mixed`.
5. If primary ETF sign opposes `relative_value.posture` → set `divergence_flag` (Breadth/Credit rule).
6. Map verdict → `confidence_delta` per design doc; apply tier clamp `{low, medium, high}`.

**`supports_node_thesis`:** `true` when verdict `supportive` and not `divergence_flag`; else `false`.

---

## 3. Degradation and fallback behavior

### 3.0 Fallback precedence (locked)

```
1. Dedicated WTM-Flows time-series (`flows_*.csv` → L1 sidecar)     PRIMARY
2. Credit cross-section 1D fallback (PR-3b)                         SECOND — Credit node only
3. Unavailable (`flows_meta.flows_status: unavailable`)             LAST — no synthetic 5D
```

Non-credit nodes never advance past step 3 when step 1 missing. **Never** infer neutrality from absence.

---

### 3.1 `degrade_mode` state machine

| Mode | Trigger | 5D available? | Nodes affected |
|------|---------|---------------|----------------|
| `full` | `flows_*.csv` staged; ≥60% basket ETFs have 5D | yes | All with populated baskets |
| `partial_basket` | Primary timeseries ok; some supporting ETFs missing | partial | Per node — missing rows `data_status: missing` |
| `fallback_1d_credit` | No `flows_*.csv`; credit raw cross-section ingested | **no** | **Credit only** |
| `unavailable` | No flows file and no fallback | no | All — `enabled: false` |

**Detection in hydrate:**

```python
def resolve_degrade_mode(sidecar, node_id, basket) -> str:
    if sidecar.ingest_mode == "timeseries_primary":
        populated = count_etf_5d(sidecar, basket)
        if populated == 0:
            return "unavailable"
        if populated < len(basket.etfs):
            return "partial_basket"
        return "full"
    if sidecar.ingest_mode == "fallback_1d_only" and node_id == "credit":
        return "fallback_1d_credit"
    return "unavailable"
```

Non-credit nodes in `fallback_1d_credit` global mode: `enabled: false`, `degrade_mode: unavailable` — **do not** fabricate 5D from credit file.

---

### 3.2 UI copy by degrade mode

| `degrade_mode` | `interpretation.degrade_notice` (exact string) |
|----------------|-----------------------------------------------|
| `full` | `` (empty) |
| `partial_basket` | `Partial flow coverage — some basket ETFs missing from WTM-Flows.` |
| `fallback_1d_credit` | `5D flows unavailable — using 1D Credit cross-section fallback.` |
| `unavailable` | Card hidden or collapsed: `Flows data not available for this session.` |

**Card visibility:**

- `unavailable` → render collapsed placeholder (one line, no ETF rows).
- `fallback_1d_credit` → show 1D columns only; 5D column header grayed with `—`.

---

### 3.3 Verdict and confidence in degraded mode

| Mode | Verdict cap | `confidence_delta` | `divergence_flag` |
|------|-------------|-------------------|-------------------|
| `full` | none | -1 / 0 / +1 per algorithm | allowed |
| `partial_basket` | none; note missing ETFs | max +1; -1 only if primary ETF has 5D | allowed if primary ok |
| `fallback_1d_credit` | **max `mixed`**; never `supportive` or `diverging` | **0 only** (`flows_confidence_penalty: 1`) | **forced false** |
| `unavailable` | n/a (`enabled: false`) | 0 | false |

**Rationale merge in fallback:** Append ` (Flows: 1D fallback only — treat as indicative.)` instead of full sponsorship sentence.

---

### 3.4 Incomplete `flows_*.csv` (partial file)

If file staged but ticker columns missing:

- Ingest all present tickers into sidecar.
- Set `ingest_mode: timeseries_primary` with `warnings: ["missing_columns: IBIT, IWM"]`.
- Per node: `partial_basket` if any basket ETF missing; aggregate uses only populated members (renormalize weights to sum 1.0 over populated).

**Never** impute zero flow for missing tickers (avoid false neutrality).

---

## 4. Implementation responsibilities

### 4.1 PR-1 — Master Data Dictionary (Bridge)

**Deliverables:**

| Item | Location |
|------|----------|
| `funds_flow_baskets` | `data_dictionary.yaml` |
| `funds_flow_thresholds` | `data_dictionary.yaml` |
| `funds_flow_column_patterns` | `data_dictionary.yaml` |
| Dataset `flows` in `file_naming_conventions` | `flows_{YYYYMMDD}_{HHMM}.csv` |
| `canonical_assets` extensions | see §5 |
| Helpers | `funds_flow_basket_for_node()`, `funds_flow_thresholds()`, `funds_flow_column_map()` |
| Tests | `test_funds_flow_baskets_locked`, `test_flows_filename_pattern` |

**Does not include:** parsing logic, UI, or node verdict code.

---

### 4.2 PR-3a — Primary parser (Integration Dynamo)

**File:** `whinfell_pipeline/flows_parser.py`

| Function | Responsibility |
|----------|----------------|
| `detect_flows_format(headers)` | Distinguish WTM-Flows wide vs invalid |
| `parse_flows_csv(path) -> FlowsSidecar` | Row-by-row Date parsing; build ticker series |
| `compute_rolling_metrics(series) -> RollingMetrics` | 5D sums, persistence |
| `write_flows_sidecar(payload, path)` | Atomic write `data/flows/v1/latest_flows.json` |

**Integration point:** `csv_download.py` or `batch_collect.py` after successful stage of `dataset=flows`:

```python
if dataset == "flows":
    flows_parser.parse_and_write(staged_path, default_flows_sidecar_path())
```

**Column mapping:**

| Vendor header | Field |
|---------------|-------|
| `Date` | session date |
| `{T} Flow (D)` | `flow_usd_1d` (millions) |
| `{T} AUM` | `aum_usd` (millions) |
| `{T} Flow % AUM (D)` | `flow_pct_aum_1d` (if present, preferred) |
| `Fund Flows/Periodic (D)` (credit only) | fallback path — not primary parser |

**Tests:** Fixture `whinfell_pipeline/examples/flows/WTM-Flows-Global-head.csv` (10 rows) + full integration with quarantine file copy.

---

### 4.3 PR-3b — Credit fallback (Integration Dynamo)

**File:** `whinfell_pipeline/flows_fallback.py`

**Trigger:** `flows_*.csv` not staged this run; raw credit cross-section available in quarantine or parallel raw ingest path.

| Function | Responsibility |
|----------|----------------|
| `parse_credit_cross_section_flows(path)` | Read Ticker, AUM, Fund Flows/Periodic (D) |
| `merge_fallback_into_sidecar(sidecar, credit_rows)` | Patch Credit tickers 1D only; set `ingest_mode: fallback_1d_only` |

**Scope limit:** Only tickers in `credit_hy_ig` basket. Does not write 5D fields.

---

### 4.4 PR-2 extension — `funds_flows.py` (Bridge)

| Function | Responsibility |
|----------|----------------|
| `build_funds_flows(node_id, sidecar, node_cockpit)` | L2 view model |
| `compute_aggregate(etf_rows, weights)` | Weighted 1D/5D, breadth, concentration |
| `assign_verdict(aggregate, node_cockpit, thresholds, degrade_mode)` | Sponsorship labels |
| `build_interpretation(...)` | summary, caution, change_mind, degrade_notice |
| `apply_confidence_delta(tier, delta)` | low↔medium↔high clamp |

**Wire:** `node_cockpits.build_node_cockpit()` — load sidecar once per hydrate, pass to each node build.

---

### 4.5 Phase2_Node_Cockpit_Data_Model.md updates (Blueprint)

Add new section **§9.1 Funds Flow Sponsorship** (pointer to this spec):

- `funds_flows` optional block on each `node_cockpit`
- MVP checklist row: flows enabled or graceful unavailable
- Cross-reference `degrade_mode` enum

**Do not duplicate** full field catalogs — link to this document as implementation authority.

---

### 4.6 UI — `FundsFlowSponsorshipCard` (Clarity + Bridge, PR-4)

| Owns | Does not own |
|------|----------------|
| Render L2 fields | Parse CSV |
| Variant styles (rail / compare / expanded) | Verdict computation |
| Tabular nums, badge colors | Confidence delta math |
| Read `degrade_notice` verbatim | Gate/score display |

**Suggested JS shape:**

```javascript
function FundsFlowSponsorshipCard({ fundsFlows, variant = 'rail' }) {
  if (!fundsFlows?.enabled) return <FlowsUnavailable collapsed />;
  return (
    <section className="ff-sponsorship-card" data-degrade={fundsFlows.degrade_mode}>
      <header>...</header>
      {fundsFlows.interpretation.degrade_notice && <DegradeBanner />}
      <AggregateLine aggregate={fundsFlows.aggregate} />
      <EtfTable rows={fundsFlows.etfs} show5d={fundsFlows.degrade_mode !== 'fallback_1d_credit'} />
      <Interpretation text={fundsFlows.interpretation.summary} />
    </section>
  );
}
```

---

### 4.7 Hydration bundle extensions (v1.2.0)

| Key | Change |
|-----|--------|
| `hydration_version` | `1.2.0` when any `funds_flows.enabled` |
| `node_cockpits.*.funds_flows` | L2 block per node |
| `flows_sidecar` (optional) | Copy of L1 sidecar metadata for provenance panel — `snapshot_id`, `source_file`, `ingest_mode`, `warnings` |

```json
{
  "hydration_version": "1.2.0",
  "flows_sidecar": {
    "as_of": "2026-06-29",
    "source_file": "flows_20260629_1525.csv",
    "ingest_mode": "timeseries_primary",
    "ticker_count": 18,
    "warnings": []
  },
  "node_cockpits": { "...": { "funds_flows": {} } }
}
```

---

### 4.8 WTM EXPORT extensions

Append to existing `NODE COCKPIT` block in `export_contract.py`:

```
Funds Flow Enabled: true
Funds Flow Status: ok
Funds Flow Source: wtm_flows_timeseries
Funds Flow Degraded: false
Funds Flow Fallback Reason:
Funds Flow Verdict: supportive
Funds Flow 1D: +0.05% AUM
Funds Flow 5D: +0.18% AUM
Funds Flow Breadth: 3/4
Funds Flow Confidence Penalty: 0
Funds Flow Summary: HYG 5D inflows confirm constructive credit transmission.
```

Omit 5D lines when `flows_status: fallback_1d`. Parser round-trip optional Phase 2b — export-first acceptable for MVP.

---

## 5. Master Data Dictionary impact

### 5.1 New top-level blocks

```yaml
funds_flow_baskets:        # §1.3 baskets per node — see design doc
funds_flow_thresholds:     # verdict cutoffs
funds_flow_column_patterns: # vendor → canonical field
funds_flow_ingest:         # sidecar path, units, degrade rules
```

### 5.2 `funds_flow_thresholds` (starter)

```yaml
funds_flow_thresholds:
  version: "1.0"
  supportive_5d_pct: 0.15
  weak_5d_pct: 0.05
  divergence_5d_pct: -0.05
  breadth_supportive_ratio: 0.60
  concentration_single_etf: 0.70
  primary_divergence_weight: 2.0
```

### 5.3 File naming and datasets

| Pattern | Dataset | Source |
|---------|---------|--------|
| `flows_{YYYYMMDD}_{HHMM}.csv` | `flows` | koyfin |
| `WTM-Flows*.csv` | `flows` (normalize) | koyfin |
| `WTM-Flows-Global.csv` | `flows` (normalize) | koyfin |

Add to `normalize_rules`:

```yaml
- detect_glob: "WTM-Flows*.csv"
  canonical_template: "flows_{YYYYMMDD}_{HHMM}.csv"
  dataset: flows
```

Add to `watchlist_names.koyfin_saved_views`:

```yaml
WTM-Flows:
  dataset: flows
  vendor_detect_glob: "WTM-Flows*.csv"
  optional: true
  clicks: 2
```

### 5.4 Column mappings

```yaml
funds_flow_column_patterns:
  flow_usd_1d: ["{TICKER} Flow (D)", "Fund Flows/Periodic (D)"]
  aum_usd: ["{TICKER} AUM", "AUM"]
  flow_pct_aum_1d: ["{TICKER} Flow % AUM (D)"]
  date: ["Date"]
```

### 5.5 `json_structures` updates

```yaml
hydration_bundle:
  expected_version: "1.2.0"
  blocks:
    flows_sidecar: [as_of, source_file, ingest_mode, ticker_count, warnings]
    node_cockpits: [... existing ..., funds_flows per node]
flows_sidecar:
  path: "data/flows/v1/latest_flows.json"
  version_field: version
```

### 5.6 `canonical_assets` additions

| `asset_id` | Koyfin ticker | Class |
|------------|---------------|-------|
| `shy` | SHY | rates_etf |
| `ief` | IEF | rates_etf |
| `tlt` | TLT | rates_etf |
| `bil` | BIL | rates_etf |
| `iwm` | IWM | equity_etf |
| `rsp` | RSP | equity_etf |
| `ibit` | IBIT | btc_vehicle |
| `bito` | BITO | btc_vehicle |
| `gbtc` | GBTC | btc_vehicle |

### 5.7 `transmission_outputs` addition

```yaml
flows_sidecar:
  source: data/flows/v1/latest_flows.json
  fields: [as_of, ingest_mode, tickers]
```

### 5.8 `collection_manifest.yaml` addition

```yaml
- id: koyfin_flows
  priority: 15
  optional: true
  source: koyfin
  dataset: flows
  saved_view: WTM-Flows
  canonical_name: "flows_{YYYYMMDD}_{HHMM}.csv"
```

Not added to `required_batch_ids`.

---

## 6. PR sequence (locked order)

```
PR-1  Master DD registry + normalize rule + canonical_assets
PR-3a flows_parser.py + sidecar write + batch_collect hook
PR-3b flows_fallback.py (credit 1D)
PR-2  funds_flows.py + node_cockpits wire + hydration v1.2.0
PR-4  FundsFlowSponsorshipCard UI
PR-5  WTM export lines + Phase2_Node_Cockpit §9.1 pointer
```

**Gate:** This spec **v1.1** locked (§8 sign-off) → then PR-1 and PR-3a may start in parallel.

---

## 8. Review checklist (desk sign-off)

- [ ] Companion spec authority accepted (not embedded in main cockpit doc)
- [ ] Option D hybrid + fallback precedence §3.0
- [ ] `flows_meta` machine-readable flags — UI can distinguish neutral vs unavailable
- [ ] 5D = sum of daily % AUM (not average)
- [ ] Units: millions USD for Flow and AUM
- [ ] Credit-only fallback limited to Credit node
- [ ] Non-credit nodes: `flows_status: unavailable` when no WTM-Flows file
- [ ] `confidence_delta` never moves composite_score or gate
- [ ] Appendix A JSON examples match implementation expectations
- [ ] ETF basket ticker list for Clark's WTM-Flows view

---

## Key decisions (for lock)

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Companion spec file is authoritative | Parser / DD / UI lock interfaces without overloading cockpit doc |
| 2 | Three-layer model L0/L1/L2 | Clean separation ingest vs node view |
| 3 | `flows_meta` block on every L2 payload | Same clarity standard as freshness/provenance in TC |
| 4 | `flows_confidence_penalty` as data | Degraded mode suppresses boost without ambiguous verdict |
| 5 | 5D % AUM = sum of daily % | Desk cumulative convention |
| 6 | Fallback precedence: WTM-Flows → credit 1D → unavailable | Option D locked |
| 7 | Hydration v1.2.0 | Backward-compatible capability signal |

---

## Appendix A — JSON examples (implementation-grade)

### A.1 L1 — Parsed flow record (single ticker, post-PR-3a)

```json
{
  "ticker": "HYG",
  "asset_id": "hyg",
  "canonical_asset_resolved": true,
  "latest": {
    "date": "2026-06-29",
    "flow_usd_1d": -120.5,
    "aum_usd": 14505.42,
    "flow_pct_aum_1d": -0.83
  },
  "rolling": {
    "flow_usd_5d": -310.2,
    "flow_pct_aum_5d": -2.14,
    "sessions_in_5d": 5,
    "persistence_score_20d": 0.65
  }
}
```

### A.2 L2 — Healthy node payload (`credit`, `flows_status: ok`)

```json
{
  "funds_flows": {
    "enabled": true,
    "source": "derived",
    "as_of": "2026-06-29",
    "horizon_display": "5d",
    "basket_id": "credit_hy_ig",
    "basket_label": "Credit ETF Sponsorship",
    "node_id": "credit",
    "flows_meta": {
      "flows_status": "ok",
      "flows_source": "wtm_flows_timeseries",
      "flows_degraded": false,
      "flows_confidence_penalty": 0,
      "fallback_reason": "",
      "degrade_mode": "full"
    },
    "aggregate": {
      "flow_pct_aum_1d": 0.05,
      "flow_pct_aum_5d": 0.18,
      "positive_count": 3,
      "total_count": 4,
      "verdict": "supportive",
      "confidence_delta": 1
    },
    "etfs": [
      {
        "ticker": "HYG",
        "asset_id": "hyg",
        "node_affiliation": "credit",
        "basket_role": "primary",
        "flow_pct_aum_1d": 0.08,
        "flow_pct_aum_5d": 0.31,
        "data_status": "ok"
      }
    ],
    "interpretation": {
      "supports_node_thesis": true,
      "divergence_flag": false,
      "summary": "HYG 5D inflows confirm constructive credit transmission.",
      "degrade_notice": ""
    }
  }
}
```

### A.3 L2 — Degraded fallback (`credit`, no WTM-Flows file)

```json
{
  "funds_flows": {
    "enabled": true,
    "source": "derived",
    "as_of": "2026-06-29",
    "horizon_display": "1d",
    "basket_id": "credit_hy_ig",
    "node_id": "credit",
    "flows_meta": {
      "flows_status": "fallback_1d",
      "flows_source": "credit_cross_section",
      "flows_degraded": true,
      "flows_confidence_penalty": 1,
      "fallback_reason": "credit_cross_section_1d_only",
      "degrade_mode": "fallback_1d_credit"
    },
    "aggregate": {
      "flow_pct_aum_1d": 0.04,
      "flow_pct_aum_5d": null,
      "positive_count": 2,
      "total_count": 4,
      "verdict": "neutral",
      "confidence_delta": 0
    },
    "etfs": [
      {
        "ticker": "HYG",
        "asset_id": "hyg",
        "basket_role": "primary",
        "flow_pct_aum_1d": 0.08,
        "flow_pct_aum_5d": null,
        "data_status": "partial_1d_only"
      }
    ],
    "interpretation": {
      "supports_node_thesis": false,
      "divergence_flag": false,
      "summary": "1D credit flows mildly positive — 5D unavailable.",
      "degrade_notice": "5D flows unavailable — using 1D Credit cross-section fallback."
    }
  }
}
```

### A.4 L2 — Unavailable (`breadth`, no WTM-Flows, no fallback)

```json
{
  "funds_flows": {
    "enabled": false,
    "source": "derived",
    "as_of": "2026-06-29",
    "basket_id": "breadth_participation",
    "node_id": "breadth",
    "flows_meta": {
      "flows_status": "unavailable",
      "flows_source": "none",
      "flows_degraded": true,
      "flows_confidence_penalty": 0,
      "fallback_reason": "non_credit_node_no_fallback",
      "degrade_mode": "unavailable"
    },
    "aggregate": {
      "verdict": null,
      "confidence_delta": 0
    },
    "etfs": [],
    "interpretation": {
      "summary": "",
      "degrade_notice": "Flows data not available for this session."
    }
  }
}
```

### A.5 L2 — Partial basket (WTM-Flows missing IBIT/IWM columns)

```json
{
  "funds_flows": {
    "enabled": true,
    "node_id": "highbeta",
    "flows_meta": {
      "flows_status": "partial",
      "flows_source": "wtm_flows_timeseries",
      "flows_degraded": true,
      "flows_confidence_penalty": 0,
      "fallback_reason": "missing_basket_etfs",
      "degrade_mode": "partial_basket"
    },
    "aggregate": {
      "flow_pct_aum_5d": 0.09,
      "verdict": "neutral",
      "confidence_delta": 0
    },
    "interpretation": {
      "degrade_notice": "Partial flow coverage — some basket ETFs missing from WTM-Flows."
    }
  }
}
```

### A.6 Hydration bundle excerpt (v1.2.0, healthy session)

```json
{
  "hydration_version": "1.2.0",
  "flows_sidecar": {
    "as_of": "2026-06-29",
    "source_file": "flows_20260629_1525.csv",
    "ingest_mode": "timeseries_primary",
    "flows_status": "ok",
    "ticker_count": 18,
    "warnings": []
  },
  "node_cockpits": {
    "credit": { "funds_flows": { "flows_meta": { "flows_status": "ok" } } }
  }
}
```

### A.7 WTM EXPORT NODE COCKPIT lines (degraded fallback)

```
Funds Flow Enabled: true
Funds Flow Status: fallback_1d
Funds Flow Source: credit_cross_section
Funds Flow Degraded: true
Funds Flow Fallback Reason: credit_cross_section_1d_only
Funds Flow Verdict: neutral
Funds Flow 1D: +0.04% AUM
Funds Flow Confidence Penalty: 1
Funds Flow Summary: 1D credit flows mildly positive — 5D unavailable.
```

---

**Next step after §8 lock:** Execute PR-1 + PR-3a using `staged_raw/quarantine/.../WTM-Flows-Global.csv` as golden fixture.