# Liquidity Mission-Surface v1 — Plan

**Build target:** `2.2-MISSION` (same badge family as Basis/Credit)  
**File:** `08_Deliverables/Whinfell_Transmission_Control.html` only  
**Effort:** ~1 session (mirror Credit)  
**Fixture:** `whinfell_pipeline/examples/cockpit_hydration_snippet.json` → `node_cockpits.liquidity`  
**Status:** Approved — implementation in progress (June 30, 2026)

---

## 1. Objective

Extend the mission-surface operator console to **Liquidity & Rates** using the same three-zone pattern as Basis and Credit. Presentation layer only — no hydration, scoring, or `node_cockpits` schema changes.

---

## 2. Mission zones (v1 scope)

| Zone | Liquidity behavior |
|------|-------------------|
| **Tactical banner** | Eyebrow: *"Liquidity mission read."* Lead line = **primary RV series + gate sizing** (not raw band). Suffix = optional SQ3/China constraint (muted). |
| **Summary strip** | Primary reading in **pct** (`usgg2y10y`, e.g. `1.225%`). Stance row: richness · Q · percentile · n. Expression row: preferred RV posture + size cap. |
| **Implication rail** | Compact chips + collapsible Full diagnostics (signal / directional / RV / flows / gate). |
| **Shared (reuse as-is)** | Hydration & Coverage banner · gate decision sentence · post-import checklist · funds-flow card inside diagnostics drawer · RV chart (generic quartile bars). |

---

## 3. Liquidity data model (read-only inputs)

| Domain | Hydration source | v1 display |
|--------|------------------|------------|
| **Primary RV** | `rv_basis.active_series_id` → `usgg2y10y` | Label: *US 2s10s spread* · unit `%` · `higher_is_richer` |
| **Secondary RV** | `sofr_ois_spread` (operator series switch) | Label: *SOFR front-end stress* · unit `bps` · `higher_is_cheaper` |
| **Tradable expression** | `relative_value.posture` + `structure` | Default structure: *2s10s curve trade / SOFR spread* |
| **Composite signal** | `band` / `composite_score_source` | Band chip in rail; **not** the tactical lead |
| **Components** | 2s10s direction, SOFR, 10Y, DXY, real rates | Full diagnostics only (ticker strip unchanged) |
| **Flows** | `funds_flows` / `liquidity_duration` basket | Rail chip + diagnostics card |
| **China** | `china_parallel` (soft coupling) | Gate chip + gate sentence; optional suffix (§7-B) |
| **Gate** | Global Whinfell + transmission health | Tight / Blocked / Tight + China Caution |

**Tactical lead template** (follows existing `buildMissionTacticalLead`):

- *"US 2s10s spread is {richness}; {expression} is allowed, but only at 0.5× under Tight Risk."*
- Blocked: *"… new curve RV is blocked under current gate."*
- Open gate: *"… eligible within desk policy."*

Lead always follows **RV richness + gate**, never the composite band (Credit precedent — §7-A).

---

## 4. Reuse vs Liquidity-specific

### Reuse unchanged

- `MISSION_SURFACE_NODES` pattern + shared DOM (`basisTacticalBanner`, `basisSummaryStrip`, etc.)
- `renderMissionTacticalBanner`, `renderMissionSummaryRows`, `renderMissionImplicationRail`
- `buildMissionTacticalLead`, `buildMissionChartDiagnosis` (non-Basis path)
- Hydration/coverage banner, gate sentence, post-import workflow, funds-flow diagnostics card
- Headless probe pattern (`__creditMissionProbe` → add `__liquidityMissionProbe`)

### Liquidity-specific additions

| Item | Change |
|------|--------|
| `MISSION_SURFACE_NODES` | Add `'liquidity'` |
| `MISSION_NODE_CONFIG.liquidity` | `eyebrow`, `defaultSeriesLabel: 'US 2s10s spread'`, `blockedPhrase: 'new curve RV is blocked under current gate.'` |
| Summary strip unit | `%` for primary series (existing `formatReadingValue` handles `pct`) |
| Implication chips | **Band chip** (not Composite fallback when `weighted_components`) |
| Signal diagnostics copy | Liquidity-weighted components message when populated; horizon-net fallback only if `< 2` components |
| Weakest link chip | **Generalize** to all mission nodes when `is_weakest_link` (§7-C) |
| China suffix | **Generalize** to all mission nodes when SQ3 impaired/fragile/mixed (§7-B) |
| Composite fallback chip | Show when `composite_score_source === 'horizon_net_fallback'` for any mission node (§7-D) |

### Explicitly not changing

- Pipeline / `node_cockpits` builder / scoring weights
- Basis or Credit behavior
- Legacy rail for Breadth / High Beta
- CSS rename of `basis-*` classes (deferred)

---

## 5. Implication rail chips (v1)

| Chip | Source | Liquidity fixture expectation |
|------|--------|------------------------------|
| Signal | `band` or **Composite fallback** if `horizon_net_fallback` | *Supportive* |
| RV posture | `relative_value.posture` | *Neutral* |
| Flows | `funds_flows.aggregate.verdict` | *Supportive* |
| Gate | `resolveMissionGateChipLabel` | *Tight + China Caution* (when SQ3 impaired) |
| Weakest link | `is_weakest_link` | Omit on fixture (Credit is weakest) |

---

## 6. Desk validation (post-build)

| # | Test | Expected |
|---|------|----------|
| 1 | Import bundle → **Liquidity** | Mission banner visible; reading **~1.225%**; RV **fair** / Q2 |
| 2 | Implication rail | *Supportive · Neutral · Supportive · Tight + China Caution* (no Composite fallback) |
| 3 | Tactical lead vs band | Lead mentions **fair** + gate cap; does **not** open with band label alone |
| 4 | Full diagnostics | Five liquidity components visible; IEF flows card; gate sentence populated |
| 5 | Series switch | Toggle to SOFR → strip shows **320 bps**; tactical lead updates series label |
| 6 | Regression Credit / Basis | Mission surfaces unchanged |
| 7 | Breadth | Still legacy rail (no mission banner) |

---

## 7. Locked decisions (approved)

| # | Question | Decision |
|---|----------|----------|
| A | **Band vs RV tension** | Tactical lead follows **RV + gate**; band stays in rail + diagnostics. |
| B | **China coupling** | Gate chip + gate sentence carry China; **SQ3 suffix on all mission nodes** when impaired/fragile/mixed. |
| C | **Weakest link placement** | **Rail chip only** — generalized to all mission nodes. |
| D | **Composite fallback chip** | Show only when `horizon_net_fallback` — any mission node. |

---

## 8. Implementation steps

1. Add `liquidity` to `MISSION_SURFACE_NODES` + `MISSION_NODE_CONFIG`
2. Generalize weakest-link chip, China suffix, composite-fallback chip (A–D)
3. Restore dark/light theme toggle (`btnTheme`, `data-theme`, light CSS tokens)
4. Add `window.__liquidityMissionProbe` (mirror Credit probe)
5. Smoke test fixture + regression Basis/Credit
6. Write `Liquidity_Mission_Surface_Desk_Handoff.md` (post-build)

---

## 9. Out of scope (v1)

- Pipeline / ARCH-1 live component routing
- Credit desk feedback fixes (unless blockers)
- Breadth / High Beta mission surfaces
- Basis polish
- CSS/DOM rename (`basis-*` → neutral)