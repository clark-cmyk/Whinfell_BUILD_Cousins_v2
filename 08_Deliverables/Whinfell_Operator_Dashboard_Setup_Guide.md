# Whinfell Operator Dashboard — Setup Guide

**Deliverable:** C4.5  
**Main file:** `Whinfell_Operator_Dashboard.html`  
**Version:** 0.3 (Draft)  
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

1. In the **Preferred Default URLs** bar (top of page):
   - Paste your **Koyfin Whinfell workspace URL**
   - Paste your **Barchart futures / basis page URL**
2. Click **Save Settings** — stores defaults in browser `localStorage` (loads automatically next open)
3. Click **Reload Panes** if needed after saving
4. If iframe is blocked → click **Open ↗** per pane; keep dashboard open for bottom utilities

**v0.3:** Prominent **↻ Refresh All Panes** · optional 5-min auto-refresh · URL Setup Help tab.

## Refresh Panes

- Click **↻ Refresh All Panes** (header or settings bar) each morning or after market moves
- Optional: enable **Auto-refresh every 5 min** (reloads iframe src; may not work if site blocks embed — use Open ↗)

## Visual Reference vs Daily Cockpit

- **Perplexity dashboard** — visual reference
- **This local HTML file** — primary daily operations cockpit

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