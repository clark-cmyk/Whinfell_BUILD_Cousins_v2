# Whinfell BUILD Cousins Operating Plan v1.0

**Project:** Whinfell Transmission Map  
**Team:** BUILD Cousins (Parallel Execution Team)  
**Version:** 1.0  
**Date:** June 26, 2026  
**Status:** Draft for Approval

---

## 1. Goal

Support the core Whinfell Transmission Map build by owning logic, documentation, fallback tools, and testing. This allows the primary builder (user + Comet) to stay focused on constructing the live dashboard inside Comet + Koyfin/Barchart without interruption.

The BUILD Cousins operate as a **parallel, semi-autonomous team** that delivers high-quality supporting artifacts while the main build progresses.

---

## 2. Operating Principles

- **Autonomous Mode**: Once this plan is approved, the Cousins begin work on Priority 1 tasks immediately without waiting for daily instructions.
- **Quality Gate**: Every major deliverable must pass self-review → peer review → Arena Team review before being marked complete.
- **Transparency**: All work is logged in the shared folder structure with clear status.
- **No Blocking**: The Cousins never block the main build. If clarification is needed, they note it and continue with other tasks.
- **Version Control**: All documents use semantic versioning and are stored in the `01_Strategy_Docs` folder.

---

## 3. Team Structure & Roles

| Role | Primary Responsibility | Assigned To |
|------|------------------------|-------------|
| **Integration Dynamo (Lead)** | Score calculation logic, technical coordination | BUILD Cousins Lead |
| **Forge Master** | Documentation quality, Quick Reference Card, prompt library hygiene | BUILD Cousins |
| **Risk Warden (Support)** | Risk sidebar logic, fallback tool validation | Arena Team support |
| **Clarity Sentinel** | Testing log structure, usability of deliverables | BUILD Cousins |
| **Visual Vanguard (Support)** | Visual consistency of fallback Excel/Sheets | As needed |

---

## 4. Task List & Priorities

### Priority 1 – Immediate (Start Immediately)

| # | Task | Description | Deliverable | Target Completion |
|---|------|-------------|-------------|-------------------|
| **C1** | Whinfell Credit Confirmation Score – Full Calculation Logic | Create clean, documented formula with exact weighting, data sources, calculation steps, and handling for missing fields. Include worked example using live data. | Markdown + Excel example in `04_Score_Calculation/` | 2–3 days |
| **C2** | Fallback Excel / Google Sheet Dashboard | Build a simple, usable spreadsheet that replicates Credit Confirmation Inputs + Whinfell Score + basic Basis conditions as backup. | Working .xlsx file + instructions in `05_Fallback_Tools/` | 3–4 days |
| **C3** | Exact Series & Ticker Master List | Definitive list of every ticker/series used in the workspace (Koyfin + Barchart) with preferred time windows and known limitations. | Clean reference table in `07_Reference_Materials/` | 1–2 days |

### Priority 2 – Short Term (Within 7–10 Days)

| # | Task | Description | Deliverable | Target Completion |
|---|------|-------------|-------------|-------------------|
| **C4** | Test the 6 Refined Agentic Prompts | Run all 6 prompts daily for 5–7 trading days using the live workspace. Log accuracy, usefulness, and recommended tweaks. | Testing log + prompt improvement recommendations in `06_Testing_Logs/` | Ongoing |
| **C5** | Quick Reference Card (One-Pager) | Create a clean, printable one-page desk cheat sheet containing the 6 prompts, score interpretation bands, morning workflow, and key invalidation rules. | Professional PDF in `08_Deliverables/` | 4–5 days |

### Priority 3 – Deferred

- Gross Exposure / Risk sidebar logic (only after core build is stable)
- Any future API/integration bridges or automation

---

## 5. Review & Approval Process (Arena)

All Priority 1 and 2 deliverables must follow this sequence:

1. **Self Review** – Cousin who created it reviews for completeness and clarity.
2. **Peer Review** – Another Cousin reviews.
3. **Arena Review** – Relevant Arena member reviews for strategic alignment and quality.
4. **Final Sign-off** – TempLibby marks as complete.

---

## 6. Communication Rules

- The Cousins work primarily in this folder structure.
- Major updates or blockers are posted in the shared workspace notes.
- Questions that block progress are logged with a clear “BLOCKER” tag.
- Daily progress is summarized in `Progress_Log.md` inside `01_Strategy_Docs/`.

---

## 7. Success Criteria

- The Whinfell Credit Confirmation Score has a clear, documented, and testable calculation method.
- A reliable fallback tool exists so the desk can continue operating if Comet/Koyfin is unavailable.
- All 6 refined prompts have been tested in real conditions with documented results.
- The main builder can focus on the Comet build without being pulled into logic or documentation work.

---

## 8. Approval

**Plan Status:** APPROVED

**Approved by:** _______________________________     **Date:** _______________

Once approved, the BUILD Cousins will begin work on **C1, C2, and C3** immediately.

---

*Document Version: 1.0*  
*Last Updated: June 26, 2026*

**Approved by:** TempLibby (Template Team)     **Date:** June 26, 2026
**Activation Note:** BUILD Cousins officially activated. Work on C1 begins immediately.
**Approved by:** TempLibby (Template Team)     **Date:** June 26, 2026
**Activation Note:** BUILD Cousins officially activated. Work on C1 begins immediately.
**Approved by:** TempLibby (Template Team)     **Date:** June 26, 2026
**Activation Note:** BUILD Cousins officially activated. Work on C1 begins immediately.

**Approved by:** TempLibby (Template Team)     **Date:** June 26, 2026
**Activation Note:** BUILD Cousins officially activated. Work on C1 begins immediately.
