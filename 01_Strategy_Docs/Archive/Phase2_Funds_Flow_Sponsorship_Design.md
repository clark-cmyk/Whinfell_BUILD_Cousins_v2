# Phase 2 — Funds Flow Sponsorship Layer

**Version:** 1.0 (design locked for implementation)  
**Date:** June 29, 2026  
**Authors:** BUILD Cousins (Blueprint + Bridge + Clarity)  
**Status:** Approved — implementation detail in [Phase2_Flows_Implementation_Spec.md](Phase2_Flows_Implementation_Spec.md)
**Prerequisites:** [Phase2_Node_Cockpit_Data_Model.md](Phase2_Node_Cockpit_Data_Model.md) v0.2, hydration bundle v1.1.0, Master Data Dictionary v1.0

---

## Understanding confirmed

Whinfell Transmission Control is a **regime-first** operator console. Score, transmission, gate, shock, and freshness remain the **primary control authority**. Node cockpits are evolving into self-contained trading workspaces.

The Funds Flow Sponsorship layer adds a **confirmation and conviction subsystem** inside each node cockpit. It answers three questions in under two seconds:

1. Is there allocator sponsorship?
2. Is it persistent (not just a 1D impulse)?
3. Does it confirm or contradict the node verdict?

Flows use **% AUM** as the canonical cross-ETF normalization. Raw USD is retained in the data model but subordinate in UI and interpretation logic.

**Flows never override** score / transmission / gate unless the desk explicitly enables that later.

---

## Design recommendation (concise)

| Decision | Choice |
|----------|--------|
| Authority tier | **Confirmation layer** — affects `confidence`, rationale, divergence flags, “what would change my mind” |
| Normalization | **`flow_pct_aum`** primary; `flow_usd` optional / hidden by default |
| Horizons shown | **1D + 5D cumulative** in UI; 20D used for `persistence_score` only |
| Placement | **Right rail** below driver checklist / trigger map (`FundsFlowSponsorshipCard`) |
| Architecture | Reusable **node-level module**: raw → aggregate → verdict → view model |
| Phase placement | **Phase 2b** — data contract + pipeline in 2b-data; UI card with Phase 2 cockpit UI (before Phase 3 polish) |

---

## Theoretical justification

### UI / information design

- **Signal hierarchy:** Command bar and gate state stay fixed at the top; flows are visually subordinate (smaller type, neutral palette, no heatmaps).
- **Progressive disclosure:** Card shows verdict + aggregate + 3–5 ETF rows; sparklines are optional secondary cues.
- **Visual calm:** Tabular numerals, right-aligned values, low-opacity intensity bars only for extremes or primary ETF.
- **Decision support:** Operator reads sponsorship as *evidence*, not permission.

### Finance / microstructure

- ETF flows proxy **allocator demand** when normalized as % AUM.
- **1D is noisy** — always pair with **5D cumulative** to separate impulse from persistence.
- **Node-specific baskets** — Liquidity flows (duration ETFs) ≠ Credit flows (HY/IG) ≠ High-Beta (IBIT/QQQ).
- Framing is **confirm / contradict**, not “inflow good / outflow bad.”
- **Divergence** (price or RV improving while flows weak/negative) reduces conviction.

### Computer science / systems

- **Deterministic transforms** — stable thresholds → stable labels → exportable rationale.
- **Separation of concerns** — `funds_flow_inputs` (raw) → `funds_flows` (computed) → `FundsFlowSponsorshipCard` (render).
- **State compatibility** — block lives on `node_cockpit.funds_flows`; preserved across node flip and compare mode.
- **Graceful degrade** — missing flow columns → `enabled: false`; cockpit remains valid.

---

## Data model

### Extension to `node_cockpit`

Add optional block `funds_flows` on each cockpit object in hydration bundle v1.2.0 (backward-compatible with v1.1.0).

```json
{
  "funds_flows": {
    "enabled": true,
    "source": "pipeline",
    "as_of": "2026-06-29",
    "horizon_display": "5d",
    "basket_id": "credit_hy_ig",
    "basket_label": "Credit ETF Sponsorship",
    "aggregate": {
      "flow_pct_aum_1d": 0.12,
      "flow_pct_aum_5d": 0.46,
      "positive_count": 3,
      "total_count": 4,
      "verdict": "supportive",
      "confidence_delta": 1,
      "concentration_flag": false
    },
    "etfs": [
      {
        "ticker": "HYG",
        "asset_id": "hyg",
        "role": "hy_high_yield",
        "primary": true,
        "flow_pct_aum_1d": 0.08,
        "flow_pct_aum_5d": 0.31,
        "flow_usd_1d": null,
        "flow_usd_5d": null,
        "persistence_score": 0.67
      }
    ],
    "interpretation": {
      "supports_node_thesis": true,
      "divergence_flag": false,
      "summary": "Flows confirm spread stabilization.",
      "caution_line": "",
      "change_mind_trigger": "5D aggregate turns negative while RV still rich."
    }
  }
}
```

### Field notes

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| `enabled` | bool | pipeline | `false` when inputs missing |
| `horizon_display` | string | default | UI default tab: `5d` |
| `basket_id` | string | registry | Stable key in Master DD |
| `aggregate.verdict` | enum | derived | `supportive` \| `neutral` \| `mixed` \| `diverging` |
| `aggregate.confidence_delta` | int | derived | `-1`, `0`, `+1` — applied to node `confidence` tier |
| `aggregate.concentration_flag` | bool | derived | True when one ETF > 70% of signed 5D flow |
| `etfs[].persistence_score` | number 0–1 | derived | Share of last 20 sessions with same sign as 5D |
| `interpretation.change_mind_trigger` | string | derived | Feeds “What would change my mind” |

### Master DD registry (`funds_flow_baskets`)

Register in `data_dictionary.yaml`:

```yaml
funds_flow_baskets:
  version: "1.0"
  status: Locked
  normalization: flow_pct_aum
  horizons:
    display: [1d, 5d]
    persistence_lookback_sessions: 20
  nodes:
    liquidity:
      basket_id: liquidity_duration
      basket_label: "Duration & front-end sponsorship"
      primary_ticker: IEF
      etfs:
        - {ticker: SHY, asset_id: shy, role: front_end, primary: false, weight: 0.2}
        - {ticker: IEF, asset_id: ief, role: intermediate_duration, primary: true, weight: 0.35}
        - {ticker: TLT, asset_id: tlt, role: long_duration, primary: false, weight: 0.25}
        - {ticker: BIL, asset_id: bil, role: t_bill, primary: false, weight: 0.2}
    credit:
      basket_id: credit_hy_ig
      basket_label: "Credit ETF sponsorship"
      primary_ticker: HYG
      etfs:
        - {ticker: HYG, asset_id: hyg, role: hy_high_yield, primary: true, weight: 0.35}
        - {ticker: LQD, asset_id: jaaa, role: ig_investment_grade, primary: false, weight: 0.30}
        - {ticker: BKLN, asset_id: bkln, role: leveraged_loan, primary: false, weight: 0.20}
        - {ticker: CWB, asset_id: cwb, role: convertibles, primary: false, weight: 0.15}
    breadth:
      basket_id: breadth_participation
      basket_label: "Equity participation sponsorship"
      primary_ticker: IWM
      etfs:
        - {ticker: IWM, asset_id: iwm, role: small_cap, primary: true, weight: 0.35}
        - {ticker: SPY, asset_id: spy, role: large_cap, primary: false, weight: 0.25}
        - {ticker: QQQ, asset_id: qqq, role: growth_tech, primary: false, weight: 0.20}
        - {ticker: RSP, asset_id: rsp, role: equal_weight, primary: false, weight: 0.20}
    highbeta:
      basket_id: highbeta_crypto_beta
      basket_label: "High-beta & crypto vehicle sponsorship"
      primary_ticker: IBIT
      etfs:
        - {ticker: IBIT, asset_id: btc_vehicle_ibit, role: btc_spot_vehicle, primary: true, weight: 0.40}
        - {ticker: QQQ, asset_id: qqq, role: growth_beta, primary: false, weight: 0.30}
        - {ticker: SPY, asset_id: spy, role: market_beta, primary: false, weight: 0.20}
        - {ticker: BITO, asset_id: bito, role: btc_futures_vehicle, primary: false, weight: 0.10}
    basis:
      basket_id: basis_warehouse_proxy
      basket_label: "Warehouse / ETF basis proxy sponsorship"
      primary_ticker: IBIT
      etfs:
        - {ticker: IBIT, asset_id: btc_vehicle_ibit, role: primary_warehouse, primary: true, weight: 0.50}
        - {ticker: BITO, asset_id: bito, role: futures_linked, primary: false, weight: 0.25}
        - {ticker: GBTC, asset_id: gbtc, role: trust_proxy, primary: false, weight: 0.25}
```

**Basis node note:** Futures calendar trades have no AUM; IBIT/BITO/GBTC flows proxy **warehouse demand** sponsoring basis expression.

### Raw input contract (`funds_flow_inputs`)

Sidecar or columns from Koyfin `WTM-Credit-Confirmation` / dedicated `WTM-Flows` export:

| Column pattern | Maps to |
|----------------|---------|
| `{TICKER} Flow (D)` | `flow_usd_1d` |
| `{TICKER} AUM` | denominator for `% AUM` |
| `{TICKER} Flow % AUM (D)` | preferred if present |

Pipeline computes 5D cumulative from last 5 sessions when daily rows available.

---

## Node ETF mapping summary

| `node_id` | Primary ETF | Why | Aggregate method |
|-----------|-------------|-----|------------------|
| `liquidity` | **IEF** | Intermediate duration is the cleanest “rates risk-on/off” flow read | Weighted mean of 1D/5D `% AUM` using basket weights |
| `credit` | **HYG** | HY ETF flows directly sponsor spread trades | Weighted mean; breadth = count of positive 5D |
| `breadth` | **IWM** | Small-cap participation vs cap-weight | Weighted mean; flag when IWM 5D negative but SPY positive |
| `highbeta` | **IBIT** | BTC vehicle flow = high-beta transmission sponsor | Weighted mean; IBIT gets 2× weight in concentration check |
| `basis` | **IBIT** | Warehouse ETF flow proxies futures basis demand | Primary-led: 60% IBIT + 40% basket mean |

---

## Interpretation algorithm (deterministic)

Constants (desk-tunable in YAML):

```yaml
thresholds:
  supportive_5d_pct: 0.15      # +0.15% AUM cumulative 5D on aggregate
  weak_5d_pct: 0.05            # below = weak sponsorship
  divergence_5d_pct: -0.05     # negative 5D while node bullish
  breadth_supportive_ratio: 0.60 # 60%+ ETFs positive 5D
  concentration_single_etf: 0.70 # one ETF > 70% of signed flow
```

### Step 1 — Aggregate

```
agg_1d = Σ(weight_i × flow_pct_aum_1d_i)
agg_5d = Σ(weight_i × flow_pct_aum_5d_i)
positive_count = count(etf where flow_pct_aum_5d > 0)
breadth_ratio = positive_count / total_count
```

### Step 2 — Base verdict (flow-only)

| Condition | Verdict |
|-----------|---------|
| `agg_5d >= supportive_5d` AND `breadth_ratio >= 0.60` | `supportive` |
| `agg_5d <= divergence_5d` OR (`agg_1d > 0` AND `agg_5d < 0`) | `mixed` |
| `abs(agg_5d) < weak_5d` | `neutral` |
| else | `neutral` |

### Step 3 — Divergence overlay (node context)

Compare against node `directional.posture` and `relative_value.posture`:

| Node signal | Flow read | Result |
|-------------|-----------|--------|
| Bullish directional OR long_spread RV | `agg_5d < divergence_5d` OR (`agg_5d < weak_5d` AND node conviction ≥ medium) | **`diverging`** |
| Bearish / short_spread | Strong positive 5D inflows | **`mixed`** (flows contradict bearish read) |
| Neutral | Any | Keep flow-only verdict |

### Step 4 — Confidence delta

| Verdict | `confidence_delta` |
|---------|-------------------|
| `supportive` + agrees with node | `+1` |
| `neutral` | `0` |
| `mixed` | `0` |
| `diverging` | `-1` |

Apply: bump node `confidence` tier (low → medium → high) with clamp. **Never** change `composite_score` or gate.

### Step 5 — Narrative

- `summary` — one line from template keyed by verdict + primary ETF sign
- `caution_line` — set when `diverging` or `concentration_flag`
- `change_mind_trigger` — opposite-flow condition vs current node posture

---

## Component: `FundsFlowSponsorshipCard`

### Placement

**Primary:** Right-side rail, below driver checklist / trigger map, above sizing (when enabled).

**Secondary (compact):** Below Relative Value chart band — `variant: "compact"` hides ETF rows, shows verdict + aggregate only.

### Structure (desktop)

```
┌ Funds Flow Sponsorship ──────────────┐
│ Supportive                    [badge]│
│ 1D +0.12% AUM · 5D +0.46% · 3/4 pos │
├──────────────────────────────────────┤
│ HYG *   +0.08%   +0.31%   ▂▄▅▆      │
│ LQD       +0.02%   +0.09%   ▂▃▄     │
│ BKLN      +0.01%   +0.04%   ▁▂▂     │
├──────────────────────────────────────┤
│ Flows confirm spread stabilization.  │
│ ⚠ Price improving faster than flows. │  (optional)
└──────────────────────────────────────┘
```

### Visual rules

- Font size one step below node verdict
- Verdict badge: muted green / amber / gray only — no saturated red blocks
- Numbers: `font-variant-numeric: tabular-nums`; right-aligned
- Primary ETF: subtle left border or `*` marker
- Sparklines: 20D, 24px height, 15% opacity fill

### Compare mode

- One card per compared node, synchronized `horizon_display`
- Same width as single-node card; stack vertically in compare rail
- Verdict badges align horizontally for scan

### Flip mode

- Card content swaps with node; **no layout reflow** — fixed height container
- Fade transition ≤ 150ms

### Full-screen “Here’s Why”

- Expand interpretation + `change_mind_trigger` + ETF table
- Hide sparklines in fullscreen text-first layout
- Flows section titled **“Allocator sponsorship (confirming evidence)”** — explicitly subordinate

---

## Implementation sketch

### Pipeline (`whinfell_pipeline/funds_flows.py`)

```python
def build_funds_flows(
    node_id: str,
    *,
    flow_inputs: Mapping[str, Any],
    node_cockpit: Mapping[str, Any],
    as_of: datetime,
) -> dict[str, Any]:
    basket = load_basket(node_id)
    etfs = [compute_etf_row(spec, flow_inputs) for spec in basket["etfs"]]
    aggregate = compute_aggregate(etfs, basket)
    verdict = assign_verdict(aggregate, node_cockpit)
    interpretation = build_interpretation(verdict, aggregate, node_cockpit)
    return {
        "enabled": True,
        "as_of": as_of.date().isoformat(),
        "basket_id": basket["basket_id"],
        "basket_label": basket["basket_label"],
        "aggregate": {**aggregate, "verdict": verdict, "confidence_delta": confidence_delta(verdict)},
        "etfs": etfs,
        "interpretation": interpretation,
    }
```

Wire in `node_cockpits.build_node_cockpit()` after directional/RV computed.

### UI (`FundsFlowSponsorshipCard.js` or TC inline module)

```javascript
function renderFundsFlowSponsorshipCard(cockpit, { variant = 'rail' } = {}) {
  const ff = cockpit.funds_flows;
  if (!ff?.enabled) return renderDisabledPlaceholder();
  return el('.ff-sponsorship-card', [
    header('Funds Flow Sponsorship', ff.aggregate.verdict),
    aggregateLine(ff.aggregate),
    ...ff.etfs.slice(0, 5).map(renderEtfRow),
    interpretationBlock(ff.interpretation),
  ]);
}
```

### WTM EXPORT v2.3 (optional extension)

Per-node line block (append to v2.2):

```
Funds Flow Verdict: supportive
Funds Flow 5D: +0.46% AUM (3/4 positive)
Funds Flow Summary: Flows confirm spread stabilization.
```

---

## WTM export & Master DD additions

| Artifact | Change |
|----------|--------|
| `data_dictionary.yaml` | `funds_flow_baskets`, `funds_flow_thresholds`, column map `{TICKER} Flow (D)` |
| `json_structures.hydration_bundle` | `expected_version: 1.2.0`; `node_cockpits.*.funds_flows` |
| `Phase2_Node_Cockpit_Data_Model.md` | §9 MVP checklist + `funds_flows` optional block |
| `WTM_EXPORT_v2.2_SPEC.md` | Optional v2.3 addendum for flow lines |
| `collection_manifest.yaml` | Optional `WTM-Flows` or flow columns on credit export |

---

## Compare / flip / fullscreen behavior

| Mode | Behavior |
|------|----------|
| Sequential flip | Card swaps with `node_cockpit`; fixed rail slot; 150ms fade |
| Compare | N cards (N = compared nodes); shared horizon; no animated charts |
| Full-screen Why | Expanded narrative; sponsorship section below node rationale |
| State persistence | `funds_flows` hydrated from bundle; operator cannot override flows (read-only) |

---

## Key Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Flows = confirmation layer only | Preserves regime-first hierarchy |
| 2 | `% AUM` canonical | Cross-ETF comparability |
| 3 | 1D + 5D display | Impulse vs persistence |
| 4 | Node-specific baskets in Master DD | No ad-hoc ETF rows in UI |
| 5 | Deterministic thresholds in YAML | Stable rationale + export |
| 6 | Phase 2b placement | Data can ship before full cockpit UI; card ships with cockpit rail |
| 7 | Basis uses ETF warehouse proxy | Futures lack AUM; IBIT is best sponsor signal |
| 8 | `confidence_delta` not score delta | Conviction tier only — no gate override |

---

## Open Questions

| # | Question | Status / default |
|---|----------|------------------|
| 1 | **Flow ingest path** — see [Funds_Flow_Ingest_Arena_Debate.md](../08_Deliverables/Funds_Flow_Ingest_Arena_Debate.md) | **BUILD recommends Option D (hybrid):** primary `WTM-Flows` → `flows_{YYYYMMDD}_{HHMM}.csv`; fallback cross-section `Fund Flows/Periodic (D)` for Credit 1D only. **Team vote pending.** |
| 2 | Add `GBTC`, `BITO`, `RSP`, `SHY`, `BIL` to `canonical_assets`? | Yes in PR-1 registry |
| 3 | Desk threshold tuning UI? | YAML-only for MVP |
| 4 | Flow/AUM units (millions USD)? | Sanity check on HYG row in `WTM-Flows-Global.csv`; desk confirm |

### Why not credit-only ingest?

Staged `credit_*.csv` after 2.2e transform is **WTM observation** format — no flow columns. Raw cross-section credit exports have `Fund Flows/Periodic (D)` + `AUM` but **no dated history** in the daily chain, so **5D cumulative % AUM cannot be computed** without a separate time-series source.

**Desk evidence (Jun 29):** `WTM-Flows-Global.csv` dropped to `whinfell_drop` — correct column shape, **quarantined** for filename (`flows_{YYYYMMDD}_{HHMM}.csv` required). File covers SPY/HYG/LQD/JAAA/BKLN/MCHI only; view must expand for full node baskets.

---

## PR Plan

### PR-1: Master DD + flow basket registry
- **Files:** `data_dictionary.yaml`, `data_dictionary.py` helpers, `test_data_dictionary.py`
- **Deps:** None
- **Changes:** `funds_flow_baskets`, thresholds, column patterns, canonical assets for new tickers

### PR-2: `funds_flows.py` builder + node cockpit wire-up
- **Files:** `whinfell_pipeline/funds_flows.py`, `node_cockpits.py`, `tests/test_funds_flows.py`
- **Deps:** PR-1
- **Changes:** Aggregate/verdict/interpretation; attach `funds_flows` to each cockpit; bump bundle to v1.2.0

### PR-3: Flow input ingest from Koyfin CSV
- **Files:** `raw_csv_transform.py` or `koyfin_adapter.py`, `collection_manifest.yaml`
- **Deps:** PR-1
- **Changes:** Parse `Flow (D)` / `AUM` columns → `funds_flow_inputs` sidecar

### PR-4: `FundsFlowSponsorshipCard` TC component
- **Files:** `Whinfell_Transmission_Control.html` (or extracted module), CSS
- **Deps:** PR-2
- **Changes:** Right-rail card, compare variant, fullscreen section

### PR-5: WTM EXPORT flow lines + docs
- **Files:** `export_contract.py`, `WTM_EXPORT_v2.2_SPEC.md` or v2.3 addendum, strategy docs
- **Deps:** PR-2, PR-4
- **Changes:** Export/import flow verdict lines; update phased plan

---

**Recommendation:** Ship **PR-1 + PR-2 + PR-3** as Phase **2b-data** (pipeline-ready, UI stub). Ship **PR-4 + PR-5** with Phase **2 cockpit UI** — not Phase 3 polish.