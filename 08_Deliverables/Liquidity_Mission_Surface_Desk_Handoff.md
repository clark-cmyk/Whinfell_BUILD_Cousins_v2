# Liquidity Mission-Surface — Desk Handoff Note

**Build:** `2.2-MISSION-2026-06-29` · **Console:** `Whinfell_Transmission_Control.html`  
**Audience:** Operators using Basis/Credit mission-surfaces · **Status:** v1 shipped — desk testing

---

## Open Liquidity — what to check first

Same cockpit shell as Basis/Credit; eyebrow reads **"Liquidity mission read."**

| Zone | What you should see |
|------|---------------------|
| **Tactical lead** (`#basisTacticalSentence`) | One RV + gate sentence — **not** the raw band. Example: *"US 2s10s spread is fair; neutral is allowed, but only at 0.5× under Tight Risk."* |
| **Tactical suffix** (muted line below, when material) | Short SQ3 constraint — e.g. *"· SQ3 35 constraint"*. **Not** in the lead line. |
| **Summary strip** | Primary reading in **%** (2s10s spread), stance row (Q · percentile · n), preferred expression + size cap |
| **Implication rail** | Compact chips — see validation below |
| **RV chart** | Generic quartile bars (no Basis-style ref bands) |
| **Shared (unchanged)** | Hydration & Coverage banner · gate decision sentence · post-import checklist · funds-flow card in diagnostics drawer |
| **Theme** | **Light mode** / **Dark mode** toggle in header (persists in browser) |

---

## Validate key behaviors

### Weighted components (fixture default)

Liquidity runs on **interim weighted components** (5 inputs), not horizon-net fallback.

- **Rail:** **Supportive** band chip (not Composite fallback).
- **Full diagnostics → Signal:** Band label + component strip populated.

### Band vs RV tension

Fixture can show band **Supportive** while RV reads **fair** and posture **neutral**.

- **Tactical lead must follow RV + gate**, not the band.

### Gate: Tight Risk + China caution

With Whinfell ~50 and impaired SQ3:

- **Rail gate chip:** **Tight + China Caution**
- **Tactical suffix:** SQ3 constraint when impaired/fragile/mixed
- **China constraint** carried by gate chip + gate sentence; lead stays RV-focused

### Dual RV series

Liquidity has **2s10s** (primary, %) and **SOFR stress** (secondary, bps). Switching active series updates tactical lead + summary strip.

### Weakest link

When Liquidity is transmission weakest link: **Weakest link** chip on implication rail only.

---

## Recommended first test cases

| # | Test | Expected on Liquidity |
|---|------|----------------------|
| 1 | Import bundle → select **Liquidity** | Mission banner; reading **~1.225%**; RV **fair** / Q2 |
| 2 | Implication rail | **Supportive · Neutral · Supportive · Tight + China Caution** |
| 3 | Tactical lead vs band | Lead mentions **fair** + gate cap; does not open with "Supportive" |
| 4 | Full diagnostics | Five liquidity components; IEF flows card; gate sentence |
| 5 | Contrast Credit / Basis | Mission surfaces unchanged |
| 6 | Breadth | Legacy rail (no mission banner) |
| 7 | Theme toggle | Header **Light mode** switches console to light theme |

**Open console:**
```bash
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Transmission_Control.html
```