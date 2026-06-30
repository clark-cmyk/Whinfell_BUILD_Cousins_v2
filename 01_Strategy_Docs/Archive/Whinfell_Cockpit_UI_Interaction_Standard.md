# Whinfell Cockpit UI Interaction Standard

**Version:** 1.0  
**Date:** June 29, 2026  
**Authors:** BUILD Cousins (Clarity + Bridge)  
**Status:** Locked — applies to all Phase 2+ Transmission Control UI work  
**Primary surface:** `08_Deliverables/Whinfell_Transmission_Control.html`

---

## Authority statement

Whinfell Transmission Control must be built as a **world-class operating cockpit** for two-way use:

1. **Trading decisions** in live desk conditions  
2. **Product-development / system-design decisions** while the framework evolves

This is not a dashboard, not a BI surface, and not a presentation layer. It is a cockpit. The operator must feel inside one coherent machine that supports action, review, adjustment, comparison, and development in the same environment.

**Closing line (non-negotiable framing):**

> Build Whinfell like a cockpit with memory, authority, and reversibility — not a dashboard with panels.

---

## What the console already is

The current console already contains:

| Layer | Examples |
|-------|----------|
| Regime / permissioning | Whinfell Score, Transmission, Gate State, Shock, Freshness |
| Operator inputs | Confidence, execution intent, key observation |
| Provenance | Import/export actions with lineage awareness |
| Desk workflow | Prompt and execution layers tied to actual workflows |

The UI must behave like a **command environment** where:

- the system explains itself  
- the operator can interrogate it  
- the operator can adjust inputs  
- the product can evolve without the interface fragmenting  

---

## Degraded vs neutral — trust rule (behavioral contract)

Every **degraded** or **non-authoritative** state must be **visibly distinguishable** from a real **neutral** state. Ambiguity is what makes advanced tools feel second-rate.

This applies to:

| Signal | Must not look like neutral |
|--------|---------------------------|
| Freshness degrade | Stale/aging ≠ “all clear” |
| Provenance gap | Missing lineage ≠ authoritative read |
| `flows_meta` / sponsorship | `unavailable` / `fallback_1d` / `partial` ≠ supportive/neutral verdict chrome |
| Compare mode gaps | Missing node data ≠ flat “no signal” |
| Partial hydration | Incomplete bundle ≠ full session |
| Imported sidecars | Degraded ingest mode visible at import + rail |

**Implementation rule:** render meta chip / degrade banner **before** verdict or aggregate lines; unavailable blocks use collapsed placeholder, not neutral badge styling.

---

## Core interaction standard

Every interaction should reinforce four properties:

| Property | Requirement |
|----------|-------------|
| **Speed** | Minimal friction moving through nodes, modes, and evidence |
| **Stability** | Layout, controls, and state do not jump or reset unexpectedly |
| **Legibility** | Hierarchy is obvious — eye knows first, second, third read |
| **Bidirectionality** | Supports reading outputs *and* shaping system logic |

---

## Non-negotiable principles

### 1. One machine, not many pages

Moving between nodes, focus modes, prompts, and compare views should feel like turning within the same machine. The shell remains stable; only the analytical payload changes.

- No “screen hopping”  
- Flip navigation, full-screen “Here’s Why,” compare mode, and side modules **preserve context and state**

### 2. Read → decide → act → refine

Each node and each global section supports:

```
read signal → inspect reasoning → check evidence → decide → refine system / note observation
```

The interface must never trap the user in passive viewing. Every important read connects naturally to execution posture or product refinement.

### 3. Context-preserving depth

Expand detail via focus layers and structured expansion — not disruptive modals or page changes.

The operator must always know:

- where they are  
- what node they are in  
- what changed  
- how to return without losing place  

### 4. Calm over flashy

Motion is functional, short, and low-volatility. Color communicates state, not branding excitement.

Use emphasis only for:

- active warnings  
- degraded freshness  
- divergence  
- gating  
- actual decision thresholds  

Do not use motion or color for decoration.

### 5. Development mode is first-class

Whinfell is actively shaped, not only consumed. The interface must support:

- provenance inspection  
- export / import workflow  
- state save / restore  
- explanation audit  
- schema-aware modules  
- future extensibility without visual drift  

Assume the operator is also a **designer of system logic**, not only a consumer of output.

---

## What world-class means here

A world-class cockpit in this context should feel:

- as **fast** as a trading workstation  
- as **legible** as a high-end research terminal  
- as **structured** as a mission-control interface  
- as **extensible** as an internal product platform  

Serious, disciplined, intentional. Every panel exists for a reason; every interaction is considered.

---

## Specific UI reminders (Phase 2+)

| Area | Standard |
|------|----------|
| Global band | Regime/governance band persistent and authoritative |
| Node flip | Instantaneous and stateful — no layout reflow |
| “Here’s Why” | True focus mode for deep reading and audit |
| Operator inputs | First-class controls, not tucked secondary forms |
| Compare mode | Diagnostic instrument, not layout gimmick |
| Degradation | Freshness, provenance, `flows_meta` as interaction-level signals — not footnotes |
| Workflows | Export, prompts, hydration feel integrated — not bolted on |
| Funds Flow card (PR-4) | Read-only confirmation layer; regime-first render order: meta chip → degrade banner → verdict → aggregate → ETFs → interpretation |

---

## Ship gate — ask before every major UI change

| Question | Must be yes |
|----------|-------------|
| Does this make the cockpit **faster** to operate? | ✓ |
| Does it **preserve context**? | ✓ |
| Does it strengthen **trust** in the system? | ✓ |
| Does it help both **live trading** and **product development**? | ✓ |
| Does it feel like a real **operator cockpit**, not a dashboard? | ✓ |

If any answer is no — redesign.

---

## Phase 2 module alignment

| Module | Cockpit rule |
|--------|--------------|
| `node_cockpits.*` | Node flip swaps payload inside stable shell; fixed-height rail sections |
| `funds_flows` / `FundsFlowSponsorshipCard` | L2 read-only; `flows_meta` chip before verdict; unavailable ≠ neutral styling |
| Hydration import | Provenance + version visible; no silent overwrite of operator state |
| WTM EXPORT | Integrated action, not external report dump |

---

## References

- `08_Deliverables/Whinfell_Transmission_Control.html` — live console  
- `01_Strategy_Docs/Phase2_Node_Cockpit_Data_Model.md` — node payload contract  
- `01_Strategy_Docs/Phase2_Funds_Flow_Sponsorship_Design.md` — flow card placement and visual rules  
- `01_Strategy_Docs/Phase2_Flows_Implementation_Spec.md` — `flows_meta` degrade contract (UI must distinguish unavailable vs neutral)