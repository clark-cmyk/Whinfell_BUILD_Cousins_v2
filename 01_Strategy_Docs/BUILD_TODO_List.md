# BUILD Cousins - TODO List

**Maintained by:** BUILD Cousins  
**Last Updated:** June 29, 2026 (Phase 1 verified · Phase 2 prep)  
**Purpose:** Track all active and planned work for the Whinfell Transmission Map support track.

---

## Current Status

| # | Deliverable | Priority | Status | Owner | Notes |
|---|-------------|----------|--------|-------|-------|
| **ARCH** | WTM Data Architecture (Koyfin + Barchart) | **High** | **Plan shipped** | Integration Dynamo | `01_Strategy_Docs/WTM_Data_Architecture_Build_Plan.md` · `whinfell_pipeline/data_dictionary.yaml` |
| **ARCH-1** | `source_router.py` unified ingest routing | High | **Open** | Integration Dynamo | Depends on dictionary v1.0.0 |
| **ARCH-3** | Clark: WTM-Import-Core Koyfin watchlist | High | **Open** | Clark | Replaces interim WhinPump-only canonical |
| **ARCH-4** | Barchart core batch export in manifest | Medium | **Open** | Integration Dynamo | 16-symbol core set in dictionary |
| **Desk feedback** | Transmission Control rollout | High | **Collecting** | Bridge | `Desk_Feedback_Log.md` |
| **Phase 2.1** | Refinements post-feedback | Medium | **Standing by** | Bridge + Edge | WTC-2.0 import · scenario loop |
| **Phase 2.2 Final** | Desk validation of browser blueprint | Medium | **Collecting** | Bridge | Blueprint + hydration UX shipped |
| **2.2e** | Raw vendor CSV → WTM observation row transform | **High** | **Shipped** | Integration Dynamo | `whinfell_pipeline/raw_csv_transform.py` — auto on stage |
| **Desk ops** | Document pre-stage rename in Operator Guide v1.5 | Medium | **Open** | Clarity | `normalize_whinfell_drop.sh` + canonical name table |
| **Desk ops** | Clark first live CSV drop — report to TempLibby | High | **In progress** | Bridge | Re-test with Master DD v1.0 canonical names |
| **Phase 1** | Master Data Dictionary v1.0 + naming rectification | **High** | **Complete · Verified** | Bridge + Precision | 104 tests PASS · 0 naming violations · `194506a` |
| **Phase 2 prep** | Node cockpit data model spec | High | **Locked v0.2** | Blueprint | `Phase2_Node_Cockpit_Data_Model.md` · decisions applied · implementation next |
| **Phase 2** | Node architecture redesign (5 trading cockpits) | High | **Planned** | Bridge + Edge + Clarity | Blocked on data model sign-off + desk validation |
| **Phase 3** | TC interface (full-screen Why, flip nav, margin module) | Medium | **Planned** | Clarity + Safeguard | Blocked on Phase 2 |
| **Phase 4** | Validation & reliability gate | Medium | **Planned** | Hammer + Precision | After Phase 3 |

---

## Report for TempLibby (June 28, 2026)

**What happened:** Clark ran the daily CSV chain against real Barchart/Koyfin exports in `~/Downloads/whinfell_drop`. All 7 files were **quarantined** — staged classifier rejected native export filenames.

**Root cause (layer 1 — fixed):** Pipeline requires canonical names (`rates_20260628_1119.csv`, `futures_daily_20260628_1015.csv`, `btc_basis_20260628.csv`, etc.), not Barchart/Koyfin default download names.

**Mitigation shipped:** `scripts/normalize_whinfell_drop.sh` — renames desk drop files to contract before `run_csv_download.py stage`.

**Root cause (layer 2 — open):** Even after rename, **header validation fails**. Raw vendor CSVs use market-data columns; pipeline expects single-row **WTM observation** exports (`timestamp`, `whinfell_score`, `near_month`/`basis_spread`, etc.) per `whinfell_pipeline/examples/staged/`.

**Desk workaround today:** Use Transmission Control **WTM EXPORT v2.1** import path, or export WTM-shaped CSVs from saved Comet/TC views — not raw Barchart/Koyfin dumps alone.

**Next build items:** (1) raw→WTM row converter in daily chain, or (2) Operator Guide v1.5 clarifying export shape + rename step, or (3) relax staged header check for raw files with adapter-side transform (design TBD with Perplexity).

**Also fixed June 28:** Desktop Daily Launcher double-click — redeployed `Whinfell Daily AM.app` (AppleScript) + updated `.command` files.

---

## Production Rollout

| Item | Status |
|------|--------|
| Transmission Control Phase 2.2 Final | **Deployed to desk** |
| Quick Reference Card v1.4 | **Distributed** |
| Expanded Operator's Guide v1.4 | **Master reference** |
| Comet Browser Operations Blueprint | **Shipped** |
| Daily CSV chain (`run_csv_download.py`) | **Live — `verify_2_2_final` PASS** |
| Whinfell Daily Launcher (`Whinfell_Daily_Launcher.py`) | **Shipped — one-click desk tool** |
| Pre-stage rename (`scripts/normalize_whinfell_drop.sh`) | **Shipped — filename contract only** |
| Raw vendor CSV header transform (2.2e) | **Shipped** |
| WTM data dictionary v1.0.0 + ARCH build plan | **Shipped** |
| C4 Prompt Testing | **Signed off — 20/20** |
| TempLibby production sign-off (Phase 2) | **Approved** |

---

## Completed

| # | Deliverable | Completed On | Notes |
|---|-------------|--------------|-------|
| Plan | BUILD Cousins Operating Plan v1.0 | June 26, 2026 | Approved |
| C1–C3 | Score logic, Excel, tickers | June 26, 2026 | Signed off |
| C4.5 | Operator Dashboard | June 26, 2026 | Legacy cockpit |
| **Transmission Control** | Phase 0 / 1.2 / Phase 2 | June 26, 2026 | `0ddb7f1` · `c9d9b63` · `1a33bee` |
| **C4** | Prompt Testing | June 26, 2026 | 20/20 PASS |
| **C5** | Quick Reference Card v1.2 | June 26, 2026 | Print-ready |
| **Phase 2.2b** | Hybrid Signal Tracer + progressive disclosure | June 27, 2026 | `verify_2_2b_goal` PASS |
| **Phase 2.2c** | Staged CSV folder + `ingest --staged` | June 27, 2026 | `test_staged_2_2c` PASS |
| **Comet handoff** | Adapter package to Comet | June 27, 2026 | `Comet_Adapter_Handoff.zip` |
| **Phase 2.2d** | Comet CSV Download Runbook (`run_csv_download.py`) | June 27, 2026 | 12 tests PASS · E2E verified |
| **C5 / Ops** | Quick Reference Card + Operator Guide v1.4 | June 27, 2026 | Daily CSV chain on desk |
| **Phase 2.2 Final** | Browser blueprint + hydration UX + E2E verify | June 27, 2026 | `verify_2_2_final` PASS |
| **Daily Launcher** | `Whinfell_Daily_Launcher.py` + `whinfell_daily_am.sh` | June 27, 2026 | Tkinter one-click AM · live log |
| **Session** | BUILD Cousins agent role adoption (`/arena /role /plan`) | June 29, 2026 | `BUILD_Cousins_Session_Activation.md` · 7/7 canon tests PASS · `25ed812` |
| **Phase 1** | Master Data Dictionary v1.0 locked + naming alignment | June 29, 2026 | `data_dictionary.yaml` · TC badge · phased plan |
| **Phase 1 verify** | Evidence scripts + disk-backed badge test | June 29, 2026 | `generate_phase1_evidence.py` · `dd_badge_file_evidence.mjs` · `194506a` |
| **Phase 2 prep** | Node cockpit data model (planning only) | June 29, 2026 | `Phase2_Node_Cockpit_Data_Model.md` · `877524a` |

---

## Desk Open Commands

```bash
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Transmission_Control.html
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Quick_Reference_Card_v1.4.docx
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Expanded_Operators_Guide_v1.4.md
```

**One-click morning (preferred):**

```bash
cd ~/Desktop/Whinfell_BUILD_Cousins
python3 Whinfell_Daily_Launcher.py
```

**Pre-stage rename (before daily chain, if using raw Barchart/Koyfin downloads):**

```bash
cd ~/Desktop/Whinfell_BUILD_Cousins
scripts/normalize_whinfell_drop.sh ~/Downloads/whinfell_drop
```

**CLI fallback:**

```bash
cd ~/Desktop/Whinfell_BUILD_Cousins
./whinfell_daily_am.sh
# Then: Transmission Control → Import Latest Hydration Bundle → data/hydration/latest.json
```

**Verify:**

```bash
python3 -m whinfell_pipeline.verify_2_2_final
```

**Ship commits:** P1.2 `c9d9b63` · Sprint `1a33bee` · Phase 2.2 Final (pending commit)

---

## Notes
- **June 29, 2026** — **Phase 1 verified** — `scan_operator_violations()` → 0; full suite **104 tests PASS** (4 skipped); sync pipeline yaml → `DICTIONARY_BADGE_DEFAULT` + `data_dictionary_meta.json`; disk-backed badge evidence PASS. Commits `80472ed` · `194506a`.
- **June 29, 2026** — **Phase 2 prep shipped (planning only)** — `Phase2_Node_Cockpit_Data_Model.md` defines per-node JSON shape (signal, directional, RV, implementation, sizing, basis quartiles). **Awaiting Clark review** before implementation. Commit `877524a`.
- **June 29, 2026** — **Phase 1 complete** — Master Data Dictionary v1.0 locked; naming aligned across YAML, Comet shortcuts, normalize script, TC badge. Phased plan v1.0 shipped. Phase 2 cockpit **UI/code not started**.
- **June 29, 2026** — **BUILD Cousins role adoption complete** — session activation shipped; canon test PASS; commit `25ed812`.
- **June 28, 2026** — **Desk CSV drop issue logged** — filename quarantine mitigated via `normalize_whinfell_drop.sh`; header/transform gap open (2.2e). TempLibby report block added above. Perplexity working on response.
- **June 28, 2026** — **Desktop launcher fixed** — `deploy_desktop_launchers.sh` · use `Whinfell Daily AM.app` on Desktop.
- **June 27, 2026** — **Daily Launcher shipped** — `Whinfell_Daily_Launcher.py` runs `whinfell_daily_am.sh` with live log + status bar; fixed `--window` typo in AM script.
- **June 27, 2026** — **Phase 2.2 Final shipped** — Browser blueprint, hydration import UX, `morning_daily.sh`, `verify_2_2_final` PASS.
- **June 27, 2026** — **Comet CSV runbook shipped** — `run_csv_download.py` daily chain live; Operator Guide + Quick Ref v1.4 distributed.
- **June 27, 2026** — Full pipeline verified: export → stage → ingest → hydrate → Transmission Control import.
- **June 26, 2026** — **Production sign-off** — desk rollout approved. No blockers.
- **June 26, 2026** — Acceptable gaps: WTC-2.0 full round-trip, scenario loop scope.
- **June 26, 2026** — Phase 2.1 refinements follow structured desk feedback.