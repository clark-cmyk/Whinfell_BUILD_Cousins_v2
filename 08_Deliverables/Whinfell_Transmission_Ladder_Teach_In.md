# Whinfell Transmission Ladder — Teach-In

**Version:** 1.0  
**Date:** 2026-06-28  
**Audience:** (i) Junior analyst (post-undergrad, first desk rotation) · (ii) LLM operator / collection agent  
**Primary surfaces:** `Whinfell_Transmission_Control.html` · `whinfell-transmission-ladder-deep-dive.html`  
**Companion docs:** `Whinfell_Expanded_Operators_Guide_v1.4.md` · `Perplexity_Barchart_Koyfin_Playbook.md` · `Fast_CSV_Collect_Guide.md`

---

## How to use this document

| If you are… | Read first | Then |
|-------------|------------|------|
| **Junior analyst** | Part I (theory, lightly) → Part II (full) | Part IV (enhancements) when you have 2+ weeks on desk |
| **LLM / agent** | Part III (full) → Part I §1–3 (formal definitions) | `desk_urls.yaml`, `run_batch_collect.py plan` for execution |
| **Senior reviewing juniors** | Part II §Mental Math + §Best Practices | Part III §QA for grading desk notes |

---

# Part I — Rigorous theory (shared foundation)

## 1. What problem the ladder solves

Markets do not jump from “macro headline” to “BTC calendar trade” in one step. Risk transmits through a **ordered chain**:

```text
Liquidity & Rates → Credit Confirmation → Equity Breadth → High-Beta/BTC → Basis & Term Structure
```

**Theory (transmission / cascade):** Each stage is a **necessary but not sufficient** filter for the next. When financing is impaired, credit may still look OK intraday; when credit fails, equity beta can be a head-fake; when breadth is narrow, BTC strength may not fund basis warehousing. The ladder makes that chain **explicit and scorable** so the desk does not confuse *price movement* with *transmission quality*.

This is consistent with:

- **Financial conditions indices** (liquidity/rates lead).
- **Cross-asset risk appetite** literature (credit and breadth confirm risk-on).
- **Crypto microstructure** (basis and calendar trades are balance-sheet and funding intensive).

The ladder is **not** a price forecast. It is a **posture filter**: what structures are institutionally supportable *today*.

## 2. Composite scoring theory

Each stage score is a **transparent composite indicator**:

```text
StageScore = Σᵢ (wᵢ × sᵢ)     where Σwᵢ = 100,  sᵢ ∈ {25, 50, 75}
```

| Mark (from tracer) | Subscore sᵢ | Interpretation |
|--------------------|-------------|----------------|
| up | 75 | Constructive transmission on that input |
| flat | 50 | Neutral / fragile — no directional sponsorship |
| down | 25 | Impaired — desk should not build size here |

**Why not equal weights?** In a financing-chain model, inputs that lead the constraint (e.g. 20D funding for Liquidity) should carry more weight than inputs that merely confirm (1D noise). Equal weights treat “1D BTC tick” and “20D curve funding” as equally important — that violates the economics of transmission.

**Why not statistical weights at launch?** With &lt;60 live desk sessions, optimized weights **overfit** and destroy trust. The production choice is **expert-judgment hybrid v1**: fixed weights documented per stage, with statistical overlays reserved for validation later.

**Regime bands** (ordinal, not cardinal precision):

| Band | Score | Desk meaning |
|------|-------|--------------|
| Healthy | ≥ 80 | Warehouse-friendly; full policy size |
| Constructive | ≥ 65 | Carry and beta within policy |
| Fragile | ≥ 50 | Tactical only; reduced carry |
| Broken | &lt; 50 | Client structures / convexity; block new calendar risk |

Treat 41 vs 43 as **meaningfully different** but do not pretend 41.2 vs 41.8 is signal.

## 3. Horizon marks and lookbacks

Tracer horizons map desk time:

| Tracer | Desk label | Role in math panel |
|--------|------------|-------------------|
| d1 | 1D | Impulse / today |
| d5 | 5D | Weekly trend |
| d20 | 20D | ~30D practical window (highest weight on several stages) |
| d60 | 60D | ~3M regime persistence |

**Lookback panels (30D / 3M / 1Y)** are **counterfactual composites**: “What would score have been if recent marks had not deteriorated?” They support **causal narrative**, not backtested history. An LLM must not describe them as stored time series.

## 4. Weakest link and tie-break

**Weakest link** = minimum stage score; tie-break order (financing chain priority):

```text
Liquidity → Credit → Breadth → High-Beta → Basis
```

**Theory:** If two stages tie at 50, the desk sizes off **liquidity first** because leverage and carry quality degrade before participation metrics matter for calendar books.

## 5. BTC / ETH implementation layer

Implementation is **conditional on ladder state**, not on spot price:

- **BTC:** Tradable in **reduced-risk** structures when fragile (client facilitation, front-curve carry).
- **ETH:** **More selective than BTC** — same ladder, tighter sizing; basis less durable.
- **Both:** Weak liquidity + credit + basis → avoid prop warehousing and levered carry.

This is **constraint logic**, not alpha logic.

---

# Part II — Junior analyst teach-in

## A. Your job in one sentence

**Translate transmission state into size and structure — fast, honestly, without confusing marks for narrative.**

## B. Open the tools (navigation)

| Step | Action | Path |
|------|--------|------|
| 1 | Daily console | `Whinfell_Transmission_Ladder_Deep_Dive.command` or TC → **Deep Dive** |
| 2 | Operator console | `Whinfell_Transmission_Control.command` |
| 3 | After CSV chain | TC → **Import Latest Hydration Bundle** → review **Suggested Tracer** → Accept/Dismiss → Save |

**Deep Dive read order (memorize):**

1. **Decision band** — Regime · Weakest · BTC · ETH · Ladder avg · As of  
2. **Transmission ladder** — five cards (trigger → state → evidence)  
3. **Stage score math** — five always-visible breakdowns  
4. **Failure points** — ranked bottlenecks  
5. **BTC / ETH** — posture + trade menu tables  
6. **Playbook** — what changes posture if ladder improves / deteriorates  

**10-second scan:** Decision band only.  
**60-second scan:** Band + heat strip + failure #1 + BTC/ETH posture chips.  
**3-minute read:** Open weakest-link math card + both trade menus.

### B.1 Gate vs China SQ3 (do not conflate)

| Surface | What it controls |
|---------|------------------|
| **BTC gate (`gate.code`)** | Global Whinfell Score + Transmission Health only — `blocked` / `reduced` / `open` thresholds unchanged in v1.1 |
| **SQ3 policy** | China policy composite (Policy STR + State IMP + Growth IMP) — feeds **China final (adj.)** handicap multiplier |
| **SQ3 caution overlay** | When SQ3 &lt; 50 and Global score ≥ 50, TC shows **Allowed · China Caution** or **Tight + China Caution** on `displayLabel` — **not** a gate floor change |

China ladder handoff block (append to WTM EXPORT v2.1):

```text
--- CHINA LADDER EXPORT v1.1 ---
China Raw Score: …
China Final Score: …
China Final Band: …
SQ3 Policy Score: …
Weakest China Stage: …
Key China Observation: …
```

Grok `master_state.china_ladder` mirrors the same five scalars plus weakest stage name for operator prompts.

## C. Mental math workbook

### C.1 Mark → subscore (instant)

```text
up   → 75
flat → 50
down → 25
```

### C.2 One component contribution

```text
contrib = round(weight% × subscore / 100)
```

**Example:** 40% weight × 25 subscore → 40 × 25 / 100 = **10 points**

### C.3 Liquidity & Rates (fixture walkthrough)

Weights: 15% · 20% · **40%** · 25% on 1D, 5D, 20D, 60D marks.

| Input | Wt | Mark | Sub | Contrib |
|-------|-----|------|-----|---------|
| 1D funding | 15% | flat | 50 | 8 |
| 5D funding | 20% | flat | 50 | 10 |
| 20D curve | **40%** | **down** | **25** | **10** |
| 60D regime | 25% | flat | 50 | 13 |
| **Total** | | | | **41** |

**Mental shortcut:** Only 20D is down. Lost ~(50−25)×40% ≈ **10 pts** vs all-flat → 50 − 10 ≈ **40** (actual 41 after rounding).

**Band:** 41 → **Broken** (&lt;50). Desk: no new calendar risk; client-only if forced.

### C.4 Credit Confirmation (fixture)

5D **down** on 30% weight → lose ~7–8 pts vs all-flat → score ~**43**.

### C.5 All-flat stages (Breadth, High-Beta, Basis)

All marks flat → all subs 50 → **score 50** (Fragile threshold). Mental check: 50×100% = 50. ✓

### C.6 Horizon delta (30D vs today)

If today = 41 and 30D composite = 51 → **−10 vs now** on chip.  
**Causal sentence you should be able to say:** “20D funding mark rolled from flat to down; at 40% weight that’s roughly ten points on the composite.”

### C.7 Tracer cross-check

Parallel formula (in math panel footer):

```text
net = (#up marks) − (#down marks)     over {1D,5D,20D,60D}
tracerScore = round((net + 4) / 8 × 100)
```

Fixture liquidity: one down → net = −1 → tracer ≈ **38**. Expert composite = **41**.  
**Best practice:** If composite and tracer diverge by &gt;5 pts, note it in Key Observation and re-check marks before sizing.

## D. Best practices (desk)

### Do

- Read **trigger** before **evidence** — triggers change book posture; evidence explains why.
- Size off **weakest link**, not favorite narrative (e.g. “BTC looks strong”).
- Write Key Observation as **one constraint + one action** (“Liquidity 41, front-curve client rolls only”).
- Import hydration **before** China open / US open if marks changed overnight.
- Use trade menu **Status** column: Supported / Tactical / Avoid — not your gut.

### Do not

- Do not treat **51 vs 49** as noise-free precision.
- Do not warehouse basis because “ETH basis looks rich” when liquidity &lt; 50.
- Do not paste Koyfin/Barchart CSV into the HTML — use the hydration pipeline.
- Do not edit localStorage to “fix” scores — fix marks in Tracer and re-save.
- Do not confuse **Fragile Risk-On** (regime tag) with **Fragile band** (stage score) — related but not identical.

## E. Daily workflow (junior checklist)

```text
□ Morning: run_csv_download.py daily OR scripts/whinfell_morning_collect.sh
□ TC: Import hydration → Accept/Dismiss tracer → Save State
□ Deep Dive: confirm weakest link matches your Koyfin/Barchart read
□ If marks changed: update horizon overrides in TC tracer table
□ Export WTM / Grok payload if senior review required
□ EOD: note which trigger would unlock size tomorrow
```

## F. Dig deeper — Koyfin

**Purpose on this desk:** Macro and cross-asset **confirmation** for ladder stages 1–3.

| Ladder stage | Koyfin dashboard (wired name) | What to verify | Export |
|--------------|------------------------------|----------------|--------|
| Liquidity & Rates | `WTM-Rates-Credit` | T10Y2Y, DGS10, front-end move vs 20D | ⋮ → Export CSV |
| Credit Confirmation | `WTM-Credit-Confirmation` | HYG, LQD, HYG/LQD ratio trend | ⋮ → Export CSV |
| Equity Breadth | `WTM-Equities-Breadth` | IWM vs SPY, sector participation | ⋮ → Export CSV |
| High-Beta / BTC | `Whinfell-Daily-TimeSeries` | BTCUSD, IBIT, SPY aligned dates | Download Available Data |
| China overlay | `WTM-China-Policy` | policy / state / growth impulses | ⋮ → Export CSV |

**Navigation tips:**

- Home: `https://app.koyfin.com/`
- Assist URLs in `whinfell_pipeline/desk_urls.yaml` (e.g. `USGG2Y10Y`, `HYG.US`, `IBIT.US`).
- **Must have Date column** on daily export — not snapshot-only watchlists.
- Compare **5D and 20D direction** on your chart before setting tracer marks.

**Junior exercise:** Open HY OAS and T10Y2Y. If 20D trend disagrees with your liquidity 20D mark, fix the mark *before* the team meeting — not during it.

## G. Dig deeper — Barchart

**Purpose:** Futures curve, basis, spreads — ladder stages **4–5** and BTC/ETH implementation.

| Ladder stage | Barchart screen | What to verify | Export |
|--------------|-----------------|----------------|--------|
| High-Beta / BTC | `WTM-Futures-Intraday` / crypto futures | BTC vs ES beta, session leadership | Download CSV |
| Basis & Term Structure | `WTM-BTC-Basis` / spreads tab | Calendar spreads, contango richness | Download CSV |
| History / vol context | `WTM-Futures-Daily` | Nearby historical, roll behavior | Historical download |

**Contract literacy (exam-level):**

| Shortcut | Asset | Filename root |
|----------|-------|---------------|
| BT1 | Bitcoin CME | `btm26_*` |
| ER1 | **Ether** CME (not Russell) | `erm26_*` |
| ES1 | E-mini S&P | `esm26_*` |

**Five file types** — classify before parsing (`Perplexity_Barchart_Koyfin_Playbook.md` §2):

1. Historical daily nearby  
2. Intraday prices (curve)  
3. Spreads  
4. Options side-by-side (Call/Put duplicate columns trap)  
5. Vol/Greeks side-by-side  

**Junior exercise:** Pull `bitcoin-futures-prices-intraday` CSV. Confirm near vs next month **Change** direction matches your basis stage 5D/20D marks.

## H. When to escalate

| Situation | Escalate to senior |
|-----------|-------------------|
| Composite vs tracer diverge &gt;5 pts | Yes — marks may be wrong |
| Weakest link flipped overnight | Yes — posture change |
| Whinfell Score &lt; 50 + client wants calendar size | Yes — gate conflict |
| Freshness status not `fresh` | Yes — do not trade off stale hydration |
| You cannot explain 30D delta in one sentence | Yes — teach-in gap |

---

# Part III — LLM operational specification

## 1. System manifest

```yaml
repo: Whinfell_BUILD_Cousins
primary_html:
  transmission_control: 08_Deliverables/Whinfell_Transmission_Control.html
  deep_dive: 08_Deliverables/whinfell-transmission-ladder-deep-dive.html
hydration: data/hydration/latest.json
local_storage_key: whinfell_transmission_control_v1
stages:
  - { id: liquidity, key: liquidity_rates, name: "Liquidity & Rates" }
  - { id: credit, key: credit_confirmation, name: "Credit Confirmation" }
  - { id: breadth, key: equity_breadth, name: "Equity Breadth" }
  - { id: highbeta, key: highbeta_btc, name: "High-Beta / BTC" }
  - { id: basis, key: basis_term_structure, name: "Basis & Term Structure" }
stage_rank_tiebreak: [liquidity, credit, breadth, highbeta, basis]
```

## 2. Data precedence (deep dive loader)

```text
1. localStorage[whinfell_transmission_control_v1]  → tracer.horizons + intake
2. fetch data/hydration/latest.json               → suggested_tracer + global
3. FIXTURE embedded in HTML
```

**LLM rule:** Always call `normalizeHorizons()` semantics — each stage must have d1,d5,d20,d60 ∈ {up,flat,down}. Missing → flat.

## 3. Scoring functions (normative)

```python
MARK_SCORE = {"up": 75, "flat": 50, "down": 25}

def contrib(weight_pct: int, mark: str) -> int:
    return round(weight_pct * MARK_SCORE[mark] / 100)

def stage_score(components: list[tuple[int, str]]) -> int:
    return sum(contrib(w, m) for w, m in components)

def score_band(s: int) -> str:
    if s >= 80: return "Healthy"
    if s >= 65: return "Constructive"
    if s >= 50: return "Fragile"
    return "Broken"

def weakest(stages: list[dict]) -> dict:
    return min(stages, key=lambda s: (s["score"], STAGE_RANK[s["id"]]))
```

**Expert weights v1** — see `STAGE_MODELS` in deep dive HTML JS; must sum to 100 per stage.

## 4. Rendering contract (LLM must not violate)

| Rule | Requirement |
|------|-------------|
| DOM | `createElement` + `textContent` only for dynamic copy |
| No markdown | No `**`, `###`, pipe tables, `<strong>` for labels |
| Math visibility | All 5 stages: full math in `#mathStageList`, not collapsed |
| Tables | Native `<table>` for components and trade menus |
| Weakest | Single source: `ranked[0]` after score + tie-break |
| Causal text | Max 2 lines per horizon pair; cite mark + weight |

## 5. LLM read protocol (analogous to human 10s/60s/3m)

```text
PASS_1 (10s): decision_band → regime, weakest, btc_posture, eth_posture
PASS_2 (60s): failure_rows[0], heat_strip min score, trade_menu Supported count
PASS_3 (3m): math_stage_card[weakest_id] full component table + 30D/1Y deltas
OUTPUT: posture recommendation MUST cite weakest stage score and band
```

## 6. Collection agent binding

When tasked with **data refresh** (not UI):

```bash
cd ~/Desktop/Whinfell_BUILD_Cousins
python3 run_batch_collect.py plan      # read-only checklist
python3 run_batch_collect.py run --window today
```

URLs: `whinfell_pipeline/desk_urls.yaml`  
Drop dir: `~/Downloads/whinfell_drop`  
**Do not** transform vendor CSV in-browser — Python stages WTM rows.

## 7. LLM QA checklist (honest — render scrape)

```text
FAIL if body text contains: **, | TRADE |, |---|
FAIL if math_stage_cards < 5
FAIL if any math card missing: "Weighted total", "Score =", "30D", "1Y"
FAIL if weakest link text disagrees with failure_rows[0].name
FAIL if <strong> or <details> count > 0
PASS only if all above clear on desktop 1440×900 AND mobile 390×844
```

## 8. Grok / operator prompt alignment

When generating desk narrative, use `Whinfell_Grok_Operator_Prompt.txt` structure:

1. Plain English before tool language  
2. Map to Whinfell Score, Transmission, Regime, Gate, Execution Intent  
3. WHY bullets: band context + driver anecdote + threshold trigger  
4. Score &lt; 50 → calendar arb **BLOCKED** unless senior override documented  

**LLM must not** invent weights or marks not present in hydration/tracer.

---

# Part IV — Tool enhancement opportunities

Prioritized by desk value × implementation clarity.

| Priority | Enhancement | Theory / practice basis | Owner surface |
|----------|-------------|-------------------------|---------------|
| P0 | **Historical mark storage** — real 30D/3M/1Y scores from Parquet, not counterfactual | Eliminates lookback approximation; enables honest backtest | Pipeline + deep dive |
| P0 | **2.2e raw→WTM transform** — Barchart/Koyfin CSV → tracer marks auto-suggest | Reduces manual mark error; Freshens China open workflow | `staged_csv.py` |
| P1 | **Component live values** from Koyfin/Barchart fields (not only up/flat/down) | Richer subscores while keeping mental math | Hydration schema v2 |
| P1 | **Divergence alert** when \|composite − tracer\| &gt; 5 | Catches mapping bugs | TC + deep dive |
| P2 | **Regime-adaptive weights** (validation overlay only) | Post-60-session backtest | Methodology card v2 |
| P2 | **ETH-specific basis panel** separate from BTC | ETH implementation already more selective | Deep dive ETH card |
| P3 | **China SQ3 → ladder attribution** link | Industrial policy acceleration → credit/breadth | TC intake |
| P3 | **Export desk note PDF** (print CSS already partial) | Client-facing memo | Deep dive |

**Junior-friendly enhancement requests** (good first tickets):

- Tooltip on each component row: “where to see this in Koyfin”  
- One-click open `desk_urls.yaml` assist URL per stage  
- “Explain this score” plain-English sentence under composite total  

---

# Appendix A — Stage weight reference (expert v1)

### Liquidity & Rates
`15%·1D + 20%·5D + 40%·20D + 25%·60D`

### Credit Confirmation
`20%·1D + 30%·5D + 30%·20D + 20%·60D`

### Equity Breadth
`25%·1D + 25%·5D + 30%·20D + 20%·60D`

### High-Beta / BTC
`25%·1D + 25%·5D + 30%·20D + 20%·60D`

### Basis & Term Structure
`25%·1D + 20%·5D + 30%·20D + 25%·60D`

---

# Appendix B — LLM machine-readable summary (JSON)

```json
{
  "teach_in_version": "1.0",
  "production_weighting": "expert_judgment_hybrid_v1",
  "mark_subscore_map": { "up": 75, "flat": 50, "down": 25 },
  "bands": [
    { "name": "Healthy", "min": 80 },
    { "name": "Constructive", "min": 65 },
    { "name": "Fragile", "min": 50 },
    { "name": "Broken", "min": 0, "max_exclusive": 50 }
  ],
  "weakest_tiebreak_order": ["liquidity", "credit", "breadth", "highbeta", "basis"],
  "fixture_weakest": { "name": "Liquidity & Rates", "score": 41, "band": "Broken" },
  "read_order": ["decision_band", "ladder", "scoring_math", "failure", "btc_eth", "playbook"],
  "data_sources": {
    "koyfin": "whinfell_pipeline/desk_urls.yaml#koyfin",
    "barchart": "whinfell_pipeline/desk_urls.yaml#barchart",
    "hydration": "data/hydration/latest.json"
  },
  "blocked_actions_when_score_lt_50": [
    "new_calendar_warehouse",
    "aggressive_prop_basis",
    "levered_carry_without_senior_override"
  ]
}
```

---

# Appendix C — Glossary (junior)

| Term | Meaning |
|------|---------|
| **Transmission** | Risk moving through macro → credit → equities → beta → crypto basis |
| **Tracer mark** | up / flat / down on a horizon — your distilled chart read |
| **Composite** | Weighted average of mark subscores — the stage number |
| **Weakest link** | Lowest composite; sizes financing-sensitive books first |
| **Hydration** | `latest.json` bundle feeding TC and Deep Dive |
| **Posture** | Supported / Tactical / Avoid — not a price view |
| **WTM** | Whinfell Transmission Model export format for agents |

---

*End of teach-in. For CSV collection agents, continue to `Perplexity_Comet_Collection_Instructions.md`. For daily ops, continue to `Whinfell_Expanded_Operators_Guide_v1.4.md`.*