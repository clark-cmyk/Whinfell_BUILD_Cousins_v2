# Phase 2 — Transmission Control Cockpit UI Architecture

**Version:** 1.0 (lock candidate)  
**Date:** June 29, 2026  
**Authors:** BUILD Cousins (Clarity + Blueprint + Bridge)  
**Status:** Draft for desk lock — concrete definitions before TC implementation  
**Companion to:** [Phase2_Node_Cockpit_Data_Model.md](Phase2_Node_Cockpit_Data_Model.md) (JSON fields) · [Whinfell_Cockpit_UI_Interaction_Standard.md](Whinfell_Cockpit_UI_Interaction_Standard.md) (behavioral contract)

---

## Confirmation — direction understood

**Phase 2 goal:** Each of the five ladder nodes is a **self-contained trading cockpit** inside one stable Transmission Control shell — not five separate pages.

**AI-first cockpit principle (locked):**

> Deliver maximum reasoning quality and contextual intelligence with **minimum** compute, latency, token spend, and UI redraws.

**Operational rules:**

| Rule | Implementation |
|------|----------------|
| Structured data first | Hydration bundle + `node_cockpits.*` are the reasoning substrate; UI reads JSON, does not re-infer scores/verdicts |
| Compute once per session | Quartiles, composites, `funds_flows` verdicts computed in **pipeline at hydrate**; client toggles horizons/series only |
| No redundant AI | Do not call LLM for values already in hydration (band, quartile, flows_meta, gate) |
| Targeted AI only | LLM reserved for: operator-authored rationale polish, export narrative, optional “challenge thesis” — never for percentile math |
| Stable shell, swap payload | Node flip changes **data bound to fixed regions**; no layout reflow |
| Degrade as data | `flows_meta`, freshness, provenance gaps render as **interaction signals** — never styled as neutral (see Interaction Standard) |

---

## 1. Navigation model — Barchart-style risk curve

### 1.1 Node rail (canonical order)

Horizontal risk curve left → right (canonical `node_id`):

```
liquidity → credit → breadth → highbeta → basis
```

| Key | `node_id` | Rail label |
|-----|-----------|------------|
| `1` | `liquidity` | Liquidity & Rates |
| `2` | `credit` | Credit |
| `3` | `breadth` | Breadth |
| `4` | `highbeta` | High-Beta / BTC |
| `5` | `basis` | Basis |

**Note:** Desk may say “Cyclical”; canonical ID remains `highbeta` per Master DD.

### 1.2 Rail chrome (persistent)

Each tab shows **without opening the node**:

| Indicator | Source |
|-----------|--------|
| Band color | `node_cockpit.band_key` |
| Weakest-link dot | `node_cockpit.is_weakest_link` |
| Freshness dot | `node_cockpit.freshness_status` |
| Flows degrade chip (when present) | `node_cockpit.funds_flows.flows_meta.flows_status` ≠ `ok` |
| Composite score (compact) | `node_cockpit.composite_score` |

Rail is **always visible** in node cockpit view and in full-screen “Here’s Why”.

### 1.3 Keyboard bindings (locked)

| Input | Action |
|-------|--------|
| `←` / `→` | Previous / next node on risk curve (wrap optional — default **no wrap**) |
| `1`–`5` | Jump to node by index |
| `Esc` | Exit full-screen focus → restore pre-focus shell state |
| `c` | Toggle Compare Mode (when focus off) |
| `f` | Toggle full-screen “Here’s Why” for active node |
| `?` | Keyboard cheat sheet overlay (non-modal, dismiss on Esc) |

Focus trap: when full-screen active, `←`/`→` flip **nodes inside focus**; `Esc` exits focus only.

### 1.4 View modes

| Mode | `navigation.view_mode` | Behavior |
|------|------------------------|----------|
| **Sequential Flip** | `flip` | One active node; rail + shell stable; chart/rail bind to `active_node_id` |
| **Compare** | `compare` | 2–3 selected nodes (`compare_node_ids[]`); stacked compact cockpit cards; shared `compare_horizon` for RV |

Default on load: `flip`, `active_node_id` = `cockpit_context.weakest_node_id` or last session value.

### 1.5 State persistence on flip (locked)

**Preserved globally (session):**

| Key | Persists across node flip |
|-----|---------------------------|
| `navigation.view_mode` | yes |
| `navigation.active_node_id` | updates on flip |
| `navigation.compare_node_ids` | yes in compare mode |
| `navigation.focus_mode` | yes until Esc |
| `chart.shared_horizon` | yes — `rv_basis.active_horizon` default for new node unless node override exists |
| `chart.shared_series_preference` | yes — if target node has same `series_id`, keep selection |
| `chart.zoom_range` | yes — x-axis window (date range) preserved when series shares time axis |
| `chart.y_scale_mode` | yes — `auto` \| `fixed` per session |
| `panel.expanded_sections` | per-node map — restoring when returning to node |

**Reset on flip (never preserved):**

- Scroll position inside node-specific detail band (restore from `panel.scroll_positions[node_id]`)
- Transient tooltips / hover states

**Storage:** `localStorage` key `whinfell_transmission_control_v7` → `navigation` + `chart` + `panel` blocks (see Data Model §13).

### 1.6 Compare mode rules

- Select nodes via rail **long-press** or checkbox affordance (max **3** nodes).
- Each compare card shows: band, composite, directional one-liner, RV active quartile line, `flows_meta` chip if degraded.
- Missing node data → explicit “unavailable” strip — **not** empty neutral card (Interaction Standard).
- Compare does **not** open full-screen; operator must exit compare to enter “Here’s Why”.

---

## 2. Full-screen “Here’s Why” focus mode

### 2.1 Entry / exit

| Action | Result |
|--------|--------|
| `f` or “Here’s Why” control | `navigation.focus_mode: true`, `focus_node_id = active_node_id` |
| `Esc` | `focus_mode: false`; restore scroll, horizon, implementation selection |

**Not a modal** — replaces main content region below global regime band; rail remains.

### 2.2 Information architecture (top → bottom)

| Zone | Content | Primary sources |
|------|---------|-----------------|
| **Thesis header** | Band, composite, confidence, gate note | `node_cockpit` core |
| **Directional block** | Posture, conviction, rationale, invalidation | `directional.*` |
| **RV / Basis evidence** | Active series chart + quartile table (all horizons) | `rv_basis.series[active]` |
| **Drivers** | `component_inputs[]` strip with weights | pipeline |
| **Funds flow confirmation** | `FundsFlowSponsorshipCard` expanded variant | `funds_flows` (L2 only) |
| **Implementation & sizing** | Selected impl, legs, margin summary | `implementations`, `sizing` |
| **Change mind** | `funds_flows.interpretation.change_mind_trigger`, `directional.invalidation` | derived |
| **Provenance footer** | `snapshot_id`, `as_of`, `freshness_status`, flows source | bundle + `flows_meta` |

### 2.3 Flip inside focus

- `←`/`→` changes `focus_node_id` and `active_node_id` together.
- Chart animates ≤150ms cross-fade; **no** height change between nodes.
- Operator overrides (`node_cockpit_overrides`) follow the focused node.

### 2.4 AI usage in focus mode

- **No** on-open LLM call.
- Optional button: “Challenge thesis” → single structured prompt using **already-hydrated** fields only (export-style), operator-triggered.

---

## 3. Reusable node cockpit shell (all five nodes)

Fixed grid — same DOM structure for every node:

```
┌─────────────────────────────────────────────────────────────────┐
│ GLOBAL REGIME BAND (persistent) — score, gate, freshness, BTC  │
├─────────────────────────────────────────────────────────────────┤
│ NODE RAIL — 5 tabs + compare toggle                             │
├──────────────────────────────┬────────────────────────────────┤
│ CHART AREA (flex)            │ DECISION SIDE RAIL (fixed width) │
│  • RV / Basis primary chart  │  • Directional summary         │
│  • Horizon + series selectors  │  • Relative value posture      │
│  • Threshold bands overlay     │  • Implementation picker       │
│                              │  • FundsFlowSponsorshipCard      │
│                              │  • Sizing (when enabled)         │
├──────────────────────────────┴────────────────────────────────┤
│ DETAIL BAND — component_inputs strip + china_parallel (optional)│
├─────────────────────────────────────────────────────────────────┤
│ ACTIONS — Here's Why · Compare · Export node · Accept tracer    │
└─────────────────────────────────────────────────────────────────┘
```

| Zone | Height behavior |
|------|-----------------|
| Global band | fixed 56px |
| Node rail | fixed 48px |
| Chart + side rail | min 320px; **fixed** between flips |
| Detail band | max 120px; collapsible |
| Funds flow card | fixed 150px rail / 120px compare |

**Muscle-memory rule:** Control positions do not move between nodes; only labels and data change.

---

## 4. Relative Value & Basis charts

### 4.1 Visual standard

Reference quality bar: institutional minimal — `basis-chart-template.html` lineage (clean axes, muted grid, single accent for active series).

| Element | Rule |
|---------|------|
| Background | Match TC dark theme; no gradients |
| Line | 1.5px primary series; 1px reference median |
| Threshold bands | Shaded Q1/Q4 zones from **active horizon** percentile bins |
| Current marker | Dot + label: value, percentile, quartile |
| X-axis | Dates; preserve zoom on flip (see §1.5) |
| Y-axis | `tabular-nums`; unit from `rv_basis.series.*.horizons.*.unit` |
| Legend | Series label + `quartile_direction` hint |

### 4.2 What the chart must answer in &lt;3 seconds

1. Where is the series **now**?
2. Versus **which horizon** (1M–3Y selector)?
3. **Rich or cheap** per `quartile_direction`?
4. Distance to **decision thresholds** (ref_low/mid/high when on basis node)?

### 4.3 Basis node extras

- Overlay `execution.basis_spread` when present.
- Show `ref_low`, `ref_mid`, `ref_high` horizontal guides from execution sidecar.
- Calendar spread from `btc_calendar_bt_near_deferred` as primary series default.

### 4.4 Client vs pipeline

| Responsibility | Owner |
|----------------|-------|
| History series, percentile, quartile, richness_label | **Pipeline** at hydrate |
| `active_horizon`, `active_series_id`, zoom, y-scale | **Client** (localStorage) |
| Chart draw | **Client** from hydrated `rv_basis.series` — no fetch on horizon toggle |

---

## 5. Quartile & percentile — pipeline authority (with examples)

### 5.1 Where calculation lives

**Pipeline only:** `whinfell_pipeline/node_cockpits.py` (or `rv_quartiles.py` helper) during `build_node_cockpit()`.

**Client:** reads `rv_basis.series.{id}.horizons.{h}.*` — never recomputes percentile.

**Registry:** `data_dictionary.yaml` → `rv_series` (`quartile_direction`, lookback days).

### 5.2 Algorithm (per `series_id` × horizon)

```
window = last N trading rows for series (N from rv_series.lookback_trading_days)
percentile = (count(window <= current_value) / len(window)) * 100
quartile = bin(percentile): 1→[0,25), 2→[25,50), 3→[50,75), 4→[75,100]
richness_label = map(quartile, quartile_direction)  # see Data Model §6.3
```

### 5.3 Worked example — Credit `hy_oas_proxy` (higher_is_cheaper)

| Horizon | Window | Current (bps) | Percentile | Quartile | Richness |
|---------|--------|---------------|------------|----------|----------|
| 3m | 63d | 312 | 18 | 1 | **cheap** |
| 12m | 252d | 312 | 42 | 2 | fair |

Desk read: “HY OAS cheap vs 3M, fair vs 12M” — drives `relative_value.posture: long_spread`.

### 5.4 Worked example — Basis `btc_calendar_bt_near_deferred` (higher_is_richer)

| Horizon | Current (%) | Percentile | Quartile | Richness |
|---------|-------------|------------|----------|----------|
| 3m | 1.25 | 82 | 4 | **extreme** |

Desk read: “Calendar extreme rich vs 3M” — supports `relative_value.posture: short_spread`.

### 5.5 Exposure surfaces

| Surface | Fields shown |
|---------|--------------|
| Normal chart header | `richness_label`, percentile, active horizon |
| Side rail RV line | `quartile_context` one-liner |
| Full-screen table | All horizons for active + secondary series |
| WTM EXPORT v2.2 | `RV Horizon \| Quartile \| Percentile \| Richness \| Direction` |

---

## 6. State model summary

Three layers — full field tables in [Phase2_Node_Cockpit_Data_Model.md §13](Phase2_Node_Cockpit_Data_Model.md).

| Layer | Storage | Examples |
|-------|---------|----------|
| **Hydration (read-only)** | `data/hydration/latest.json` | `node_cockpits`, `cockpit_context`, `flows_sidecar` |
| **Session navigation** | `localStorage` v7 `navigation.*` | `active_node_id`, `view_mode`, `focus_mode` |
| **Operator overrides** | `localStorage` v7 `node_cockpit_overrides.*` | sizing, `active_series_id`, rationale edits |

**Merge at render:** `hydration[node]` ⊕ `overrides[node]` → displayed cockpit.

**flows_meta contract:** Always read `funds_flows.flows_meta` before rendering verdict chrome; `unavailable` ≠ `neutral` styling.

---

## 7. Implementation sequence (UI)

| PR | Deliverable |
|----|-------------|
| UI-1 | Shell grid + node rail + keyboard bindings (flip only) |
| UI-2 | RV/Basis chart component bound to `rv_basis` |
| UI-3 | Full-screen “Here’s Why” focus layer |
| UI-4 | Compare mode + persistence (`localStorage` v7) |
| UI-5 | `FundsFlowSponsorshipCard` (PR-4 flows) |

**Gate:** Each PR passes Interaction Standard ship checklist + AI-first rules (§ above).

---

## 8. Lock checklist (desk sign-off)

- [ ] AI-first: pipeline owns quartile/verdict; no hydrate-time LLM
- [ ] Rail order and keyboard map accepted
- [ ] Shell zones fixed height — no flip reflow
- [ ] Focus mode is full-viewport layer, not modal
- [ ] Compare max 3 nodes; degraded nodes visibly distinct
- [ ] Quartile examples match desk intuition for credit + basis
- [ ] `flows_meta` renders before verdict badge (PR-4)

---

**References:** `08_Deliverables/Whinfell_Transmission_Control.html` · `whinfell_pipeline/data_dictionary.yaml` (`rv_series`) · `Phase2_Flows_Implementation_Spec.md` (`flows_meta`)