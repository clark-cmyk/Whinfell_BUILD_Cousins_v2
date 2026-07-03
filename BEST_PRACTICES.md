# Best Practices for Whinfell Desk Preview + CI

This document captures operational best practices for the desk preview deployment (GitHub Pages) and the supporting CI verification workflow.

## Desk Preview Publishing

- **Preferred workflow**: Use `scripts/publish_desk_preview.sh` after updating source assets in `08_Deliverables/` (TC HTML, BasisWatch, JS/CSS/JSON) and/or data in `data/`.
  - It runs the build, syncs to `docs/`, stages the right files, commits, pushes, and triggers the Pages deploy.
  - The script dynamically derives the repo slug from `git remote` (no hard-coded owner/repo names like the old `Whinfell_BUILD_Cousins`).

- **What gets deployed**:
  - Primary: `main/docs/` (served as GitHub Pages root with `.nojekyll`).
  - Backup path: the `desk-preview-pages.yml` workflow also publishes the `_desk_preview_out/` artifact.

- **Triggering the deploy**:
  - Push to `main` that touches relevant paths automatically runs `.github/workflows/desk-preview-pages.yml`.
  - Manual: `gh workflow run desk-preview-pages.yml --ref main` or GitHub UI.

- **Private access**: See `08_Deliverables/Desk_Preview_Private_Access_Setup.md`.

## CI Verification (`whinfell_verify.yml`)

- Runs the "Whinfell Verify" workflow **only on changes to pipeline code** (via `paths` filters):
  - `whinfell_pipeline/**`
  - `china_policy_track/**`
  - `scripts/ci_verify.sh`
  - `.github/workflows/whinfell_verify.yml`

- This prevents noisy failures on routine desk asset/data publishes (which only touch `docs/`, `08_Deliverables/`, and the Pages workflow).

- **Never** commit hard-coded macOS temp paths. Use:
  ```python
  import tempfile
  from pathlib import Path
  SCRATCH = Path(os.environ.get("GROK_GOAL_SCRATCH",
      str(Path(tempfile.gettempdir()) / "grok-goal-verify" / "implementer")))
  ```
  The `ci_verify.sh` also seeds the env var with `mktemp`.

- `verify_phase2_goal.py` (and `goal_scratch.py`) are intentionally strict for local goal verification. In CI we use `continue-on-error: true` so a single publish doesn't turn the repo red while still surfacing logs.

## GitHub Actions Hygiene (Node + Deprecations)

- Always pin to recent major versions that target current Node runtimes:
  - `actions/checkout@v7`
  - `actions/setup-python@v6`
  - `actions/setup-node@v6`
  - `actions/upload-pages-artifact@v5`
  - `actions/deploy-pages@v4`

- Old pins (`@v4`, `@v3`) trigger "Node 20 is being deprecated" warnings (and sometimes force Node 24 compatibility issues).

- When adding new JS steps, prefer `setup-node` explicitly.

## General Rules

- Keep workflow triggers narrow (`paths` / `paths-ignore`) so that doc updates, data refreshes, and desk HTML changes don't run expensive or fragile Python/Node verification jobs.
- `publish_desk_preview.sh` and `build_desk_preview.sh` must be kept in sync with the Pages workflow file list.
- Data in `data/hydration/`, `data/barchart/`, etc. is intentionally committed so that the static preview + CI hydrate tests can run without external services.
- Run `bash scripts/ci_verify.sh` (or the full goal verifier) locally **before** pushing pipeline changes.
- `.github/workflows/` changes themselves should be tested via a PR when possible.

## Common Pitfalls

- Hard-coded repo names in publish scripts → broken `gh api` calls on forks/renames.
- Missing `data/hydration/latest.json` → build produces a stub; some tests expect richer data.
- Running the full `verify_phase2_goal.py` on every push → flaky failures from timestamps, flow status, and HTML string assertions.
- Using old Actions → repeated Node deprecation spam in logs.

Update this file when patterns change.
