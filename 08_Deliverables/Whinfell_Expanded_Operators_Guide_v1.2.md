# Whinfell Expanded Operator's Guide v1.2

**Version:** 1.2  
**Date:** June 26, 2026  
**Authority:** TempLibby, Template Team  
**Status:** Production — Desk Rollout  
**Primary file:** `Whinfell_Transmission_Control.html`  
**Quick ref:** `Whinfell_Quick_Reference_Card_v1.2.docx`

---

## 1. System Architecture

| Layer | Tool | Role |
|-------|------|------|
| **Research & Analysis** | Perplexity (Prompts A–E) | Regime read, sizing, trade eval, income, divergence |
| **Execution & State** | Transmission Control (HTML) | Intake, gates, gross risk, tracer, BTC modules |
| **Live Data** | Koyfin + Barchart (browser tabs) | Transmission map, futures/basis |

**No iframes.** Control surface opens live data in dedicated tabs.

---

## 2. Open Commands

```bash
# Primary execution layer (v1.2 + Phase 2)
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Transmission_Control.html

# Quick Reference Card (print at desk)
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Quick_Reference_Card_v1.2.docx

# Legacy full cockpit (optional)
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Operator_Dashboard.html
```

---

## 3. Daily Workflow (5 Minutes)

| Step | Action |
|------|--------|
| 1 | Open Koyfin → read Transmission Map |
| 2 | Run **Prompt A** in Perplexity |
| 3 | Copy **WTM EXPORT v2.0** block from response |
| 4 | **Import from Perplexity** in Transmission Control |
| 5 | Verify Gate Banner, Gross Risk, Signal Tracer |
| 6 | Run Prompts B–E as needed · **Save State** |

---

## 4. WTM EXPORT v2.0 (Research Handoff)

Perplexity responses must end with:

```
--- WTM EXPORT v2.0 ---
Whinfell Score: [0-100]
Transmission State: [Normal / Stressed / Disorderly / Crisis]
Regime Tag: [phrase]
Key Observation: [1-2 sentences]
Gross Risk Recommendation: [e.g. 35% total, Light posture]
BTC Bias: [Confirming / Dragging / Neutral]
Timestamp: [YYYY-MM-DDTHH:mm:ss]
```

**Import** populates intake, gross risk, BTC tracer horizon, and research readout.  
**Export for Perplexity** sends full state + v2.0 block back for follow-up prompts.

---

## 5. Gate Rules

| Score | Gate | BTC Access | Banner |
|-------|------|------------|--------|
| &lt; 50 | NO NEW BTC RISK | Blocked | Red |
| 50–64 | Tight Risk Band | Reduced sizing | Amber |
| ≥ 65 | Allowed | Full access | Green |

**Posture ladder:** Full (80+) · Selective (65–79) · Light (50–64) · Defensive (&lt;50) · Flat

Amber warning appears when posture exceeds gate band — confirm intentional.

---

## 6. WTM Prompts

| ID | Title | Use When |
|----|-------|----------|
| A | Transmission Read & Regime Classification | Shift start, regime change |
| B | Posture & Gross-Risk Recommendation | Sizing decisions |
| C | Trade Evaluation & Ranking | Candidate trade list |
| D | Income Projection from Current Book | Session/week P&L outlook |
| E | Divergence & Risk Compression | Tape vs WTM mismatch |
| L2 | BTC Options Workflow | Vol surface / structures |
| L3 | BTC Calendar Arb Agent | Calendar spreads |

Copy buttons in Transmission Control bottom panel.

---

## 7. Signal Tracer (Phase 2)

| Feature | How to Use |
|---------|------------|
| **Horizon matrix** | Mark 1d/5d/20d/60d per stage (↑ → ↓) |
| **Health score** | Informational on gate banner — does not override gate |
| **Shocks** | Credit Widening · Curve Inversion · BTC Decoupling · Vol Spike |
| **Shock config** | Mild (1d only) / Full · per-stage toggles |
| **Re-evaluate** | Refresh matrix → re-apply shock → recalc health |
| **Snapshots** | Save up to 12 named states · compare to current |
| **Scenario Loop** | 3 what-if intake variants (session-only) |

---

## 8. BTC Layer 3 Scan

1. Enter Near Month, Far Month, Basis Spread (manual)
2. Set Reference Low / Mid / High (historical range)
3. Click **Scan for Opportunities** → Rich / Fair / Cheap + hint
4. Copy Layer 3 prompt includes spread fields

Rule-based only — no live Barchart feed.

---

## 9. Persistence

- **Save State** → `localStorage` key `whinfell_transmission_control_v1`
- Migrates from Phase 0/v1.2 legacy keys automatically
- Snapshots stored in schema v3 (max 12)

---

## 10. Known Gaps (Acceptable for Rollout)

- WTC-2.0 full export not yet round-trip importable
- Scenario Loop uses current tracer for all variants (intake-only what-if)
- No live data auto-fill on tracer horizons

Phase 2.1 refinements follow desk feedback.

---

## 11. Feedback

Log usability, tracer value, and handoff reliability in `08_Deliverables/Desk_Feedback_Log.md`.  
Route blockers to TempLibby · BUILD Cousins (Bridge).

---

## 12. Support

| Role | Contact |
|------|---------|
| System owner | TempLibby |
| Build support | BUILD Cousins (Bridge) |
| Quality | Arena Team |

**Ship commits:** P1.2 `c9d9b63` · Sprint `1a33bee` · Production sign-off June 26, 2026