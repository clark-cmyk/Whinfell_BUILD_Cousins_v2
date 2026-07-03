# Whinfell_BUILD_Cousins Best Practices

**Last Updated**: 2026-07-03  
**Purpose**: Prevent dirty repo states, CI failures, and deployment issues.

This document combines low-level repo hygiene with higher-level practices for the desk preview (GitHub Pages) and CI workflows.

## 1. Repo Hygiene

- **Never** `git add -A`. This is the #1 way to accidentally commit gigabytes of CSVs, parquet files, or quarantine data.
- Maintain a strong `.gitignore`. At minimum it should cover:
  - `staged_raw/`
  - `Archive/`
  - `quarantine/`
  - `repo_cleanup*/`
  - `*.DS_Store`
  - `__pycache__/`
  - `_desk_preview_out/`
- Periodically run `git clean -fdx -n` (dry-run first!) to see what would be removed.
- Large artifacts and raw ingestion data must stay out of the history.

## 2. Git Workflow

- **Always** run `git status -sb` before any commit or publish.
- Use `git pull --rebase origin main` frequently to keep history clean.
- Use **targeted** adds only. Example safe pattern:

  ```bash
  git status -sb

  # Safe targeted add for desk work
  git add 08_Deliverables/ docs/ scripts/ .github/ README.md BEST_PRACTICES.md
  git add -u -- . ':!staged_raw' ':!staged_raw/**' ':!Archive' ':!quarantine'
  ```

- When publishing desk previews, prefer `scripts/publish_desk_preview.sh` (it performs a controlled add internally).

## 3. Desk Preview Publishing

- **Preferred workflow**: Use `scripts/publish_desk_preview.sh` after updating source assets in `08_Deliverables/` (TC HTML, BasisWatch, JS/CSS/JSON) and/or data in `data/`.
  - It runs the build, syncs to `docs/`, stages the right files, commits, pushes, and triggers the Pages deploy.
  - The script dynamically derives the repo slug from `git remote` (no hard-coded owner/repo names).

- **What gets deployed**:
  - Primary: `main/docs/` (served as GitHub Pages root with `.nojekyll`).
  - The `desk-preview-pages.yml` workflow also publishes the `_desk_preview_out/` artifact via GitHub Pages.

- **Triggering the deploy**:
  - Pushes to `main` that touch relevant paths automatically run `.github/workflows/desk-preview-pages.yml`.
  - Manual trigger: `gh workflow run desk-preview-pages.yml --ref main` or via the GitHub UI.

- **Private access**: See `08_Deliverables/Desk_Preview_Private_Access_Setup.md`.

## 4. CI Verification (`whinfell_verify.yml`)

- The "Whinfell Verify" workflow only runs on changes to pipeline code (via `paths` filters):
  - `whinfell_pipeline/**`
  - `china_policy_track/**`
  - `scripts/ci_verify.sh`
  - `.github/workflows/whinfell_verify.yml`

  This prevents noisy CI failures on routine desk asset updates and data refreshes.

- **Never** hard-code macOS temp paths. Use a portable pattern:

  ```python
  import os
  import tempfile
  from pathlib import Path

  SCRATCH = Path(
      os.environ.get(
          "GROK_GOAL_SCRATCH",
          str(Path(tempfile.gettempdir()) / "grok-goal-verify" / "implementer"),
      )
  )
  SCRATCH.mkdir(parents=True, exist_ok=True)
  ```

  `scripts/ci_verify.sh` seeds `GROK_GOAL_SCRATCH` using `mktemp`.

- `verify_phase2_goal.py` is intentionally strict. The workflow uses `continue-on-error: true` so a single publish doesn't turn the whole repo red while still surfacing full logs.

## 5. GitHub Actions Hygiene (Node + Deprecations)

- Always use recent major versions that target current Node runtimes:
  - `actions/checkout@v7`
  - `actions/setup-python@v6`
  - `actions/setup-node@v6`
  - `actions/upload-pages-artifact@v5`
  - `actions/deploy-pages@v4`

- Older pins (`@v4` / `@v3`) produce repeated "Node 20 is being deprecated" warnings.

## 6. General Rules

- Keep workflow `on:` triggers narrow (`paths` / `paths-ignore`) so that documentation, data refreshes, and desk HTML changes don't run heavy Python/Node verification jobs.
- Keep `publish_desk_preview.sh` and `build_desk_preview.sh` in sync with the file list in `desk-preview-pages.yml`.
- Intentionally committed data (`data/hydration/`, `data/barchart/`, etc.) exists so the static preview and CI can run without external dependencies.
- Run `bash scripts/ci_verify.sh` (or the full goal verifier) locally before pushing changes to the pipeline.
- Changes to `.github/workflows/` should ideally go through a PR.

## 7. Common Pitfalls

- `git add -A` or broad adds → massive accidental commits of `staged_raw/`.
- Hard-coded repo names in publish scripts → broken `gh api` calls.
- Missing `data/hydration/latest.json` → build falls back to a stub (some tests expect richer content).
- Running full `verify_phase2_goal.py` on every push → flaky failures due to timestamps, flow status values, and HTML string assertions.
- Using outdated Actions → persistent Node deprecation noise in logs.

---

Update this file whenever new patterns or gotchas are discovered.