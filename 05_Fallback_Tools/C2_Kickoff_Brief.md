# C2 Kickoff Brief: Fallback Excel / Google Sheet Dashboard

**Task ID:** C2  
**Priority:** 1 (High)  
**Owners:** Edge + Safeguard  
**Status:** ✅ Approved & Signed Off (v0.1)
**Activated:** June 26, 2026  
**Dependency:** C1 v1.0 (Approved & Signed Off)

---

## Objective

Build a manual fallback dashboard that replicates the Whinfell Credit Confirmation Score and basic basis conditions when Comet/Koyfin is unavailable.

## Required Deliverable

One Excel workbook (`.xlsx`) in this folder containing:

1. **Input Panel** — Blue-coded cells for observable market data (HYG, LQD, XLF, IBIT, SPY returns, etc.)
2. **Signal Assessment** — Per-component Bullish / Mixed / Bearish / Neutral selection
3. **Score Engine** — Auto-calculates from C1 formula (base 50, weighted sum, clamp 0–100)
4. **Interpretation Panel** — Color zone, band name, positioning guidance
5. **Basis Conditions** — Basic checklist (Client Basis vs Outright Basis readiness)
6. **Instructions Tab** — How to update daily in <2 minutes

## Success Criteria

- Trader can update inputs and read score + guidance in under 2 minutes
- Logic matches approved C1 v1.0 exactly
- Zero formula errors
- Usable offline (no live API dependencies)

## Review Gates

1. Self Review (Edge + Safeguard)
2. Peer Review (Blueprint)
3. Arena Review (Basis Avenger + Risk Warden)
4. TempLibby Sign-off

---

**Start work now using `04_Score_Calculation/Whinfell_Credit_Confirmation_Score_Logic.md` as source of truth.**