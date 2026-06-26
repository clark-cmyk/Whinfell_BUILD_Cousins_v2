# Whinfell Series & Ticker Master List

**Deliverable:** C3  
**Version:** 0.9 (Draft — pending review)  
**Owner:** Bridge  
**Last Updated:** June 26, 2026  
**Status:** In Progress — Self Review  
**Maintained by:** BUILD Cousins (Bridge)

---

## Purpose

Single source of truth for all market data series used in the Whinfell Transmission Map Credit Confirmation Score (C1), fallback Excel dashboard (C2), and Comet workspace panels.

---

## Master List

| ID | C1 Component | Display Name | Ticker / Series | Platform | Field | Windows | Used In | Notes |
|----|--------------|--------------|-----------------|----------|-------|---------|---------|-------|
| S01 | 1 — HY spread trend | HY OAS (Option-Adjusted Spread) | `HY OAS` (ICE BofA US High Yield Index OAS) | Koyfin | Spread (bp) | 5D Δ, 20D Δ | Comet, C1 | Primary. Tightening = spread falling |
| S02 | 1 — HY spread trend | HYG Price Return (proxy) | `HYG` | Koyfin / Barchart | Price % chg | 1D, 5D, 1M | C2, Comet | Proxy when OAS delayed; rising HYG ≈ tightening |
| S03 | 2 — IG spread trend | IG OAS | `IG OAS` (ICE BofA US Corporate Index OAS) | Koyfin | Spread (bp) | 5D Δ, 20D Δ | Comet, C1 | Primary. Stable = ≤2 bp over 20D |
| S04 | 2 — IG spread trend | LQD Price Return (proxy) | `LQD` | Koyfin / Barchart | Price % chg | 1D, 5D, 1M | C2, Comet | Proxy when OAS delayed |
| S05 | 3 — HY−IG differential | HY minus IG OAS Spread | Derived: S01 − S03 | Koyfin / derived | Spread (bp) | 5D Δ, 20D Δ | Comet, C1 | Narrowing = bullish |
| S06 | 4 — HYG/LQD ratio | HYG ÷ LQD Relative Ratio | Derived: `HYG` / `LQD` | Koyfin / Barchart | Ratio | 5D direction | Comet, C1, C2 | Rising ratio = risk-on credit |
| S07 | 5 — Financials vs Defensives | Financials Sector ETF | `XLF` | Koyfin / Barchart | Price % chg | 1D, 5D, 20D | Comet, C1, C2 | vs defensives |
| S08 | 5 — Financials vs Defensives | Utilities Sector ETF | `XLU` | Koyfin / Barchart | Price % chg | 1D, 5D, 20D | Comet, C1 | Defensive benchmark |
| S09 | 5 — Financials vs Defensives | Consumer Staples ETF | `XLP` | Koyfin / Barchart | Price % chg | 1D, 5D, 20D | Comet, C1 | Defensive benchmark (alt/complement to XLU) |
| S10 | 6 — Curve impulse | 2s10s Treasury Spread | `USGG2Y10Y` or `T10Y2Y` | Koyfin / FRED | Yield spread | Level + 5D Δ | Comet, C1 | FRED: T10Y2Y (10Y − 2Y) |
| S11 | 6 — Curve impulse | 10-Year Treasury Yield | `US10Y` / `DGS10` | Koyfin / FRED | Yield (%) | 3M Δ | Comet, C1 | 3m10y impulse component |
| S12 | 6 — Curve impulse | 2-Year Treasury Yield | `US2Y` / `DGS2` | Koyfin / FRED | Yield (%) | 5D Δ | Comet, C1 | Front-end context for steepener classification |
| S13 | 7 — Equity breadth | Russell 2000 ETF | `IWM` or index `RUT` | Koyfin / Barchart | Price % chg | 5D vs SPX | Comet, C1 | Small-cap participation |
| S14 | 7 — Equity breadth | S&P 500 ETF | `SPY` | Koyfin / Barchart | Price % chg | 1D, 5D | Comet, C1, C2 | Benchmark for breadth |
| S15 | 7 — Equity breadth | Industrials Sector ETF | `XLI` | Koyfin / Barchart | Price % chg | 5D | Comet, C1 | Cyclical participation signal |
| S16 | 8 — BTC / High-beta | Bitcoin ETF | `IBIT` | Koyfin / Barchart | Price % chg | 1D, 5D vs SPY | Comet, C1, C2 | High-beta confirmation |
| S17 | 8 — BTC / High-beta | Nasdaq 100 ETF (alt high-beta) | `QQQ` | Koyfin / Barchart | Price % chg | 5D | Comet, C1 | Secondary high-beta reference |

---

## Platform Reference Keys

| Platform | Identifier Format | Access |
|----------|-------------------|--------|
| **Koyfin** | Ticker search (e.g., `HYG`, `HY OAS`) | Comet workspace / Koyfin terminal |
| **Barchart** | Symbol (e.g., `HYG`) | Barchart quote pages |
| **FRED** | Series ID (e.g., `T10Y2Y`, `DGS10`, `DGS2`) | fred.stlouisfed.org |

---

## Proxy Hierarchy (when primary unavailable)

| Component | Primary | Fallback 1 | Fallback 2 |
|-----------|---------|------------|------------|
| HY spread | S01 (HY OAS) | S02 (HYG returns) | Half-weight mixed + flag |
| IG spread | S03 (IG OAS) | S04 (LQD returns) | Half-weight mixed + flag |
| HY−IG diff | S05 (derived OAS) | S06 (HYG/LQD ratio direction) | Neutral (0 pts) |
| Curve | S10 + S11 | S12 for context only | 0 pts + flag |

Per C1 Section 5 Missing Data Rules.

---

## Maintenance Protocol

1. **On Comet series change:** Bridge updates this file within 1 business day
2. **Version bump:** Log changes in `01_Strategy_Docs/Progress_Log.md`
3. **Review cadence:** Re-validate quarterly or on any Transmission Map framework update

---

## Open Items (for Arena / Comet confirmation)

| Item | Status | Action |
|------|--------|--------|
| Exact Koyfin series ID for HY OAS panel | Pending Comet workspace confirm | Verify against live dashboard |
| Exact Koyfin series ID for IG OAS panel | Pending Comet workspace confirm | Verify against live dashboard |
| RTY vs IWM — which is used in Comet breadth panel | Assumed IWM/SPY | Confirm with live workspace |

---

## Review Status

| Gate | Status | Date |
|------|--------|------|
| Self Review | In Progress | June 26, 2026 |
| Peer Review | Not started | — |
| Arena Review | Not started | — |
| TempLibby Sign-off | Not started | — |