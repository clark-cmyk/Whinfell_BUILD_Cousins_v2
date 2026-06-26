# Whinfell Series & Ticker Master List

**Deliverable:** C3  
**Version:** 1.0  
**Owner:** Bridge  
**Last Updated:** June 26, 2026  
**Status:** Submitted for Arena Review
**Maintained by:** BUILD Cousins (Bridge)

---

## Purpose

Single source of truth for every ticker/series used in the Whinfell Transmission Map — Credit Confirmation Score (8 components), Basis Edge Meter, and Futures Leadership panels.

---

## A. Whinfell Score Components (8)

| Component | Primary Ticker/Series | Fallback / Proxy | Time Window | Koyfin / Barchart Source | Maintenance Note |
|-----------|----------------------|------------------|-------------|--------------------------|------------------|
| **HY Spread Trend** | `HY OAS` (ICE BofA US High Yield Index OAS) | `HYG` price return (1D, 5D, 1M) | 5D Δ, 20D Δ | Koyfin: search "HY OAS" · Barchart: `HYG` | Tightening = spread falling. Proxy at half-weight per C1 §5. Confirm exact Koyfin series ID from Comet. |
| **IG Spread Trend** | `IG OAS` (ICE BofA US Corporate Index OAS) | `LQD` price return (1D, 5D, 1M) | 5D Δ, 20D Δ | Koyfin: search "IG OAS" · Barchart: `LQD` | Stable = ≤2 bp over 20D. Confirm exact Koyfin series ID from Comet. |
| **HY−IG Differential** | Derived: HY OAS − IG OAS | `HYG`/`LQD` ratio direction | 5D Δ, 20D Δ | Koyfin: derived from OAS series | Narrowing = bullish. If OAS unavailable, use ratio trend only. |
| **HYG / LQD Ratio** | Derived: `HYG` ÷ `LQD` | — | 5D direction | Koyfin: `HYG`, `LQD` · Barchart: `HYG`, `LQD` | Rising ratio = risk-on credit. Used in C2 Market Inputs. |
| **Financials vs Defensives** | `XLF` vs `XLU` + `XLP` relative return | `XLF` vs `XLU` only | 1D, 5D, 20D | Koyfin / Barchart: `XLF`, `XLU`, `XLP` | Outperformance = bullish. C2 pre-loads XLF returns. |
| **Curve Impulse (2s10s + 3m10y)** | `T10Y2Y` (2s10s spread) + `DGS10` (10Y yield) | `USGG2Y10Y` (Koyfin) · `DGS2` for front-end context | 5D Δ (spread), 3M Δ (10Y) | Koyfin: `USGG2Y10Y`, `US10Y` · FRED: `T10Y2Y`, `DGS10`, `DGS2` | Distinguish bull steepener vs bear steepener. If unavailable, score 0 + flag. |
| **Equity Breadth** | `IWM` (or `RTY`) vs `SPY` relative + `XLI` cyclical participation | `RUT` index vs `SPX` | 5D relative | Koyfin / Barchart: `IWM`, `SPY`, `XLI` | Confirm RTY vs IWM with live Comet panel. Industrials leading = constructive breadth signal. |
| **BTC / High-Beta** | `IBIT` vs `SPY` relative return | `QQQ` as alt high-beta | 1D, 5D | Koyfin / Barchart: `IBIT`, `SPY`, `QQQ` | Divergence = IBIT lagging on risk-on days. C2 pre-loads IBIT. |

---

## B. Basis Edge Meter

| Component | Primary Ticker/Series | Fallback / Proxy | Time Window | Koyfin / Barchart Source | Maintenance Note |
|-----------|----------------------|------------------|-------------|--------------------------|------------------|
| **Client Basis — Energy** | `CL` (WTI front month) vs cash/refinery margin context | `USO` ETF vs `CL` futures | 5D, 20D | Koyfin / Barchart: `CL1!` or `CL` | Basis Edge Meter right column. Client Basis favored when Score 45–79. |
| **Client Basis — Refined Products** | `RB` (RBOB) − `CL` crack spread | `XLE` sector relative vs `SPY` | 5D | Koyfin / Barchart: `RB`, `CL` | Crack widening/narrowing for product basis context. |
| **Outright Basis — Credit** | `HYG`/`LQD` ratio + HY OAS direction | `HYG` 5D% alone | 5D, 20D | Koyfin: OAS + ETFs | Outright Basis allowed when Score ≥65. Tie to C1 Components 1–4. |
| **Basis Edge Signal (composite)** | Derived from Score band + credit/futures alignment | Manual checklist in C2 Dashboard | Daily | C2 `Basis Trade Readiness` section | Client Basis ✓ at Score ≥45; Outright ✓ at ≥65; Aggressive gross ✓ at ≥80. |

---

## C. Futures Leadership

| Component | Primary Ticker/Series | Fallback / Proxy | Time Window | Koyfin / Barchart Source | Maintenance Note |
|-----------|----------------------|------------------|-------------|--------------------------|------------------|
| **Equity Index Leadership** | `ES` (S&P 500 E-mini) vs `NQ` (Nasdaq) relative | `SPY` vs `QQQ` ETF | 1D, 5D | Koyfin / Barchart: `ES1!`, `NQ1!` | Leadership rotation signals risk appetite shift. |
| **Small Cap Leadership** | `RTY` (Russell 2000 E-mini) vs `ES` | `IWM` vs `SPY` | 5D | Koyfin / Barchart: `RTY1!`, `ES1!` | Aligns with Equity Breadth component. Confirm Comet symbol. |
| **Rates Leadership** | `ZN` (10Y note) vs `ZB` (30Y bond) relative | `T10Y2Y` spread direction | 5D | Koyfin / Barchart: `ZN1!`, `ZB1!` | Rates leading equities = macro-driven session. |
| **Commodity Leadership** | `CL` (WTI) vs `GC` (Gold) relative | `USO` vs `GLD` ETF | 5D | Koyfin / Barchart: `CL1!`, `GC1!` | Risk-on = CL leading; risk-off = GC leading. |
| **Crypto Leadership** | `IBIT` vs `ES` relative | `BTC` spot vs `SPY` | 1D, 5D | Koyfin / Barchart: `IBIT`, `ES1!` | Ties to BTC/High-beta score component. |

---

## Proxy Hierarchy Summary

| If unavailable… | Use… | Then… |
|-----------------|------|-------|
| HY OAS | HYG returns | Half-weight mixed signal + flag |
| IG OAS | LQD returns | Half-weight mixed signal + flag |
| HY−IG OAS differential | HYG/LQD ratio direction | Half-weight or neutral |
| 2s10s / 10Y data | 0 points on curve component | Flag in calculation log |
| Futures continuous (`ES1!`) | ETF equivalent (`SPY`) | Note substitution in log |
| ≥2 components at 0 | — | Low-confidence reading per C1 §5 |

---

## Open Items (pending live workspace confirm)

| # | Item | Owner | Action |
|---|------|-------|--------|
| 1 | Exact Koyfin series ID — HY OAS panel | Bridge | Request from TempLibby / Comet workspace |
| 2 | Exact Koyfin series ID — IG OAS panel | Bridge | Request from TempLibby / Comet workspace |
| 3 | RTY vs IWM — breadth panel symbol | Bridge | Confirm with live dashboard |
| 4 | Basis Edge Meter — exact futures month codes in Comet | Bridge | Confirm CL/RB/RB crack series IDs |

---

## Maintenance Protocol

1. **On Comet series change:** Bridge updates within 1 business day
2. **Version bump:** Log in `01_Strategy_Docs/Progress_Log.md`
3. **Review cadence:** Quarterly or on Transmission Map framework update
4. **Share with desk:** This file + `08_Deliverables/` copies post sign-off

---

## Review Status

| Gate | Status | Date |
|------|--------|------|
| Self Review | ✅ **Pass** | June 26, 2026 |
| Peer Review | ✅ **Pass** (Blueprint) | June 26, 2026 |
| Arena Review | **Submitted** — Integration Dynamo + Macro Guardian | June 26, 2026 |
| TempLibby Sign-off | Not started | — |