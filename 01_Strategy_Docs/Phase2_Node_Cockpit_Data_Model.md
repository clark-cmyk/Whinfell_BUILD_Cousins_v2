# Phase 2 — Node Cockpit Data Model

**Version:** 0.2 (locked decisions applied)  
**Date:** June 29, 2026  
**Authors:** BUILD Cousins (Blueprint + Bridge)  
**Status:** Locked — ready for implementation planning  
**Prerequisites:** [Master Data Dictionary v1.0](Master_Data_Dictionary_v1.0.md) (Locked), hydration bundle v1.0.0 stable

---

## Purpose

Define the **minimum data shape** for one ladder node to function as a **fully independent trading cockpit**. This document covers fields and JSON structure only — no UI, no pipeline code, no Transmission Control changes.

**Scope:** One reusable `node_cockpit` object, instantiated five times (Liquidity, Credit, Breadth, High-Beta/BTC, Basis). Phase 3 UI and Phase 4 validation consume this model unchanged.

---

## Locked decisions (June 29, 2026)

| # | Topic | Decision |
|---|-------|----------|
| 1 | **Composite score authority** | Node-specific weighted components from score-calculation docs are **primary**. `horizon_net` is **fallback only** when component data is missing or incomplete. |
| 2 | **Quartile & percentile direction** | **No global Q4=rich rule.** Each RV/basis series carries `quartile_direction`: `higher_is_richer` \| `higher_is_cheaper`. Quartile/percentile computed **per series, per horizon** (1M/3M/6M/12M/3Y). |
| 3 | **Options implementation** | Defer full options to **Phase 2b**. Schema retains `instrument_class: options`; MVP populates **ETF, futures, combinations only**. |
| 4 | **China ladder coupling** | **Soft coupling** via optional `china_parallel` block. Global cockpits remain **fully operable** when China reference is missing or empty. |

---

## Canonical node registry

Locked IDs from Transmission Control `LADDER` (Master DD v1.0):

| `node_id` | Display name | Primary signal domain |
|-----------|--------------|----------------------|
| `liquidity` | Liquidity & Rates | Curve shape · front-end funding |
| `credit` | Credit Confirmation | HY/IG · spread confirmation |
| `breadth` | Equity Breadth | Participation · index vs breadth |
| `highbeta` | High-Beta / BTC | BTC beta transmission vs equities |
| `basis` | Basis & Term Structure | Futures calendar · contango/backwardation |

All JSON keys use **snake_case** per Master DD v1.0.

---

## Design principles

1. **Self-contained per node** — each cockpit object has everything needed to render signal, recs, implementation, sizing, and RV/basis without cross-node lookups (except optional global context block).
2. **Pipeline vs operator** — every field is tagged `source`: `pipeline` | `derived` | `operator` | `default`.
3. **Reuse before invent** — tracer horizons (`d1`, `d5`, `d20`, `d60`), freshness, and `canonical_assets` from Master DD; extend only where cockpit capability is missing.
4. **Progressive fill** — MVP cockpit loads with signal + directional stub; RV, implementation, and quartile panels degrade gracefully when history is absent.
5. **Round-trip safe** — per-node block must serialize to WTM EXPORT v2.2 and re-import without key drift.

---

## 1. Core node signal data

Minimum fields the cockpit needs to show **what the node is saying right now**.

| Field | Type | Required | Source | Description |
|-------|------|----------|--------|-------------|
| `node_id` | string | yes | locked | One of five canonical IDs |
| `display_name` | string | yes | locked | Human label from registry |
| `composite_score` | int 0–100 | yes | derived | Stage score from **node-specific weighted components** (score-calculation docs); `horizon_net` fallback only |
| `composite_score_source` | string | yes | derived | `weighted_components` \| `horizon_net_fallback` — which authority produced the score |
| `band` | string | yes | derived | Desk band label (e.g. `Supportive`, `Mixed`, `Fragile`, `Blocked`) |
| `band_key` | string | yes | derived | Machine band key for styling (`supportive` \| `mixed` \| `fragile` \| `blocked`) |
| `freshness_status` | string | yes | pipeline | `fresh` \| `aging` \| `stale` \| `unknown` (reuse `whinfell_pipeline.freshness`) |
| `as_of` | ISO-8601 | yes | pipeline | Observation timestamp for this node's primary inputs |
| `horizon_marks` | object | yes | pipeline/operator | `{ d1, d5, d20, d60 }` each `up` \| `flat` \| `down` — same contract as `suggested_tracer` / tracer matrix |
| `horizon_net` | int | yes | derived | Sum of horizon mark scores (existing `HZ_SCORE`: up=+1, flat=0, down=−1) |
| `is_weakest_link` | bool | yes | derived | True when this node is global ladder weakest stage |
| `weakest_context` | object | no | derived | When `is_weakest_link`: `{ global_health_score, transmission_state, key_observation }` |
| `key_observation` | string | yes | pipeline/operator | One-line desk-readable signal summary |
| `component_inputs` | array | yes | pipeline | Ticker feed strip — see §7 |
| `confidence` | string | no | derived | `high` \| `medium` \| `low` — from data completeness + mark agreement |
| `gate_interaction` | object | no | derived | `{ zone, blocks_directional, blocks_rv, note }` — how global gate affects this node |
| `china_parallel` | object | no | pipeline | Optional soft-coupling to matching China ladder stage — see §1.1 |

**Derived rules (locked):**
- `composite_score`: **primary** = weighted sum of `component_inputs[].contribution` per node score-calculation doc (e.g. `04_Score_Calculation/Whinfell_Credit_Confirmation_Score_Logic.md` for credit). **Fallback** = normalized `horizon_net` mapped 0–100 when fewer than 2 components present or weights unavailable; set `composite_score_source: horizon_net_fallback`.
- `is_weakest_link`: compare `composite_score` across all five nodes (never `horizon_net` alone when weighted score exists); tie-break: liquidity → credit → breadth → highbeta → basis.
- `freshness_status`: computed from oldest `component_inputs[].as_of` vs desk thresholds.

### 1.1 China parallel block (soft coupling — locked)

Optional reference to the matching China ladder stage. **Absence or emptiness must not block cockpit operation.**

| Field | Type | Required | Source | Description |
|-------|------|----------|--------|-------------|
| `china_parallel` | object | no | pipeline | Omitted or `present: false` when China data unavailable |
| `china_parallel.present` | bool | no | pipeline | `true` when China stage data populated |
| `china_parallel.stage_id` | string | if present | locked | Matches global `node_id` (e.g. `credit`) |
| `china_parallel.stage_name` | string | if present | pipeline | China ladder display name |
| `china_parallel.horizon_marks` | object | if present | pipeline | `{ d1, d5, d20, d60 }` from `china_ladder.horizons` |
| `china_parallel.horizon_net` | int | if present | derived | China stage net for this stage |
| `china_parallel.composite_score` | int | if present | derived | China stage composite (if computed) |
| `china_parallel.note` | string | no | derived | Desk-readable coupling context (informational only) |

**Independence rule:** `directional`, `relative_value`, `implementations`, and `sizing` on the global cockpit are **never** overridden by `china_parallel`. China data is display/context only in Phase 2 MVP.

---

## 2. Directional trade recommendation fields

Expresses **beta-on / beta-off view** for the node's primary risk factor.

| Field | Type | Required | Source | Description |
|-------|------|----------|--------|-------------|
| `directional` | object | yes | derived/operator | Container below |
| `directional.posture` | string | yes | derived | `long` \| `short` \| `neutral` \| `no_trade` |
| `directional.conviction` | string | yes | derived | `high` \| `medium` \| `low` |
| `directional.rationale` | string | yes | derived | Short desk sentence (feeds "Here's Why") |
| `directional.horizon` | string | no | derived | Primary holding horizon (`1d`–`60d` or `1m`–`3y`) |
| `directional.invalidation` | string | no | derived/operator | What would flip the call |
| `directional.size_hint` | string | no | derived | Qualitative only until sizing module enabled (`full` \| `half` \| `probe` \| `flat`) |
| `directional.blocked` | bool | yes | derived | True when gate or weakest-link logic blocks directional expression |
| `directional.block_reason` | string | if blocked | derived | Human-readable block explanation |

**MVP default:** When pipeline cannot infer posture, set `posture: neutral`, `conviction: low`, `blocked: true` if global gate is Red, else `blocked: false`.

---

## 3. Market-neutral / relative-value recommendation fields

Expresses **pair/spread/basis view** independent of directional beta.

| Field | Type | Required | Source | Description |
|-------|------|----------|--------|-------------|
| `relative_value` | object | yes | derived/operator | Container below |
| `relative_value.posture` | string | yes | derived | `long_spread` \| `short_spread` \| `neutral` \| `no_trade` |
| `relative_value.structure` | string | yes | derived | Trade structure label (e.g. `HYG/LQD`, `IBIT/QQQ`, `BT calendar`, `2s10s flattener`) |
| `relative_value.conviction` | string | yes | derived | `high` \| `medium` \| `low` |
| `relative_value.rationale` | string | yes | derived | Desk sentence for RV leg |
| `relative_value.leg_long` | string | no | derived | `canonical_assets` id or vendor ticker |
| `relative_value.leg_short` | string | no | derived | `canonical_assets` id or vendor ticker |
| `relative_value.hedge_ratio` | number | no | derived/operator | Units of short per long (default 1.0) |
| `relative_value.target` | string | no | derived | Target level or z-score (e.g. `+0.5σ`, `25 bps`) |
| `relative_value.stop` | string | no | derived/operator | Stop / unwind trigger |
| `relative_value.blocked` | bool | yes | derived | RV-specific gate block |
| `relative_value.block_reason` | string | if blocked | derived | |

**Node-specific RV defaults (illustrative, locked at implementation):**

| `node_id` | Default `structure` |
|-----------|---------------------|
| `liquidity` | 2s10s curve trade / SOFR spread |
| `credit` | HYG vs LQD (or HY−IG OAS proxy) |
| `breadth` | IWM/SPY participation pair |
| `highbeta` | IBIT vs QQQ beta spread |
| `basis` | BTC near vs deferred calendar |

---

## 4. Implementation options

Ordered list of **how to express** the active recommendation (directional and/or RV). Operator selects one; pipeline may pre-rank.

| Field | Type | Required | Source | Description |
|-------|------|----------|--------|-------------|
| `implementations` | array | yes | derived | See row schema below |
| `implementations[].id` | string | yes | derived | Stable key (`liq_ief_tlt`, `btc_btm26_calendar`, etc.) |
| `implementations[].instrument_class` | string | yes | derived | `etf` \| `futures` \| `combination` (MVP); `options` reserved for Phase 2b — not populated in MVP |
| `implementations[].label` | string | yes | derived | Desk display name |
| `implementations[].legs` | array | yes | derived | `[{ side, asset_id, vendor_ticker, ratio }]` — `asset_id` from `canonical_assets` |
| `implementations[].liquidity_tier` | string | no | derived | `institutional` \| `desk` \| `thin` |
| `implementations[].margin_profile` | string | no | default | Reference key into margin defaults (`cme_btc`, `ibkr_etf`, etc.) |
| `implementations[].notes` | string | no | derived | Roll, expiry, or liquidity caveat |
| `implementations[].rank` | int | no | derived | 1 = preferred |
| `selected_implementation_id` | string | no | operator | Active choice; persisted in TC state |

**Combination example (basis node):**
```json
{
  "id": "basis_btc_calendar_plus_ibit_hedge",
  "instrument_class": "combination",
  "label": "BT calendar + IBIT beta hedge",
  "legs": [
    { "side": "long", "asset_id": "btc_near_contract", "vendor_ticker": "BTM26", "ratio": 1 },
    { "side": "short", "asset_id": "btc_deferred_contract", "vendor_ticker": "BTQ26", "ratio": 1 },
    { "side": "short", "asset_id": "btc_vehicle_ibit", "vendor_ticker": "IBIT", "ratio": 0.3 }
  ]
}
```

---

## 5. Sizing inputs

Supports **Portfolio Size · Kelly · Margin** (Phase 3 module reads/writes these fields). All monetary values in **USD** unless noted.

| Field | Type | Required | Source | Description |
|-------|------|----------|--------|-------------|
| `sizing` | object | yes | operator/default | Container below |
| `sizing.enabled` | bool | yes | operator | Margin module toggle (default `false` in Phase 2 data) |
| `sizing.portfolio_nav_usd` | number | no | operator | Total portfolio NAV input |
| `sizing.risk_budget_bps` | number | no | operator | Max risk budget for this node trade (basis points of NAV) |
| `sizing.kelly_fraction` | number | no | operator/default | Assumed Kelly multiplier 0–1 (desk default e.g. `0.25` = quarter-Kelly) |
| `sizing.max_notional_usd` | number | no | derived | Hard cap from gate + posture |
| `sizing.recommended_notional_usd` | number | no | derived | NAV × risk_budget × kelly × conviction factor |
| `sizing.contracts_or_shares` | number | no | derived | Sized units for `selected_implementation_id` |
| `sizing.margin` | object | no | derived/default | See below |
| `sizing.margin.broker` | string | no | default | `cme` \| `ibkr` |
| `sizing.margin.initial_usd` | number | no | derived | Initial margin for sized position |
| `sizing.margin.maintenance_usd` | number | no | derived | Maintenance margin |
| `sizing.margin.utilization_pct` | number | no | derived | `initial_usd / portfolio_nav_usd × 100` |
| `sizing.margin.source` | string | no | default | `cme_default_2026` \| `ibkr_default_2026` \| `operator_override` |

**Margin default tables (reference data, not embedded per node):** Stored once in `data/reference/margin_defaults.json` (Phase 2 deliverable). Node cockpit only holds **computed** margin for the active implementation.

---

## 6. Relative-value / basis analysis (horizons + quartile) — locked

Separate from tracer horizons (`d1/d5/d20/d60`). Used for **RV richness/cheapness vs history**. Quartile/percentile are computed **per series, per horizon** — never pooled across nodes or series.

### 6.1 Series registry (Master DD — storage for `quartile_direction`)

Registered in `data_dictionary.yaml` under `rv_series` (Phase 2 follow-up). Each series is the atomic unit for direction, history, and quartile math.

| Registry field | Type | Description |
|----------------|------|-------------|
| `series_id` | string | Stable key (e.g. `btc_calendar_bt_near_deferred`, `hyg_lqd_ratio`, `hy_oas_proxy`) |
| `node_id` | string | Owning cockpit (`liquidity` \| `credit` \| `breadth` \| `highbeta` \| `basis`) |
| `quartile_direction` | string | **`higher_is_richer`** \| **`higher_is_cheaper`** — locked per series |
| `unit` | string | `bps` \| `pct` \| `ratio` \| `usd` |
| `history_source` | string | `barchart_spread_history` \| `barchart_curve_history` \| `koyfin_dated_series` |
| `history_key` | string | Key into source artifact (e.g. spread symbol, asset pair) |
| `horizons_supported` | array | `[1m, 3m, 6m, 12m, 3y]` — all five required at full build |

**Authoritative catalog:** `whinfell_pipeline/data_dictionary.yaml` → `rv_series.series` (locked June 29, 2026). Seed entries:

| `series_id` | `node_id` | `quartile_direction` | `primary` |
|-------------|-----------|----------------------|-----------|
| `usgg2y10y` | `liquidity` | `higher_is_richer` | yes |
| `sofr_ois_spread` | `liquidity` | `higher_is_cheaper` | no |
| `hy_oas_proxy` | `credit` | `higher_is_cheaper` | yes |
| `hyg_lqd_ratio` | `credit` | `higher_is_richer` | no |
| `iwm_spy_ratio` | `breadth` | `higher_is_richer` | yes |
| `xlf_xlu_relative` | `breadth` | `higher_is_richer` | no |
| `ibit_qqq_beta_spread` | `highbeta` | `higher_is_richer` | yes |
| `btc_spy_corr` | `highbeta` | `higher_is_richer` | no |
| `btc_calendar_bt_near_deferred` | `basis` | `higher_is_richer` | yes |
| `btc_basis_vs_refs` | `basis` | `higher_is_richer` | no |

### 6.2 Per-node cockpit structure (`rv_basis`)

Restructured to nest **series → horizons** (supports multiple RV series per node).

| Field | Type | Required | Source | Description |
|-------|------|----------|--------|-------------|
| `rv_basis` | object | yes | pipeline/derived | Container below |
| `rv_basis.active_horizon` | string | yes | operator | `1m` \| `3m` \| `6m` \| `12m` \| `3y` |
| `rv_basis.active_series_id` | string | yes | operator | Active series for richness panel |
| `rv_basis.series` | object | yes | pipeline | Map of `series_id` → series object |
| `rv_basis.series.{id}.quartile_direction` | string | yes | registry | Copied from Master DD `rv_series` |
| `rv_basis.series.{id}.label` | string | yes | registry | Desk display name |
| `rv_basis.series.{id}.horizons` | object | yes | pipeline/derived | One entry per `1m`/`3m`/`6m`/`12m`/`3y` |
| `rv_basis.series.{id}.horizons.{h}.current_value` | number | yes | pipeline | Latest reading for this series at lookback end |
| `rv_basis.series.{id}.horizons.{h}.unit` | string | yes | registry | From `rv_series.unit` |
| `rv_basis.series.{id}.horizons.{h}.percentile` | number | yes | derived | 0–100 empirical percentile vs **this series'** horizon window |
| `rv_basis.series.{id}.horizons.{h}.quartile` | int | yes | derived | 1–4 from percentile bins (Q1=0–25, Q2=25–50, Q3=50–75, Q4=75–100) |
| `rv_basis.series.{id}.horizons.{h}.richness_label` | string | yes | derived | `cheap` \| `fair` \| `rich` \| `extreme` — see §6.3 |
| `rv_basis.series.{id}.horizons.{h}.lookback_start` | date | yes | pipeline | Horizon window start |
| `rv_basis.series.{id}.horizons.{h}.lookback_end` | date | yes | pipeline | Horizon window end (= `as_of` date) |
| `rv_basis.series.{id}.horizons.{h}.n_observations` | int | no | pipeline | Points in window |
| `rv_basis.series.{id}.horizons.{h}.z_score` | number | no | derived | Optional vs horizon mean/std |
| `rv_basis.richness_label` | string | no | derived | Convenience copy from active series + active horizon |
| `rv_basis.quartile_context` | string | no | derived | One-line desk interpretation for active series/horizon |

**Horizon lookback windows (locked):**

| Key | Calendar lookback |
|-----|-------------------|
| `1m` | 22 trading days |
| `3m` | 63 trading days |
| `6m` | 126 trading days |
| `12m` | 252 trading days |
| `3y` | 756 trading days |

### 6.3 Quartile & percentile calculation (locked algorithm)

Applied **independently** for each `(series_id, horizon)` pair:

1. **Load history** for `series_id` from `history_source` / `history_key`; slice to lookback window `[lookback_start, lookback_end]`.
2. **Percentile** = empirical rank of `current_value` in window: `(count(values ≤ current) / n) × 100`. Standard statistical percentile — higher value → higher percentile. **Not** pooled across nodes or other series.
3. **Quartile** = bin from percentile: Q1 (0–25), Q2 (25–50), Q3 (50–75), Q4 (75–100).
4. **Richness label** = interpret quartile using `quartile_direction`:
   - `higher_is_richer`: Q1→`cheap`, Q2→`fair`, Q3→`rich`, Q4→`extreme`
   - `higher_is_cheaper`: Q4→`cheap`, Q3→`fair`, Q2→`rich`, Q1→`extreme`
5. **Expose** full horizon map per series in hydration; UI toggles `active_horizon` and `active_series_id` without recomputing other series.

**MVP degrade:** If history missing for a horizon, omit that horizon key; cockpit still loads if ≥1 horizon populated for ≥1 series on the node.

**Data sources:** `data/barchart/v1/barchart_spread_history.json`, `barchart_curve_history.json`, Koyfin dated series for ETF ratios.

---

## 7. Component inputs (ticker feed strip)

Lightweight list driving `composite_score` and the ticker feed UI.

| Field | Type | Required | Source | Description |
|-------|------|----------|--------|-------------|
| `component_inputs` | array | yes | pipeline | Ordered list |
| `component_inputs[].asset_id` | string | yes | pipeline | `canonical_assets` key |
| `component_inputs[].label` | string | yes | pipeline | Display label |
| `component_inputs[].value` | number/string | yes | pipeline | Current reading |
| `component_inputs[].unit` | string | no | pipeline | `%`, `bps`, `corr`, etc. |
| `component_inputs[].weight` | number | no | derived | Contribution weight to composite (0–1) |
| `component_inputs[].contribution` | number | no | derived | Weighted score contribution |
| `component_inputs[].direction` | string | no | derived | `up` \| `flat` \| `down` for strip arrow |
| `component_inputs[].as_of` | ISO-8601 | yes | pipeline | Per-input freshness |

**Per-node minimum component count:** 2 (MVP), target 4–6 at full ARCH-1 routing.

---

## 8. Proposed JSON structure

### 8.1 Hydration bundle extension (v1.1.0)

Add top-level block `node_cockpits` — keyed by `node_id`. Existing v1.0.0 blocks (`global`, `china`, `suggested_tracer`, etc.) remain unchanged.

```json
{
  "hydration_version": "1.1.0",
  "bundle_version": "1.1.0",
  "snapshot_id": "global-2026-06-27-koyfin-01",
  "as_of": "2026-06-27T14:00:00+00:00",
  "freshness_status": "aging",
  "global": { },
  "suggested_tracer": { },
  "node_cockpits": {
    "liquidity": { },
    "credit": { },
    "breadth": { },
    "highbeta": { },
    "basis": { }
  },
  "cockpit_context": {
    "transmission_health_score": 63,
    "transmission_state": "stressed",
    "weakest_node_id": "credit",
    "gate_zone": "amber",
    "whinfell_score": 58
  }
}
```

`cockpit_context` is optional shared metadata — nodes must still carry their own `is_weakest_link` flag.

### 8.2 Single node template (complete minimum)

```json
{
  "node_id": "basis",
  "display_name": "Basis & Term Structure",
  "composite_score": 42,
  "composite_score_source": "weighted_components",
  "band": "Fragile",
  "band_key": "fragile",
  "freshness_status": "fresh",
  "as_of": "2026-06-27T14:00:00+00:00",
  "horizon_marks": { "d1": "flat", "d5": "flat", "d20": "down", "d60": "flat" },
  "horizon_net": -1,
  "is_weakest_link": false,
  "china_parallel": {
    "present": true,
    "stage_id": "basis",
    "stage_name": "Basis & Term Structure",
    "horizon_marks": { "d1": "flat", "d5": "flat", "d20": "down", "d60": "flat" },
    "horizon_net": -1,
    "note": "China basis stage aligned with global calendar read"
  },
  "key_observation": "Calendar rich vs 3Y median; 20D trend deteriorating.",
  "confidence": "medium",
  "gate_interaction": {
    "zone": "amber",
    "blocks_directional": false,
    "blocks_rv": false,
    "note": "Health below 70 — size_hint capped at half."
  },
  "component_inputs": [
    {
      "asset_id": "btc_near_contract",
      "label": "BT near-deferred",
      "value": 1.25,
      "unit": "pct",
      "weight": 0.4,
      "contribution": -8,
      "direction": "down",
      "as_of": "2026-06-27T14:00:00+00:00"
    },
    {
      "asset_id": "btc_vehicle_ibit",
      "label": "IBIT vs SPY beta",
      "value": 1.8,
      "unit": "ratio",
      "weight": 0.3,
      "contribution": -4,
      "direction": "flat",
      "as_of": "2026-06-27T14:00:00+00:00"
    }
  ],
  "directional": {
    "posture": "neutral",
    "conviction": "low",
    "rationale": "Calendar rich but gate caps directional beta.",
    "horizon": "20d",
    "invalidation": "Spread < 0.75% with health > 70",
    "size_hint": "half",
    "blocked": false,
    "block_reason": ""
  },
  "relative_value": {
    "posture": "short_spread",
    "structure": "BT near vs deferred calendar",
    "conviction": "medium",
    "rationale": "Q4 richness on 3M lookback; fade contango extension.",
    "leg_long": "btc_deferred_contract",
    "leg_short": "btc_near_contract",
    "hedge_ratio": 1.0,
    "target": "Q2 median (0.95%)",
    "stop": "New 3M high + 15 bps",
    "blocked": false,
    "block_reason": ""
  },
  "implementations": [
    {
      "id": "basis_btc_calendar",
      "instrument_class": "futures",
      "label": "BT calendar spread",
      "legs": [
        { "side": "long", "asset_id": "btc_deferred_contract", "vendor_ticker": "BTQ26", "ratio": 1 },
        { "side": "short", "asset_id": "btc_near_contract", "vendor_ticker": "BTM26", "ratio": 1 }
      ],
      "liquidity_tier": "institutional",
      "margin_profile": "cme_btc",
      "rank": 1
    },
    {
      "id": "basis_ibit_proxy",
      "instrument_class": "etf",
      "label": "IBIT warehouse proxy",
      "legs": [
        { "side": "long", "asset_id": "btc_vehicle_ibit", "vendor_ticker": "IBIT", "ratio": 1 }
      ],
      "liquidity_tier": "institutional",
      "margin_profile": "ibkr_etf",
      "rank": 2
    }
  ],
  "selected_implementation_id": null,
  "sizing": {
    "enabled": false,
    "portfolio_nav_usd": null,
    "risk_budget_bps": 25,
    "kelly_fraction": 0.25,
    "max_notional_usd": null,
    "recommended_notional_usd": null,
    "contracts_or_shares": null,
    "margin": null
  },
  "rv_basis": {
    "active_horizon": "3m",
    "active_series_id": "btc_calendar_bt_near_deferred",
    "richness_label": "extreme",
    "quartile_context": "BT calendar Q4 (82nd pct) — higher_is_richer",
    "series": {
      "btc_calendar_bt_near_deferred": {
        "quartile_direction": "higher_is_richer",
        "label": "BT near-deferred calendar",
        "horizons": {
          "1m": {
            "current_value": 1.25,
            "unit": "pct",
            "percentile": 78,
            "quartile": 4,
            "richness_label": "rich",
            "lookback_start": "2025-05-27",
            "lookback_end": "2026-06-27",
            "n_observations": 22,
            "z_score": 1.1
          },
          "3m": {
            "current_value": 1.25,
            "unit": "pct",
            "percentile": 82,
            "quartile": 4,
            "richness_label": "extreme",
            "lookback_start": "2025-03-27",
            "lookback_end": "2026-06-27",
            "n_observations": 63,
            "z_score": 1.3
          },
          "6m": {
            "current_value": 1.25,
            "unit": "pct",
            "percentile": 71,
            "quartile": 3,
            "richness_label": "rich",
            "lookback_start": "2025-12-27",
            "lookback_end": "2026-06-27",
            "n_observations": 126
          },
          "12m": {
            "current_value": 1.25,
            "unit": "pct",
            "percentile": 65,
            "quartile": 3,
            "richness_label": "rich",
            "lookback_start": "2025-06-27",
            "lookback_end": "2026-06-27",
            "n_observations": 252
          },
          "3y": {
            "current_value": 1.25,
            "unit": "pct",
            "percentile": 58,
            "quartile": 3,
            "richness_label": "rich",
            "lookback_start": "2023-06-27",
            "lookback_end": "2026-06-27",
            "n_observations": 756
          }
        }
      }
    }
  }
}
```

### 8.3 Transmission Control local state extension

Persist operator edits separately from hydration (Master DD `transmission_control_state` v6 → v7 in Phase 2):

```json
{
  "version": 7,
  "node_cockpit_overrides": {
    "basis": {
      "selected_implementation_id": "basis_btc_calendar",
      "sizing": { "enabled": true, "portfolio_nav_usd": 5000000, "kelly_fraction": 0.25 },
      "rv_basis": { "active_horizon": "6m" },
      "directional": { "posture": "neutral", "rationale": "Operator note…" }
    }
  }
}
```

Merge rule: `hydration node_cockpits.*` ⊕ `local node_cockpit_overrides.*` → rendered cockpit. Operator fields win on conflict.

### 8.4 WTM EXPORT v2.2 per-node block (sketch)

One block per node for Perplexity round-trip:

```
--- NODE COCKPIT: Basis & Term Structure ---
Node ID: basis
Composite Score: 42
Band: Fragile
Horizon Net: -1
Horizon Marks: d1→ d5→ d20↓ d60→
Directional: neutral (low) — Calendar rich but gate caps directional beta.
Relative Value: short_spread — BT near vs deferred calendar (medium)
Selected Implementation: basis_btc_calendar
RV Series: btc_calendar_bt_near_deferred | Direction: higher_is_richer
RV Horizon: 3m | Quartile: Q4 | Percentile: 82 | Richness: extreme
Composite Score Source: weighted_components
Key Observation: Calendar rich vs 3Y median; 20D trend deteriorating.
```

---

## 9. Minimum viable cockpit (MVP checklist)

A node is **cockpit-ready** when these are non-empty:

| Section | MVP required fields |
|---------|---------------------|
| Signal | `composite_score`, `composite_score_source`, `band`, `freshness_status`, `horizon_marks`, `key_observation`, `component_inputs` (≥2 preferred; fallback via `horizon_net`) |
| Directional | `posture`, `conviction`, `rationale`, `blocked` |
| Relative value | `posture`, `structure`, `conviction`, `rationale` |
| Implementation | `implementations` (≥1; ETF/futures/combination only — no options in MVP) |
| Sizing | `sizing.enabled`, `sizing.kelly_fraction` (defaults OK) |
| RV / Basis | `rv_basis.active_horizon`, `rv_basis.active_series_id`, ≥1 series with ≥1 populated horizon; each series carries `quartile_direction` |
| China (optional) | `china_parallel` may be absent; cockpit valid without it |

---

## 10. Data lineage and ownership

| Data | Producer | Consumer |
|------|----------|----------|
| `component_inputs`, `rv_basis.series` | Pipeline (ARCH-1 + Barchart history + `rv_series` registry) | TC cockpit render |
| `china_parallel` | Pipeline (`china_ladder` block) | TC display only — no gate override |
| `directional`, `relative_value` (initial) | Pipeline derived rules | TC display; operator may override |
| `implementations` | Pipeline catalog per `node_id` | TC picker |
| `sizing`, `selected_implementation_id` | Operator | TC + export |
| `horizon_marks` (initial) | `suggested_tracer` → Accept flow | Node signal sync |

---

## 11. Master DD registration (Phase 2 follow-up)

When this model is locked, register in `data_dictionary.yaml`:

- `json_structures.hydration_bundle.expected_version: "1.1.0"`
- `json_structures.hydration_bundle.blocks.node_cockpits`
- `json_structures.hydration_bundle.blocks.cockpit_context`
- `rv_series` — per-series registry with `quartile_direction`, `node_id`, `history_source`
- `transmission_control_state.current_version: 7`
- `wtm_export.format: "WTM EXPORT v2.2"` with `node_cockpit_block` template

**Not in scope for this document:** UI layout, ARCH-1 implementation, margin default table population, options picker (Phase 2b).

---

## 12. Remaining ambiguities (resolve before implementation)

| # | Topic | Question | Proposed default |
|---|-------|----------|------------------|
| A | **Score docs per node** | ✅ **Locked** — `04_Score_Calculation/Phase2_Interim_Node_Score_Weights.md` + `node_score_weights` in Master DD. Credit remains C1 authoritative. | Promote to full v1.0 docs post-MVP. |
| B | **`rv_series` catalog** | ✅ **Locked** — `rv_series` block in `data_dictionary.yaml` (10 series, all five nodes). | Extend via YAML only; no ad-hoc series IDs in pipeline. |
| C | **History granularity** | Barchart history is daily; 1M window = 22 trading days — confirm desk uses calendar vs trading-day count. | Trading-day count (locked in §6.2); flag if Koyfin series differ. |
| D | **Multiple active series** | When a node has 2+ RV series (e.g. credit: OAS + HYG/LQD), which drives `relative_value.rationale`? | Primary series per node in `rv_series.primary: true`; operator can switch `active_series_id`. |
| E | **Fallback threshold** | How many `component_inputs` required before switching from weighted score to `horizon_net_fallback`? | Locked: **< 2 components** triggers fallback (see §1). |
| F | **WTM EXPORT v2.2** | Per-node export must include `quartile_direction` + active series/horizon — field list not yet written. | Blueprint deliverable; blocked on this doc lock. |

---

**Next step:** Register `rv_series` in Master DD · Blueprint locks WTM EXPORT v2.2 · Bridge drafts `node_cockpits` builder · Clarity wireframes Liquidity cockpit.

**Locked decisions applied:** BUILD Cousins · June 29, 2026