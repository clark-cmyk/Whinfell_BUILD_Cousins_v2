# Whinfell Operator Dashboard — Setup Guide

**Deliverable:** C4.5 + C4.6  
**Main file:** `Whinfell_Operator_Dashboard.html`  
**Version:** C4.6 Draft (WTM Action Layer)  
**Lead:** Bridge (Edge, Precision support)

---

## Open Daily (Desk Command)

```bash
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Operator_Dashboard.html
```

---

## What This Is

**WTM decision and action layer** — no-iframe control surface with enforceable gates:

| Zone | Width | Content |
|------|-------|---------|
| Left | ~60% | Koyfin status panel → **Open Live Koyfin** |
| Right | ~40% | Barchart status panel → **Open Live Barchart** |
| WTM Intake | Full | Transmission State, Score, Confidence, Desk Posture |
| Decision Summary | Full | Auto-generated WTM action line |
| Bottom tabs | Full | BTC module · WTM Prompts A–E · Gross Risk |

---

## First-Time Setup (~2 min)

1. Paste Koyfin + Barchart URLs → **Save Settings**
2. Each morning: open Koyfin → fill **WTM Regime & Posture** panel
3. Click **Open Live Koyfin** + **Open Live Barchart**
4. Review **WTM Decision Summary** before any BTC action

---

## WTM Gate Rules (C4.6)

| Whinfell Score | BTC Gate | Action |
|----------------|----------|--------|
| **&lt; 50** | **BLOCKED** | BTC options/calendar arb module disabled |
| **50–64** | **CLIENT-ONLY** | Client basis structures only |
| **65+** | **OUTRIGHT ALLOWED** | Outright BTC structures permitted if ArbScore supports |

---

## BTC Options & Calendar Arb Module

1. Open **BTC Options & Calendar Arb** tab
2. Enter **Basis1** (near/front) and **Basis2** (far/back) in bps
3. Review **ΔBasis**, **ArbScore**, and regime gate status
4. Copy **Prompt ③b — BTC Calendar Arb Agent** when gate permits

**ArbScore formula:** ΔBasis = Basis2 − Basis1 · ArbScore = clamp(50 + ΔBasis × 5, 0–100)

---

## 5-Minute Morning Workflow

| Min | Action |
|-----|--------|
| 1 | Open Koyfin → set WTM Regime & Posture |
| 2 | Scan Liquidity, Rates, Credit (Koyfin tab) |
| 3 | Barchart → Futures + Basis |
| 4 | Check BTC gate → Run WTM Prompts A + B |
| 5 | Update Gross Risk + review Decision Summary |

---

## WTM Prompts (A–E + ③b)

| Prompt | Purpose |
|--------|---------|
| **A** | Transmission + Score validation |
| **B** | Credit Confirmation deep dive |
| **C** | Futures leadership + Basis edge |
| **D** | Gross risk posture decision |
| **E** | Divergence check + shift handover |
| **③b** | BTC Calendar Arb Agent (from BTC tab) |

All prompts: click **Copy** → paste to agent.

---

## Persistence

All fields save via **Save Settings** to `localStorage` key `whinfell_operator_v2`. Migrates automatically from v1.

---

## References

- `08_Deliverables/C1_Whinfell_Credit_Confirmation_Score_Logic.md`
- `08_Deliverables/C3_Whinfell_Series_Ticker_Master_List.md`
- `08_Deliverables/C2_Whinfell_Credit_Score_Fallback.xlsx`