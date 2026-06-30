# Phase 2 Interim Node Score Weights (Non-Credit Nodes)

**Version:** 1.0-interim (locked)  
**Date:** June 29, 2026  
**Owners:** Blueprint + Bridge  
**Status:** Locked for Phase 2 implementation  
**Machine registry:** `whinfell_pipeline/data_dictionary.yaml` → `node_score_weights`  
**Authoritative credit doc:** [Whinfell_Credit_Confirmation_Score_Logic.md](Whinfell_Credit_Confirmation_Score_Logic.md) (unchanged)

---

## Shared design (all nodes)

| Rule | Value |
|------|-------|
| Base score | 50 |
| Clamp | 0–100 |
| Clear bullish | +full weight |
| Clear bearish | −full weight |
| Mixed / weak | ±half weight |
| Unavailable | 0 (no weight redistribution) |
| **Primary authority** | Weighted components (this doc) |
| **Fallback** | `horizon_net` mapped 0–100 when **< 2** components scorable |
| Low confidence | ≥2 components at 0 → flag `confidence: low` |

```
Final Score = CLAMP(50 + Σ(component_points), 0, 100)
component_points = weight_pct × direction_multiplier
```

---

## 1. Liquidity & Rates (`node_id: liquidity`)

**Purpose:** Measure whether curve shape and funding conditions support or impair risk transmission.

| # | Component | Weight | Bullish (+) | Bearish (−) |
|---|-----------|--------|-------------|-------------|
| 1 | 2s10s direction (5D + 20D) | **30%** | Curve steepening constructively; 2s10s rising | Inversion deepening; bear steepener |
| 2 | SOFR / front-end funding | **25%** | Stable or easing front-end | Funding stress; SOFR spike vs OIS |
| 3 | 10Y yield impulse (3M) | **20%** | Orderly decline or stable real yields | Sharp 3M rise in yields (tightening impulse) |
| 4 | DXY liquidity (5D + 20D) | **15%** | Dollar stable or weakening (easier conditions) | Dollar squeeze; DXY breaking higher |
| 5 | Real rates / duration proxy | **10%** | Duration supportive for risk | Duration headwind; real yields rising |

**Primary data:** `WTM-Rates-Credit` export, Koyfin `USGG2Y10Y`, `SOFR`, `US10Y`, Barchart `DXY00`.

**RV primary series:** `usgg2y10y` (`quartile_direction: higher_is_richer`).

---

## 2. Equity Breadth (`node_id: breadth`)

**Purpose:** Measure whether participation is broadening beyond megacap index strength.

| # | Component | Weight | Bullish (+) | Bearish (−) |
|---|-----------|--------|-------------|-------------|
| 1 | IWM / SPY ratio (5D + 20D) | **30%** | Small caps keeping pace or leading | IWM lagging; narrow rally |
| 2 | Equal-weight vs cap-weight | **25%** | RSP/SPY or equal-weight outperforming | Cap-weight concentration only |
| 3 | XLF vs XLU relative (5D + 20D) | **20%** | Cyclicals / financials leading defensives | Defensives outperforming |
| 4 | Cyclical participation | **15%** | Industrials/materials confirming index | Cyclicals lagging on up days |
| 5 | Sector breadth | **10%** | Multi-sector participation | Single-sector or megacap-led |

**Primary data:** `WTM-Equities-Breadth` export, Koyfin `IWM`, `SPY`, `QQQ`, `XLF`, `XLU`.

**RV primary series:** `iwm_spy_ratio` (`quartile_direction: higher_is_richer`).

---

## 3. High-Beta / BTC (`node_id: highbeta`)

**Purpose:** Measure whether BTC and high-beta vehicles are leading or lagging risk transmission.

| # | Component | Weight | Bullish (+) | Bearish (−) |
|---|-----------|--------|-------------|-------------|
| 1 | IBIT vs QQQ (5D + 20D) | **30%** | IBIT leading QQQ | IBIT lagging QQQ |
| 2 | IBIT vs SPY beta transmission | **25%** | Clean beta-up on risk-on days | Beta failure; IBIT flat on SPY up |
| 3 | BTC spot momentum (5D + 20D) | **20%** | BTC trending higher | BTC trending lower |
| 4 | BTC / SPY decoupling | **15%** | Correlation rising on risk-on | Decoupling / divergence on up days |
| 5 | ETH / BTC confirmation | **10%** | ETH confirming BTC beta | ETH lagging; narrow crypto beta |

**Primary data:** `WTM-Crypto-Price`, `WTM-Crypto-Correl`, Koyfin `IBIT`, `BTCUSD`, `ETHUSD`, Barchart `^BTCUSD`.

**RV primary series:** `ibit_qqq_beta_spread` (`quartile_direction: higher_is_richer`).

---

## 4. Basis & Term Structure (`node_id: basis`)

**Purpose:** Measure calendar richness, contango stability, and warehousing conditions for BTC basis trades.

| # | Component | Weight | Bullish (+) | Bearish (−) |
|---|-----------|--------|-------------|-------------|
| 1 | Calendar level vs refs | **30%** | Spread inside ref band; fair to cheap | Rich vs refs; extended contango |
| 2 | Calendar direction (5D + 20D) | **25%** | Stabilizing or cheapening | Widening / deteriorating 20D trend |
| 3 | Contango / roll stability | **20%** | Stable roll; warehousing viable | Whippy roll; unstable curve |
| 4 | Basis vs ref_low/mid/high | **15%** | Below mid ref (cheap carry entry) | Above high ref (fade richness) |
| 5 | IBIT vs futures basis gap | **10%** | ETF/futures basis aligned | Large ETF premium/discount gap |

**Primary data:** Barchart `BTM26` spreads, `WTM-BTC-Basis`, execution block `basis_spread`, `ref_low/mid/high`.

**RV primary series:** `btc_calendar_bt_near_deferred` (`quartile_direction: higher_is_richer`).

---

## Missing data rules (interim — mirrors C1)

| Situation | Rule |
|-----------|------|
| 20D% unavailable | Use 1M% proxy; flag substitution |
| 5D% unavailable | Half-weight mixed; flag |
| Conflicting 5D vs 20D | Half-weight in direction of 20D |
| Component unavailable | 0 points; no redistribution |
| < 2 components scorable | `composite_score_source: horizon_net_fallback` |

---

## Promotion path

These interim tables are **locked for Phase 2 MVP**. Full authoritative docs (v1.0 sign-off) replace interim when Blueprint completes per-node score logic with desk examples. Credit node continues to use C1 authoritative doc only.

**Locked:** BUILD Cousins · June 29, 2026