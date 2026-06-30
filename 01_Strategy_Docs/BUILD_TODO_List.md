# BUILD Cousins - TODO List

**Maintained by:** BUILD Cousins  
**Last Updated:** June 30, 2026 (Goals 1–6 **done** · **UI audit shipped** · **desk preview Pages scaffold** · next **7–11**)
**Purpose:** Track all active and planned work for the Whinfell Transmission Map support track.

---

## Next Up (recommended order)

| # | Goal | Priority | Owner | Effort | Done when |
|---|------|----------|-------|--------|-----------|
| **7** | **Fresh flows export** — `WTM-Flows-Global.csv` from wired URL → normalize → re-chain | **High** | Clark | 10 min | `flows_sidecar.as_of` = today · not Jun 29 stale |
| **8** | **Live TC Focus confirm** — Clark visual pass on `latest.json` · update ratings if needed | **High** | Clark | 15 min | Proxy ratings in `Desk_Feedback_Log.md` confirmed or revised |
| **9** | **ARCH-4 desk run** — 16-symbol Barchart core historical batch (`WTM-Barchart-Core`) | Medium | Clark | 1 session | Core symbols staged · `barchart_core_history` in provenance |
| **10** | **Phase 2.1** — WTC-2.0 import round-trip · scenario loop scope | Medium | Bridge + Edge | 1–2 sessions | Export → edit tracer → re-import without bundle downgrade |
| **11** | **Collect noise fix** — Barchart options/greeks/daily raw passthrough adapter (stops `collect_exit=1`) | Medium | Integration Dynamo | 1 session | Daily chain `chain_ok: true` with optional Barchart files in drop |

**BUILD Cousins:** P1 unlocked — start **#10–#11** in parallel while Clark runs **#7–#9**.

### Completed (Goals 1–6 — June 30)

| # | Goal | Result |
|---|------|--------|
| 1 | ARCH-3 trim + export | `credit_20260630_1002.csv` · `koyfin_snapshot_csv` |
| 2 | Morning collect | `whinfell_drop` · `missing=0` |
| 3 | Daily chain | `sha256:68ff07b54…` · `fresh` · flows `ok` |
| 4 | Desk sign-off | walkthrough 6/6 · operator confirm 8/8 (proxy) |
| 5 | TempLibby close | ARCH-3 accepted · sign-off block filled |
| 6 | Koyfin watchlist trim (UI) | `credit_20260630_1149.csv` · 16/16 from `WTM-Import-Core` watchlist · section labels OK |

### Wired desk URLs (June 30 — Clark confirmed downloader)

| View | URL | Env override (optional) |
|------|-----|-------------------------|
| **WTM-Import-Core** (Koyfin) | `https://app.koyfin.com/myw/70789aa7-8084-4e4c-85d3-09f9b78dcd3a` | `KOYFIN_VIEW_IMPORT_CORE_URL` |
| **WTM-Flows-Global** (Koyfin) | `https://app.koyfin.com/myw/afb1f314-4de4-47b6-b02f-0de2601b62b9` | `KOYFIN_VIEW_FLOWS_GLOBAL_URL` |
| **WTM-GOV-USPRC** (Koyfin) | `https://app.koyfin.com/myw/e94a97b3-600d-47d4-91d3-a01f8749146d` | `KOYFIN_VIEW_FLOWS_GOV_URL` |
| **WTM-Futures-Intraday** (Barchart) | `https://www.barchart.com/my/watchlist?viewName=197689` | `BARCHART_SCREEN_INTRADAY_URL` |

`desk_urls.yaml` + `collection_manifest.yaml` updated · `replace_me: false` · `run_batch_collect.py open` opens tabs only — **Clark clicks Download CSV**.

---

## Current Status

| # | Deliverable | Priority | Status | Owner | Notes |
|---|-------------|----------|--------|-------|-------|
| **ARCH** | WTM Data Architecture (Koyfin + Barchart) | **High** | **Plan shipped** | Integration Dynamo | `01_Strategy_Docs/WTM_Data_Architecture_Build_Plan.md` · `whinfell_pipeline/data_dictionary.yaml` |
| **ARCH-1** | `source_router.py` unified ingest routing | High | **Shipped (M1–M3)** | Integration Dynamo | M1 router · M2 components · M3 `ingest_provenance` |
| **ARCH-3** | Clark: WTM-Import-Core Koyfin watchlist | High | **Accepted · UI trimmed** | Clark | `credit_20260630_1149.csv` · 16/16 · `koyfin_snapshot_csv` |
| **Desk ops** | Wired Koyfin + Barchart watchlist URLs | High | **Shipped** | Clark + Bridge | `desk_urls.yaml` · manifest fallbacks · Clark = downloader |
| **ARCH-4** | Barchart core batch export in manifest | Medium | **Shipped · Clark desk run open** | Clark | `barchart_core_batch` · `WTM-Barchart-Core` in desk_urls |
| **Desk feedback** | Transmission Control rollout | High | **Proxy signed · live confirm open** | Clark + Bridge | Ratings 4/5 logged · TODO **#8** live Focus pass |
| **Phase 2.1** | Refinements post-feedback | Medium | **Next BUILD P1** | Bridge + Edge | WTC-2.0 import · scenario loop · TODO **#10** |
| **Phase 2.2 UI** | TC cockpit hierarchy refactor (header/KPI/drawer) | High | **Shipped** | Bridge + Clarity | Badge `2.2-UI-AUDIT-2026-06-30` · three-zone top bar · signal drawer · zone labels |
| **Phase 2.2 UI** | UI audit human + agent optimization | High | **Shipped** | Bridge + Clarity | `whinfell_ui_audit_chunked.md` · DD audit panel · flipchart state · failure taxonomy |
| **Phase 2.2 Final** | Desk validation of browser blueprint | Medium | **Collecting** | Bridge | Blueprint + hydration UX + UI refactor shipped |
| **2.2e** | Raw vendor CSV → WTM observation row transform | **High** | **Shipped** | Integration Dynamo | `whinfell_pipeline/raw_csv_transform.py` — auto on stage |
| **Desk ops** | Operator Guide v1.5 (mission surfaces + ARCH-1 + Barchart normalize) | Medium | **Shipped** | Clarity | `Whinfell_Expanded_Operators_Guide_v1.5.md` |
| **Desk ops** | Barchart native-export normalize rules | High | **Shipped** | Bridge | daily/options/greeks/spreads → canonical · ~60% quarantine coverage |
| **Desk ops** | Desk validation log (mission surfaces + UI) | High | **Automated + operator confirm** | Bridge | `desk_walkthrough.py` · 6/6 · `desk_operator_confirm` 8/8 |
| **Desk ops** | `whinfell_daily_am.sh` default `--window today` → `48h` | **High** | **Shipped** | Bridge | Normalize + 48h + `--overwrite` wired in AM script |
| **Desk ops** | Clark AM hydration chain (48h) — report to TempLibby | High | **Validated** | Clark | 91 staged routes · 5 nodes · `fresh` · flows `ok` (stale Jun 29) |
| **Desk ops** | `normalize_whinfell_drop.sh` bash portability fix | Medium | **Shipped** | Bridge | Was zsh-only (`${0:A:h:h}`); now runs under `bash` per Perplexity playbook |
| **Phase 1** | Master Data Dictionary v1.0 + naming rectification | **High** | **Complete · Verified** | Bridge + Precision | 104 tests PASS · 0 naming violations · `194506a` |
| **Phase 2 prep** | Node cockpit data model spec | High | **Complete · Locked v0.2** | Blueprint | `c9974fa` · ambiguities A/B/E/F locked |
| **Phase 2a** | `rv_series` + interim node score weights | High | **Complete** | Bridge | Master DD registry · `3293a9b` |
| **Phase 2b-data** | WTM EXPORT v2.2 + `node_cockpits` hydration builder | High | **Shipped** | Bridge | `cdd677a` · bundle v1.1.0 · 111 tests PASS |
| **Phase 2b** | ARCH-1 component routing + Koyfin history for RV quartiles | High | **M2 shipped** | Integration Dynamo | Live components + Koyfin RV series · credit still horizon fallback |
| **Phase 2.2-mission** | Basis node mission-surface (operator console) | High | **Shipped · Accepted** | Bridge + Clarity | Badge `2.2-MISSION-2026-06-29` · commits `54cc2b9`→`2d2c847` · no further Basis polish |
| **Phase 2.2-mission** | Credit node mission-surface (extend Basis pattern) | High | **Shipped · Desk testing** | Bridge + Clarity | Handoff: `08_Deliverables/Credit_Mission_Surface_Desk_Handoff.md` |
| **Phase 2.2-mission** | Liquidity node mission-surface (extend Credit pattern) | High | **Shipped · Desk testing** | Bridge + Clarity | Plan: `01_Strategy_Docs/Liquidity_Mission_Surface_v1_Plan.md` · Handoff: `08_Deliverables/Liquidity_Mission_Surface_Desk_Handoff.md` |
| **Phase 2.2-mission** | RV/Basis spot-fallback table (Credit `horizon_net_fallback`) | Medium-High | **Shipped** | Bridge | Presentation-only — value once on active horizon; pct/Q/rich per lookback |
| **ARCH-1 M2** | Live component inputs from `source_router` + RV history | High | **Shipped** | Integration Dynamo | `component_router.py` · `source: rv_history` on components |
| **Desk ops** | Quarantine retry + normalize transform layer | Medium | **Shipped** | Bridge | `quarantine_retry.py` · `retry_quarantine_normalize` · Return series · Barchart passthrough |
| **Desk ops** | TC ingest audit drawer | Medium | **Shipped** | Clarity | Signal drawer · `ingest_provenance` table |
| **Desk ops** | Flows PR-5 WTM EXPORT flow lines | Medium | **Shipped** | Bridge | `export_contract.py` · funds-flow lines in v2.2 |
| **Desk ops** | Quick Reference Card v1.5 | Low | **Shipped** | Clarity | `.md` + `.docx` at desk |
| **Phase 2b-ui** | Flows PR-4 sponsorship card polish | Medium | **Shipped** | Bridge + Clarity | Basket label · confidence delta · compare fade |
| **Phase 2** | Node architecture redesign (5 trading cockpits) | High | **Desk gate passed (proxy)** | Bridge + Edge + Clarity | 5/5 mission · UI `2.2-UI` · live confirm TODO **#8** |
| **Phase 2 open** | Ambiguity C — trading-day vs calendar-day lookback | Medium | **Open** | TempLibby + desk | Default locked in spec; desk confirm |
| **Phase 2b** | Funds Flow Sponsorship layer (`FundsFlowSponsorshipCard`) | High | **PR-1 shipped** | Bridge + Clarity | Registry locked · **PR-3a/b → PR-2 → PR-4/5** |
| **Phase 2b-data** | PR-1 registry + PR-3a/b ingest + PR-2 `funds_flows.py` | High | **PR-3a shipped** | Bridge + Dynamo | Wide `flows_*.csv` stages via `flows_parser` · sidecar `ok` |
| **Phase 2b-ops** | `flows_*.csv` staging bypass (wide format → `flows_parser`) | **High** | **Shipped** | Bridge | `stage_file` skips raw→WTM transform for `dataset=flows` |
| **Phase 2b-ops** | `WTM-*.csv` normalize rules (desk exports) | High | **Shipped** | Bridge | Global-Rates, Equities-Breath, Credit-Confirmation, China-Policy, MAS-KOY |
| **Phase 2.2-mission** | Breadth node mission-surface | High | **Shipped · Desk testing** | Bridge + Clarity | `MISSION_SURFACE_NODES` + `__breadthMissionProbe` |
| **Phase 2.2-mission** | Highbeta node mission-surface | High | **Shipped · Desk testing** | Bridge + Clarity | `MISSION_SURFACE_NODES` + `__highbetaMissionProbe` · IBIT vs QQQ beta spread |
| **Phase 2b-ops** | `WTM-Flows` normalize + Koyfin view expansion | High | **Normalize shipped** | Clark | Expand view tickers per spec §5 · `WTM-Flows*.csv` → `flows_*` via Master DD |
| **Phase 2b-ops** | `normalize_whinfell_drop.sh` — map `WTM-Flows*.csv` | Medium | **Shipped (via DD rule)** | Bridge | `batch_collect.py normalize` reads `WTM-Flows*.csv` rule |
| **Phase 3** | TC interface (full-screen Why, flip nav, margin module) | Medium | **Planned** | Clarity + Safeguard | Blocked on Phase 2 UI · flow card ships in 2b-ui |
| **Phase 4** | Validation & reliability gate | Medium | **Planned** | Hammer + Precision | After Phase 3 |

---

## Desk preview — free GitHub Pages (Wes + Lovable, $0)

**Shipped:** `scripts/build_desk_preview.sh` · `scripts/publish_desk_preview.sh` · `.github/workflows/desk-preview-pages.yml` · TC auto-hydrate from co-hosted `latest.json` on HTTPS.

**Clark one-time setup (~10 min, free):**
1. Create **private** GitHub repo → `git remote add origin …` → push `main`
2. Repo **Settings → Pages → Source: GitHub Actions**
3. **Settings → Collaborators** → add **Wes** (and Lovable reviewer if needed)
4. After first Actions run: copy Pages URL from **Settings → Pages**

**Clark ongoing:** after AM chain → `bash scripts/publish_desk_preview.sh` (commit + push → auto-deploy).

**Wes:** bookmark Pages URL · log into GitHub once if private · hard-refresh — no repo clone, no local files.

**Lovable:** same URL + `08_Deliverables/whinfell_ui_audit_chunked.md` · badge `2.2-UI-AUDIT-2026-06-30`.

---

## Report for TempLibby (June 30, 2026 — UI audit `/goal` shipped)

**Source:** `~/Downloads/whinfell_drop/whinfell_ui_audit_chunked.md` (Chunks 1–12).

**Shipped in TC** (`Whinfell_Transmission_Control.html` · badge `2.2-UI-AUDIT-2026-06-30`):

| Priority | Audit item | Fix |
|----------|------------|-----|
| P1 | Light-mode semantic contrast | Tinted `status-chip` classes on Fresh/Amber/Impaired/Complete · coverage pills · diag chips |
| P2 | Partial-data transparency | Coverage checklist adds **Signals** row · node status = flows + signal readiness · `complete` requires both |
| P3 | Shift-click + flipchart trust | Visible flipchart state (`2 / 5`) · prev/next buttons · `?` tooltip · flip toast |
| P4 | Data dictionary audit | Signal drawer panel · clickable coverage pills · failure codes (`DD-MISS`, `DD-DERIV`, etc.) · remediation detail |
| Agent | Grok/agent ingest | `ui_audit` block in `buildGrokPayload` · `window.__uiAuditProbe` · headless test PASS |

**Tests:** `node whinfell_pipeline/tests/html_headless_cockpit.mjs` — 15 probes incl. `uiAudit` (dictionary_audit_count: 9 · flip `4/5`).

**Clark verify:** Hard-refresh TC → toggle Light mode → Import `latest.json` → open Signal detail → Data dictionary audit → click coverage pill.

---

## Report for TempLibby (June 30, 2026 — Clark chain 17:09 UTC)

**What Clark ran:** Drop cleanup · `normalize_whinfell_drop.sh` · `whinfell_daily_am.sh` (48h) · attempted flows export.

**Bundle (production):** `sha256:62066f68677ac24da870473d3a00de8762b402fe40d36b524b8069dbb47f633c` · `as_of: 2026-06-30T17:09:57+00:00` · `freshness_status: fresh` · **5 node cockpits** · `desk_operator_confirm` **8/8 PASS**.

**ARCH-3:** Goal **#6 done** — `credit_20260630_1149.csv` from trimmed `WTM-Import-Core` watchlist (16/16 tickers · section labels present · route `koyfin_snapshot_csv`). Replaces desk-trimmed `credit_20260630_1002.csv`.

**Barchart intraday:** `futures_intraday_20260630_1206.csv` staged (90 symbols · watchlist `197689`).

**Flows gap (blocking freshness narrative):** `flows_sidecar.as_of` still **2026-06-29** — only `flows_20260629_1017.csv` in drop; Clark saved `.mhtml` instead of CSV on flows attempt. **Next Clark:** export `WTM-Flows-Global.csv` from wired URL → normalize → re-chain (TODO **#7**).

**Known noise:** `collect_exit=1` · `chain_ok: false` — Barchart options/greeks/daily/btc_basis adapter misses (51 ingest failures). Hydration still succeeds (`hydrate_exit=0`). BUILD TODO **#11**.

**Next Clark (#7–9):** Fresh flows CSV · live TC Focus confirm · optional ARCH-4 core batch · optional drop cleanup (zero-byte `__wtm_*` dupes).

**Next BUILD (#10–11):** Phase 2.1 WTC-2.0 round-trip · collect passthrough adapter.

**Clark → TempLibby message:** *"WTM-Import-Core watchlist trimmed and live — 16-ticker export ingested. Flows still Jun 29 until fresh Global export."*

---

## Report for TempLibby (June 30, 2026 — next batch 7–11)

**Gate cleared:** Goals 1–6 done · ARCH-3 UI-trimmed export ingested · bundle `sha256:62066f686…` fresh.

**Next Clark (7–9):** Fresh `WTM-Flows-Global` CSV · live TC Focus confirm · optional ARCH-4 core batch.

**Next BUILD (10–11):** Phase 2.1 WTC-2.0 round-trip · Barchart options/greeks/daily adapter (fix `collect_exit=1`).

**Backlog (non-blocking):** Quarantine sweep · Comet shortcut URL refresh · `koyfin_china_policy_*` normalize rule · `WTM-GOV-USPRC` export.

---

## Report for TempLibby (June 30, 2026 — Goals 1–5 executed)

**ARCH-3:** WTM-Import-Core **ACCEPTED** — `credit_20260630_1002.csv` (16 tickers) · route `koyfin_snapshot_csv` · watchlist URL wired.

**Daily chain:** `whinfell_daily_am.sh` ran · new bundle `sha256:68ff07b54f5476fc54b99974c3418673e8920e27bc48fe225cfe5b4e933ca6cb` · `freshness_status: fresh` · `flows_status: ok`.

**Desk sign-off:** walkthrough 6/6 · operator confirm 8/8 · node ratings 4/5 (BUILD proxy on live bundle). Clark to confirm visually in TC Focus mode when convenient.

**Clark → TempLibby message:** *"WTM-Import-Core live — replaces WhinPump interim."*

**Follow-up:** Trim Koyfin watchlist UI to 16 tickers only (current export was desk-trimmed from mega-watchlist).

---

## Report for TempLibby (June 30, 2026 — desk URLs + Clark downloader)

**BUILD backlog:** Phase 2.2 · ARCH-1 M1–M3 · ARCH-3 criteria · ARCH-4 manifest · quarantine transform · PR-5 · audit drawer · Quick Ref v1.5 · **desk URL wiring** — **all shipped**.

**Desk URLs wired:** Koyfin `WTM-Import-Core` + Barchart intraday watchlist `viewName=197689`. **Clark downloads** in browser; pipeline ingests from `~/Downloads/whinfell_drop` only.

**ARCH-3 check:** Vendor filename + normalize → `credit_*` **PASS**. Last export had all 16 core tickers but **~373 rows** (mega-watchlist) — Clark to trim watchlist to 16 only before sign-off.

**Latest bundle (confirm by lineage_hash):**
`sha256:f62d6257b294028c1669297fcc0da6a8af1284a0885507b3f7c8d8b1d68c8aab` · `as_of: 2026-06-30T13:49:11+00:00` · **5 node cockpits** · `freshness_status: fresh` · `flows_status: ok`

**Automated desk:** headless 12/12 + walkthrough 6/6 + operator confirm 8/8 · **live ratings still blank**

**Gate:** Clark morning collect + trimmed ARCH-3 export + Focus walk-through. No BUILD P1 until sign-off.

**Recommended Clark sequence (one AM session):**
1. Open wired URLs (`run_batch_collect.py open` or bookmarks) → download Koyfin + Barchart CSVs
2. Trim `WTM-Import-Core` to 16 tickers if not done → re-export
3. `bash whinfell_daily_am.sh` (normalize + 48h chain)
4. TC Focus walk + audit drawer → log ratings in `Desk_Feedback_Log.md`
5. Report to TempLibby: *"WTM-Import-Core live — replaces WhinPump interim."*

---

## Report for TempLibby (June 30, 2026 — TODO goals 3–6)

**What happened:** BUILD `/goal` batch **shipped** — (3) **quarantine transform** (Koyfin Return series · Barchart raw passthrough · `retry_quarantine_normalize` 20/20 sample), (4) **ARCH-4** `barchart_core_batch` manifest, (5) **TC audit drawer** ingest_provenance in signal drawer, (6) **Quick Ref v1.5.docx**. Desk walk-through now targets `latest.json`.

**Tests:** 28 targeted PASS · headless includes `ingestAudit` probe.

**Clark next:** WTM-Import-Core watchlist · live Focus ratings · optional ARCH-4 core batch download.

---

## Report for TempLibby (June 30, 2026 — goals 1–6 batch)

**What happened:** Six-item `/goal` batch **shipped** — (1) **ARCH-3 criteria** for Clark (`ARCH-3_WTM_Import_Core_Criteria.md`), (2) **ARCH-1 M3** `ingest_provenance` + `output_kind` in hydration, (3) koyfin `(N)` duplicate normalize, (4) **Flows PR-5** export lines, (5) `desk_operator_confirm` 8/8 PASS, (6) **Quick Ref v1.5** markdown.

**Latest bundle:** `sha256:f62d6257…` · 5 staged routes in `ingest_provenance` · PR-5 flow lines in `wtm_export_v22` · **32 tests PASS**.

**Clark next:** Create `WTM-Import-Core` per criteria doc → live Focus walk-through ratings.

---

## Report for TempLibby (June 30, 2026 — goal batch close)

**What happened:** Four-item `/goal` batch **shipped** — (1) desk pre-validation logged (`Desk_Feedback_Log.md` · 12/12 headless PASS), (2) **ARCH-1 M1** `source_router.py` + Koyfin RV series extraction, (3) **Operator Guide v1.5**, (4) **Barchart normalize rules** (daily/options/greeks/spreads → canonical). Prior session items retained: 5/5 mission surfaces, UI refactor `2.2-UI-2026-06-30`, flows `ok`, 48h AM chain.

**Latest bundle (confirm by lineage_hash):**
`sha256:f62d6257b294028c1669297fcc0da6a8af1284a0885507b3f7c8d8b1d68c8aab` · `as_of: 2026-06-30T13:49:11+00:00` · **37 staged** · all **5 node cockpits** · `freshness_status: fresh`

**Test suite:** 18 cockpit + ARCH-1 tests PASS (`test_source_router` · `test_rv_history` · `test_barchart_normalize_rules` · headless cockpit).

**Still open:** Desk **live** walk-through (ratings blank). ARCH-1 **M2** component stubs. ~427 quarantine files fail transform/header after rename (~60% now renameable).

**Next build priority:** Desk sign-off → ARCH-1 M2 → quarantine transform layer → ARCH-3 watchlist.

---

## Report for TempLibby (June 30, 2026 — AM)

**What happened:** Phase 2.2 Basis node mission-surface work is **accepted and shippable**. Operator console now has hydration/coverage banner, gate decision sentence, improved funds-flow messaging, post-import workflow, and Basis-specific mission read (tactical banner, summary strip, implication rail). Remaining Basis cosmetic issues are acceptable — **no further Basis polish**.

**Direction:** Extend the same mission-surface pattern to **Credit** (tactical banner + summary strip in bps + implication rail + shared coverage/gate/workflow). **No pipeline or scoring changes** for v1 — Credit hydration already ships full `rv_basis`, flows, and gate fields. Effort: **medium** (~1–2 sessions). Liquidity and Breadth follow after Credit is accepted.

**Open questions (Credit v1):** signal-band vs RV-cheap tension copy; weakest-link badge placement; China ladder in tactical line vs gate-only; light registry generalization vs Credit fork.

**Ship commits (Basis mission-surface):** `54cc2b9` · `ad01ded` · `042b1ea` · `8d21c9e` · `2d2c847`

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
| Quick Reference Card v1.4 | **Superseded by v1.5 markdown** |
| Quick Reference Card v1.5 | **Shipped (.md + .docx)** |
| Quarantine transform layer | **Shipped Jun 30** — Return series · Barchart passthrough · normalize retry |
| TC ingest audit drawer | **Shipped Jun 30** — signal drawer · `ingest_provenance` table |
| ARCH-4 barchart_core_batch | **Shipped Jun 30** — manifest + desk_urls |
| ARCH-3 WTM-Import-Core criteria | **Shipped Jun 30** |
| ARCH-1 M3 ingest_provenance | **Shipped Jun 30** |
| Flows PR-5 export lines | **Shipped Jun 30** |
| Koyfin `(N)` duplicate normalize | **Shipped Jun 30** |
| Expanded Operator's Guide v1.4 | **Superseded by v1.5** |
| Expanded Operator's Guide v1.5 | **Master reference** |
| ARCH-1 `source_router.py` (M1) | **Shipped Jun 30** |
| Barchart native normalize rules | **Shipped Jun 30** — ~60% quarantine rename coverage |
| Desk pre-validation (mission + UI) | **12/12 + 6/6 + 8/8 PASS** — live ratings open |
| Comet Browser Operations Blueprint | **Shipped** |
| Daily CSV chain (`run_csv_download.py`) | **Live — `verify_2_2_final` PASS** |
| Whinfell Daily Launcher (`Whinfell_Daily_Launcher.py`) | **Shipped — one-click desk tool** |
| Pre-stage rename (`scripts/normalize_whinfell_drop.sh`) | **Shipped — bash + zsh · filename contract** |
| Raw vendor CSV header transform (2.2e) | **Shipped — flows wide CSV still excluded** |
| AM hydration chain (`--window 48h`) | **Validated Jun 30** — 37 staged · 5 nodes · flows `ok` |
| Phase 2.2 UI refactor | **Shipped Jun 30** — badge `2.2-UI-2026-06-30` |
| Mission surfaces (5/5 nodes) | **Shipped Jun 30** — Basis · Credit · Liquidity · Breadth · Highbeta |
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
| **Phase 2 prep** | Locked decisions v0.2 (composite, quartile, options defer, China soft) | June 29, 2026 | `c9974fa` |
| **Phase 2a** | `rv_series` catalog + interim `node_score_weights` in Master DD | June 29, 2026 | 10 series · 5 nodes · `3293a9b` |
| **Phase 2b-data** | WTM EXPORT v2.2 spec + `node_cockpits.py` + hydration v1.1.0 | June 29, 2026 | `cdd677a` · 111 tests PASS |
| **Phase 2.2-mission** | Basis node mission-surface operator console | June 29, 2026 | `54cc2b9`→`2d2c847` · badge `2.2-MISSION-2026-06-29` |
| **Phase 2.2-mission** | Credit + Liquidity mission-surface + dark/light toggle | June 30, 2026 | `MISSION_SURFACE_NODES` generalized · headless tests PASS |
| **Phase 2.2-mission** | RV/Basis spot-fallback evidence table | June 30, 2026 | Presentation-only · `buildRvHorizonEvidenceMarkup()` |
| **Desk ops** | `normalize_whinfell_drop.sh` bash portability | June 30, 2026 | Perplexity playbook Step 1 now works with `bash` |
| **Desk ops** | AM hydration 48h chain validated | June 30, 2026 | lineage `315275f6…` · weakest=credit |
| **Phase 2b-ops** | Flows wide CSV staging bypass | June 30, 2026 | `flows_status: ok` · 15 tickers · lineage `f62d6257…` |
| **Phase 2b-ops** | WTM desk export normalize rules | June 30, 2026 | 9 renames on live drop |
| **Phase 2.2-mission** | Breadth mission-surface | June 30, 2026 | `__breadthMissionProbe` · headless PASS |
| **Phase 2.2-mission** | Highbeta mission-surface | June 30, 2026 | `__highbetaMissionProbe` · 5/5 nodes complete |
| **Phase 2.2 UI** | TC cockpit hierarchy refactor | June 30, 2026 | Badge `2.2-UI-2026-06-30` · drawer · zone labels |
| **Desk ops** | `whinfell_daily_am.sh` 48h + normalize | June 30, 2026 | Operator Guide v1.4 patch |
| **ARCH-1** | `source_router.py` M1 + meta sidecar routing | June 30, 2026 | `route_ingest()` · `test_source_router` PASS |
| **ARCH-1** | Koyfin RV history extraction (`load_koyfin_rv_series`) | June 30, 2026 | Live quartiles when wide rates staged |
| **Desk ops** | Barchart native normalize rules | June 30, 2026 | daily/options/greeks/spreads · 639/1066 renameable |
| **Desk ops** | Operator Guide v1.5 | June 30, 2026 | Mission surfaces · ARCH-1 · Barchart table |
| **Desk ops** | Desk feedback log pre-validation | June 30, 2026 | `Desk_Feedback_Log.md` · 12/12 headless |
| **ARCH-1** | M3 `ingest_provenance` + hydration `output_kind` | June 30, 2026 | `ingest_provenance.py` · TC audit drawer |
| **ARCH-3** | WTM-Import-Core acceptance criteria | June 30, 2026 | `ARCH-3_WTM_Import_Core_Criteria.md` |
| **ARCH-4** | `barchart_core_batch` manifest + desk_urls | June 30, 2026 | 16-symbol core · optional desk batch |
| **Desk ops** | Quarantine transform + normalize retry | June 30, 2026 | Return series · Barchart passthrough · 20/20 sample |
| **Phase 2b-ui** | Flows PR-5 export lines | June 30, 2026 | Funds Flow Verdict/5D/Summary in v2.2 |
| **Desk ops** | Quick Reference Card v1.5 | June 30, 2026 | `.md` + `.docx` |
| **Desk ops** | TC ingest audit drawer | June 30, 2026 | Signal drawer · `renderIngestProvenanceAudit` |
| **Desk ops** | `desk_operator_confirm` + walkthrough on `latest.json` | June 30, 2026 | 8/8 + 6/6 automated |

---

## Desk Open Commands

```bash
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Transmission_Control.html
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Quick_Reference_Card_v1.5.docx
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Quick_Reference_Card_v1.5.md
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/ARCH-3_WTM_Import_Core_Criteria.md
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Whinfell_Expanded_Operators_Guide_v1.5.md
open ~/Desktop/Whinfell_BUILD_Cousins/08_Deliverables/Desk_Feedback_Log.md
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

**CLI fallback (48h — matches launcher default):**

```bash
cd ~/Desktop/Whinfell_BUILD_Cousins
bash scripts/normalize_whinfell_drop.sh ~/Downloads/whinfell_drop
python3 run_csv_download.py daily \
  --downloads ~/Downloads/whinfell_drop \
  --staged-root ./staged_raw \
  --operator cwt \
  --window 48h \
  --overwrite
python3 run_batch_collect.py run --window 48h
# Then: Transmission Control → Import data/hydration/latest.json (confirm lineage_hash)
```

**Verify:**

```bash
python3 -m whinfell_pipeline.verify_2_2_final
```

**Ship commits:** P1.2 `c9d9b63` · Sprint `1a33bee` · Phase 2.2 Final (pending commit)

---

## Notes
- **June 30, 2026 (Clark chain 17:09)** — Goals 1–6 done · `credit_20260630_1149` ingested · lineage `62066f686…` · flows stale Jun 29 · `collect_exit=1` known. Next: fresh flows export + live Focus confirm.
- **June 30, 2026 (session close)** — BUILD backlog for Phase 2.2 **complete**. Clark gate: ARCH-3 watchlist + live desk ratings. Next BUILD work: Phase 2.1 after feedback.
- **June 30, 2026 (goals 1–6 + TODO 3–6)** — ARCH-3 criteria · M3 provenance · PR-5 · quarantine transform · ARCH-4 manifest · audit drawer · Quick Ref v1.5.docx.
- **June 30, 2026 (goals 1–5)** — Desk walk-through 6/6 · ARCH-1 M2 live components · quarantine_retry · ARCH-3 handoff · Flows PR-4 · koyfin date normalize rules.
- **June 30, 2026 (goal batch close)** — **ARCH-1 M1 + v1.5 + Barchart normalize + desk pre-validation** shipped. 18 tests PASS.
- **June 30, 2026 (PM close)** — **5/5 mission surfaces complete** — Highbeta shipped (`IBIT vs QQQ beta spread` · `__highbetaMissionProbe`). Phase 2.2 UI refactor shipped (badge `2.2-UI-2026-06-30`).
- **June 30, 2026 (PM)** — **Next-steps batch shipped** — flows staging fix · AM script 48h · WTM normalize (9 renames) · Breadth mission-surface · Operator Guide patch. Re-run: `flows_status: ok` · 37 staged · lineage `f62d6257…`.
- **June 30, 2026 (PM)** — **RV spot-fallback fix shipped** — Credit focus table no longer repeats identical bps across 1M/3M/6M/12M/3Y when spot reading is shared; pct/quartile/richness still per lookback.
- **June 30, 2026 (PM)** — **Liquidity mission-surface v1 shipped** — same pattern as Credit/Basis; dark/light theme toggle restored.
- **June 30, 2026 (AM)** — **Basis mission-surface accepted** — stop Basis polish; Credit/Liquidity mission-surfaces shipped same day.
- **June 29, 2026** — **Flows spec v1.1** — companion file authoritative; `flows_meta` machine-readable degrade flags; Appendix A JSON (healthy + fallback + unavailable + partial + export). Awaiting §8 checklist sign-off.
- **June 29, 2026** — **Flows implementation spec drafted** — [Phase2_Flows_Implementation_Spec.md](Phase2_Flows_Implementation_Spec.md): L0/L1/L2 data model, `degrade_mode` state machine, Credit/Breadth examples, PR-1→5 ownership, Master DD delta list. **Desk sign-off §7 before PR-1/PR-3.**
- **June 29, 2026** — **Option D (Hybrid) locked** — primary `flows_*.csv` + credit 1D fallback; arena debate resolved.
- **June 29, 2026** — **Funds Flow ingest /arena debate** — Options A–E documented; BUILD recommends **Option D hybrid** (primary `WTM-Flows` time-series + credit cross-section 1D fallback). Desk already has `WTM-Flows-Global.csv` (quarantined — wrong filename). Staged `credit_*.csv` has no flow columns post-2.2e. Team vote Q1–Q5 in `08_Deliverables/Funds_Flow_Ingest_Arena_Debate.md`.
- **June 29, 2026** — **Funds Flow Sponsorship plan locked** — Design v1.0 + `/goal` + `/plan` for node-level `% AUM` confirmation layer (`FundsFlowSponsorshipCard`); flows subordinate to score/gate; Phase **2b-data** (pipeline) then **2b-ui** (TC rail). See `01_Strategy_Docs/Phase2_Funds_Flow_Sponsorship_Design.md`.
- **June 29, 2026** — **Phase 2 data layer shipped** — `node_cockpits.py` builds all 5 cockpits; hydration bundle **v1.1.0** adds `node_cockpits`, `cockpit_context`, `wtm_export_v22`; WTM EXPORT v2.2 spec locked. Full suite **111 tests PASS** (4 skipped). Commit `cdd677a`.
- **June 29, 2026** — **Phase 2 prep locked** — Data model v0.2 + `rv_series` (10 series) + interim `node_score_weights` in Master DD; ambiguities A/B/E/F resolved. Commits `c9974fa` · `3293a9b`.
- **June 29, 2026** — **Phase 1 verified** — `scan_operator_violations()` → 0; full suite **104 tests PASS** (4 skipped); sync pipeline yaml → `DICTIONARY_BADGE_DEFAULT` + `data_dictionary_meta.json`; disk-backed badge evidence PASS. Commits `80472ed` · `194506a`.
- **June 29, 2026** — **Phase 1 complete** — Master Data Dictionary v1.0 locked; naming aligned across YAML, Comet shortcuts, normalize script, TC badge. Phased plan v1.0 shipped. Phase 2 **TC cockpit UI not started**.
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