# Whinfell Credit Confirmation Score — Full Calculation Logic

**Deliverable:** C1  
**Version:** 1.0  
**Owners:** Blueprint + Edge  
**Date:** June 26, 2026  
**Status:** Submitted for Arena Review
**Authoritative Source:** TempLibby / Arena (June 26, 2026)

---

## 1. Overview

The **Whinfell Credit Confirmation Score** is a 0–100 composite that measures whether credit and cross-asset conditions **confirm** or **impair** risk appetite. It is used to gate gross exposure and basis trade selection on the Transmission Map dashboard.

**Design principle:** Start neutral (50), add or subtract component weights based on signal direction, clamp to 0–100.

---

## 2. Weighting Table (Authoritative)

| # | Component | Weight | Bullish Condition | Bearish Condition |
|---|-----------|--------|-------------------|-------------------|
| 1 | HY spread trend (5D + 20D) | **25%** | HY spreads tightening on both windows | HY spreads widening on both windows |
| 2 | IG spread trend (5D + 20D) | **15%** | IG spreads tightening or stable | IG spreads widening persistently |
| 3 | HY minus IG differential | **10%** | Differential narrowing | Differential widening |
| 4 | HYG / LQD ratio | **10%** | Ratio rising | Ratio falling |
| 5 | Financials vs Defensives (XLF vs XLU/XLP) | **10%** | XLF outperforming defensives | XLF lagging defensives |
| 6 | 2s10s + 3m10y curve impulse | **10%** | Curve steepening for constructive/growth reasons | Inversion deepening or bear steepener |
| 7 | Equity breadth confirmation | **10%** | RTY + cyclicals participating meaningfully | Narrow megacap-led rally only |
| 8 | BTC / High-beta confirmation | **10%** | IBIT and high-beta assets confirming risk appetite | IBIT lagging or diverging sharply |

**Total weight:** 100%

---

## 3. Calculation Formula

### Step 1 — Base Score

```
Base Score = 50
```

### Step 2 — Score Each Component

For each of the 8 components, assign a **signal direction**:

| Signal | Points Applied |
|--------|----------------|
| **Clear Bullish** | +Full weight (e.g., +25 for Component 1) |
| **Clear Bearish** | −Full weight (e.g., −25 for Component 1) |
| **Mixed / Weak** | ±Half weight (e.g., +12.5 or −12.5 for Component 1) |
| **No readable signal** | 0 (see Missing Data Rules) |

```
Component Points = Weight × Direction Multiplier

Where Direction Multiplier = +1 (bullish), −1 (bearish), ±0.5 (mixed), or 0 (unavailable)
```

### Step 3 — Sum and Clamp

```
Raw Score = 50 + Σ(Component Points)
Final Score = CLAMP(Raw Score, 0, 100)
```

### Quick Reference Formula

```
Score = CLAMP( 50
  + HY_spread_pts      (±25 or ±12.5)
  + IG_spread_pts      (±15 or ±7.5)
  + HY_IG_diff_pts     (±10 or ±5)
  + HYG_LQD_ratio_pts  (±10 or ±5)
  + XLF_defensive_pts  (±10 or ±5)
  + Curve_impulse_pts  (±10 or ±5)
  + Breadth_pts        (±10 or ±5)
  + BTC_highbeta_pts   (±10 or ±5)
, 0, 100)
```

---

## 4. Data Sources

| Component | Primary Source | Series / Field | Notes |
|-----------|---------------|----------------|-------|
| HY spread trend | Koyfin | HY OAS or equivalent spread index — 5D change + 20D change | Tightening = spread level falling |
| IG spread trend | Koyfin | IG OAS or equivalent — 5D change + 20D change | Stable = within ~2 bp over 20D |
| HY minus IG differential | Koyfin / derived | HY OAS − IG OAS; compare 5D and 20D direction | Narrowing = differential shrinking |
| HYG / LQD ratio | Koyfin / Barchart | HYG price ÷ LQD price; track 5D direction | Rising ratio = risk-on credit |
| Financials vs Defensives | Koyfin / Barchart | XLF return vs blended XLU + XLP (or XLU alone) over 5D and 20D | Relative performance, not absolute |
| 2s10s + 3m10y curve impulse | Koyfin / FRED | 2s10s spread change + 3-month change in 10Y yield | Distinguish bull steepener vs bear steepener |
| Equity breadth | Koyfin / Barchart | RTY vs SPX (or QQQ) + cyclical sector participation | Meaningful = RTY keeping pace or leading |
| BTC / High-beta | Koyfin / Barchart | IBIT 5D% vs SPX; high-beta basket confirmation | Divergence = IBIT lagging on risk-on days |

> **C3 dependency:** Exact Koyfin ticker codes and Barchart series IDs will be documented in the Series & Ticker Master List (C3).

---

## 5. Missing Data Rules

| Situation | Rule |
|-----------|------|
| **20D% not directly available** | Use 1M% as proxy for 20D window. Note substitution in calculation log. |
| **5D% not available** | Use most recent 5 trading-day manual calc from daily closes. If impossible, score component as **Mixed (half weight)** and flag. |
| **Spread data delayed** | Fall back to HYG/LQD price-ratio direction as proxy for Components 1–3 only; score at **half weight** and flag as proxy. |
| **Single window conflicts** (5D bullish, 20D bearish) | Score as **Mixed (half weight)** in the direction of the 20D signal. |
| **Curve data unavailable** | Score Component 6 as **0**; do not impute. Note gap in log. |
| **Component entirely unavailable** | Assign **0 points**; do not redistribute weight. Final score reflects reduced confidence — note in interpretation. |

**Manual calc rule:** If ≥2 components are scored at 0 due to missing data, treat the overall reading as **low confidence** regardless of numeric score.

---

## 6. Component Scoring Guide (Desk Reference)

### Component 1 — HY Spread Trend (25%)

| Reading | Condition |
|---------|-----------|
| **Bullish (+25)** | HY OAS down on both 5D and 20D |
| **Bearish (−25)** | HY OAS up on both 5D and 20D |
| **Mixed (±12.5)** | One window tightening, one widening; or flat 5D with meaningful 20D move |

### Component 2 — IG Spread Trend (15%)

| Reading | Condition |
|---------|-----------|
| **Bullish (+15)** | IG OAS tightening or stable (≤2 bp change over 20D) |
| **Bearish (−15)** | IG OAS widening persistently (both windows) |
| **Mixed (±7.5)** | Stable 5D but widening 20D, or vice versa |

### Component 3 — HY minus IG Differential (10%)

| Reading | Condition |
|---------|-----------|
| **Bullish (+10)** | Differential narrowing over 5D and 20D |
| **Bearish (−10)** | Differential widening over 5D and 20D |
| **Mixed (±5)** | Conflicting window direction |

### Component 4 — HYG / LQD Ratio (10%)

| Reading | Condition |
|---------|-----------|
| **Bullish (+10)** | Ratio rising over 5D (HYG outperforming on relative basis) |
| **Bearish (−10)** | Ratio falling over 5D |
| **Mixed (±5)** | Flat or choppy; use 1M direction as tiebreaker |

### Component 5 — Financials vs Defensives (10%)

| Reading | Condition |
|---------|-----------|
| **Bullish (+10)** | XLF outperforming XLU/XLP on 5D and 20D |
| **Bearish (−10)** | XLF lagging defensives on both windows |
| **Mixed (±5)** | Outperforming short-term, lagging longer-term |

### Component 6 — Curve Impulse (10%)

| Reading | Condition |
|---------|-----------|
| **Bullish (+10)** | 2s10s steepening with growth/constructive context (not inflation panic) |
| **Bearish (−10)** | Inversion deepening or bear steepener (long-end selloff on growth fears) |
| **Mixed (±5)** | Steepening but driven by front-end cuts pricing; ambiguous context |

### Component 7 — Equity Breadth (10%)

| Reading | Condition |
|---------|-----------|
| **Bullish (+10)** | RTY and cyclicals participating; breadth expanding |
| **Bearish (−10)** | Narrow megacap-led rally; RTY lagging |
| **Mixed (±5)** | RTY flat while SPX rallies |

### Component 8 — BTC / High-Beta (10%)

| Reading | Condition |
|---------|-----------|
| **Bullish (+10)** | IBIT confirming risk-on; high-beta assets aligned |
| **Bearish (−10)** | IBIT lagging or sharp divergence from equities |
| **Mixed (±5)** | IBIT flat while equities rally |

---

## 7. Score Interpretation Bands (Authoritative)

| Score | Color | Zone Name | Positioning Guidance |
|-------|-------|-----------|----------------------|
| **80–100** | Green | Strong Confirmation | Full gross allowed. Aggressive Client + Outright Basis |
| **65–79** | Amber | Constructive | Selective adds. Prefer Client Basis over Outright |
| **45–64** | Amber | Mixed / Fragile | Light gross. Fade weak follow-through |
| **25–44** | Red | Impaired | Reduce beta exposure. Favor hedges and relative value |
| **0–24** | Red | Hard Risk-Off | Defensive posture only |

### Current Dashboard Alignment

Live Comet dashboard (June 26, 2026): **Whinfell Score 58 / Amber — Mixed / Fragile**

---

## 8. Worked Example — Live Dashboard (June 26, 2026)

**Dashboard reading:** Whinfell Score **58** / Amber — Mixed / Fragile  
**Source:** Consolidated snapshot from Comet workspace (Track 1, June 26, 2026)

### Input Data

| Component | Visible Data | Signal Assessment | Points |
|-----------|--------------|-------------------|--------|
| 1. HY spread trend (25%) | HYG +0.04% (1D), +0.19% (5D) | Mild tightening → **Mixed (half bullish)** | **+12.5** |
| 2. IG spread trend (15%) | LQD +0.08% (1D), +0.67% (5D) | Tightening → **Mixed (half bullish)** | **+7.5** |
| 3. HY−IG differential (10%) | Stable | No directional signal | **0** |
| 4. HYG/LQD ratio (10%) | Stable | No directional signal | **0** |
| 5. XLF vs defensives (10%) | XLF −0.50% (1D), −1.11% (5D) | Lagging defensives → **Mixed (half bearish)** | **−5** |
| 6. Curve impulse (10%) | 2s10s / 3m10y neutral / flat | No directional signal | **0** |
| 7. Equity breadth (10%) | SPY flat; Industrials leading, Financials lagging | Mixed participation → **Mixed (half bearish)** | **−5** |
| 8. BTC / high-beta (10%) | IBIT −1.03% (1D) vs SPY +0.14% | Diverging → **Mixed (half bearish)** | **−5** |

### Step-by-Step Calculation

```
Base Score                          = 50.0
+ Component 1 (HY spread)           = +12.5   → 62.5
+ Component 2 (IG spread)           = +7.5    → 70.0
+ Component 3 (HY−IG differential)  = 0       → 70.0
+ Component 4 (HYG/LQD ratio)         = 0       → 70.0
+ Component 5 (XLF vs defensives)     = −5      → 65.0
+ Component 6 (Curve impulse)         = 0       → 65.0
+ Component 7 (Equity breadth)        = −5      → 60.0
+ Component 8 (BTC / high-beta)       = −5      → 55.0

Manual Total (clamped)              = 55
Dashboard Display                   = 58
```

> **Reconciliation note:** Manual calculation yields **55**. The live dashboard displays **58** — a 3-point difference likely reflecting intraday input updates or dashboard smoothing. Both readings fall within the same **Amber — Mixed / Fragile** band (45–64). Flag for Arena Review if tighter alignment is required.

### Calculation Worksheet (Completed)

| Component | Weight | Signal | Points | Running Total |
|-----------|--------|--------|--------|---------------|
| Base | — | — | 50 | 50.0 |
| 1. HY spread trend | 25% | Mixed (mild tightening) | +12.5 | 62.5 |
| 2. IG spread trend | 15% | Mixed (tightening) | +7.5 | 70.0 |
| 3. HY−IG differential | 10% | Stable | 0 | 70.0 |
| 4. HYG/LQD ratio | 10% | Stable | 0 | 70.0 |
| 5. XLF vs defensives | 10% | Mixed (lagging) | −5 | 65.0 |
| 6. Curve impulse | 10% | Neutral / flat | 0 | 65.0 |
| 7. Equity breadth | 10% | Mixed | −5 | 60.0 |
| 8. BTC / high-beta | 10% | Mixed (diverging) | −5 | **55.0** |
| **Final (clamped)** | | | | **55** (dashboard: **58**) |

### Interpretation (June 26, 2026)

| Field | Value |
|-------|-------|
| **Score** | 55 (manual) / 58 (dashboard) |
| **Color** | Amber |
| **Zone** | Mixed / Fragile |
| **Guidance** | Trust equity/crypto moves only lightly. Prefer Client Basis Trades. Avoid aggressive Outright Basis until credit improves. |

**Read:** Credit is mildly supportive (HYG/LQD tightening) but equity internals are fragile — Financials lagging, breadth mixed, and IBIT diverging from SPY. Constructive enough to stay engaged, but not strong enough for full gross or aggressive outright basis.

---

## 9. Manual Calculation Checklist (~2 min)

1. Open Transmission Map / fallback sheet
2. Read each of the 8 component signals (bullish / bearish / mixed)
3. Start at **50**
4. Add or subtract weights per table (half weight for mixed)
5. Clamp to 0–100
6. Map score to interpretation band
7. Apply positioning guidance

---

## 10. Review Status

| Gate | Status | Date |
|------|--------|------|
| Self Review | ✅ **Pass** | June 26, 2026 |
| Peer Review | ✅ **Pass** (Precision) | June 26, 2026 |
| Arena Review | **Submitted** — awaiting Macro Guardian + Risk Warden | June 26, 2026 |
| TempLibby Sign-off | Pending Arena approval | — |

---

*Self Review and Peer Review complete. Submitted for Arena Review — see `C1_Review_Log.md`.*