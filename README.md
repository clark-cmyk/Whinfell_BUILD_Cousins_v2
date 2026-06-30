# Whinfell BUILD Cousins

Parallel execution team supporting the Whinfell Transmission Map build.

## Folder Structure
- 01_Strategy_Docs/       ← Operating plans & approvals
- 02_Prompt_Library/      ← All saved prompts
- 03_Dashboard_Build/     ← Dashboard specs & iterations
- 04_Score_Calculation/   ← Credit Confirmation Score logic
- 05_Fallback_Tools/      ← Excel / Google Sheet backups
- 06_Testing_Logs/        ← Prompt testing results
- 07_Reference_Materials/ ← Ticker lists, definitions
- 08_Deliverables/        ← Final approved outputs
- china_policy_track/     ← China Policy data models, Parquet schema, ingestion
- data/china_policy/      ← China Policy Parquet storage (isolated from data/global/)
- staged_raw/             ← Operator CSV staging (Comet runbook → Parquet)
- run_csv_download.py     ← Daily CSV chain: stage → collect → hydrate
- scripts/morning_daily.sh  ← Morning one-liner (Comet blueprint)
- 08_Deliverables/Comet_Browser_Operations_Blueprint.md ← Backup views + shortcuts
- whinfell_pipeline/      ← Ingest, hydrate, WTM EXPORT v2.1 spec

## Naming authority

**Master Data Dictionary v1.0 (Locked, June 29, 2026)** — [`01_Strategy_Docs/Master_Data_Dictionary_v1.0.md`](01_Strategy_Docs/Master_Data_Dictionary_v1.0.md) · machine registry: `whinfell_pipeline/data_dictionary.yaml`

Phased roadmap: [`08_Deliverables/Whinfell_Phased_Development_Plan_v1.0.md`](08_Deliverables/Whinfell_Phased_Development_Plan_v1.0.md)

This team works autonomously once the Operating Plan is approved.
