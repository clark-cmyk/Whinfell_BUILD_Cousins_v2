# Whinfell Operator Dashboard — Setup Guide

**Deliverable:** C4.5  
**Main file:** `Whinfell_Operator_Dashboard.html`  
**Version:** 1.0 (Draft)  
**Lead:** Bridge (Edge, Forge Master, Clarity)  
**Date:** June 26, 2026

---

## Purpose

Single browser window for daily Whinfell desk operations — workaround for Comet split-screen limitation.

| Zone | Width | Content |
|------|-------|---------|
| Left | ~60% | Koyfin Whinfell Transmission Map |
| Right | ~40% | Barchart futures / basis execution |
| Bottom | Full width | Prompts · 5-min workflow · Gross Risk |

---

## Open Daily

```bash
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Operator_Dashboard.html
```

1. Use Chrome or Edge — bookmark for one-click access  
2. Full screen recommended (`Cmd + Ctrl + F` on macOS)

---

## First-Time Setup (~2 min)

1. **Left pane** — paste your Koyfin Whinfell workspace URL  
2. **Right pane** — confirm Barchart URL (default: major commodities futures)  
3. Click **Save Settings** (persists in browser local storage)  
4. If iframe is blocked → click **Open ↗** per pane; keep dashboard open for bottom utilities

---

## 5-Minute Morning Workflow

| Min | Action |
|-----|--------|
| 1 | Transmission State Banner + Whinfell Score (Koyfin) |
| 2 | Liquidity, Rates, Credit Confirmation (Koyfin) |
| 3 | Futures Leadership + Basis Edge (Barchart) |
| 4 | Run Prompts ① + ② (copy from bottom panel) |
| 5 | Set posture + update Gross Risk fields |

**Daily Rule:** Update Gross Risk after morning review and after any material trade.

---

## Bottom Panel

- **5-Min Morning Workflow** — step-by-step checklist  
- **Saved Agentic Prompts (6)** — copy-paste to agent  
- **Gross Risk Controls** — Book A/B, score, posture, handover  
- **Quick Tickers** — C3 master list shortcuts to Barchart

---

## Review Gates

Self Review (Bridge) → Peer (Blueprint + Clarity) → Arena (Integration Dynamo + Visual Vanguard) → TempLibby sign-off

---

## References

- `07_Reference_Materials/Whinfell_Series_Ticker_Master_List.md`
- `08_Deliverables/C1_Whinfell_Credit_Confirmation_Score_Logic.md`
- `08_Deliverables/C2_Whinfell_Credit_Score_Fallback.xlsx`