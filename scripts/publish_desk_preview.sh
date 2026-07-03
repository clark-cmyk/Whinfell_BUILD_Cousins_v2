#!/usr/bin/env bash
# Commit + push source files so GitHub Actions redeploys desk preview (free Pages).
# Run after whinfell_daily_am.sh when you want Wes/Lovable on the latest bundle.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "publish_desk_preview: not a git repo — init + remote first:" >&2
  echo "  git init && git remote add origin <your-github-repo-url>" >&2
  exit 1
fi

REMOTE="$(git remote get-url origin 2>/dev/null || true)"
if [[ -z "$REMOTE" ]]; then
  echo "publish_desk_preview: no git remote 'origin' — add GitHub repo URL first." >&2
  exit 1
fi

# Derive owner/repo slug dynamically (supports _v2 etc); fallback for gh Pages calls
REPO_SLUG=$(echo "$REMOTE" | sed -E 's#^.*github.com[/:]([^/]+/[^/.]+)(\.git)?$#\1#')
if [[ -z "$REPO_SLUG" ]]; then
  REPO_SLUG="clark-cmyk/Whinfell_BUILD_Cousins_v2"
fi
PAGES_URL="https://${REPO_SLUG%%/*}.github.io/${REPO_SLUG##*/}/"

bash scripts/build_desk_preview.sh

# Pages serves main/docs/ (static preview). Rebuild copies _desk_preview_out → docs/
rm -rf docs
cp -R _desk_preview_out docs
touch docs/.nojekyll

# Note: build now produces a self-contained index.html (all critical JS+CSS inlined)
# This fixes asset 404s and script execution problems on GitHub Pages project subpaths.

# Optional: Actions also deploy gh-pages (backup). Primary share URL uses main/docs/.
if command -v gh >/dev/null 2>&1; then
  if ! gh api "repos/${REPO_SLUG}/pages" --silent 2>/dev/null; then
    echo "publish_desk_preview: enabling GitHub Pages (gh-pages branch)…" >&2
    if gh api -X POST "repos/${REPO_SLUG}/pages" \
      --input - <<'EOF' 2>/dev/null; then
{"build_type":"legacy","source":{"branch":"gh-pages","path":"/"}}
EOF
      echo "publish_desk_preview: Pages enabled → ${PAGES_URL}" >&2
    else
      echo "publish_desk_preview: WARN — could not auto-enable Pages." >&2
      echo "  Manual: repo → Settings → Pages → Deploy from branch gh-pages / root" >&2
      echo "  Then: gh workflow run desk-preview-pages.yml --ref main" >&2
    fi
  fi
else
  echo "publish_desk_preview: install gh CLI to auto-enable Pages on first publish." >&2
fi

# Actions rebuilds from 08_Deliverables/ — must commit sources, not only docs/
git add docs/ \
  08_Deliverables/Whinfell_Transmission_Control.html \
  08_Deliverables/Whinfell_BasisWatch.html \
  08_Deliverables/basis_watch.css \
  08_Deliverables/basis_watch_analytics.js \
  08_Deliverables/basis_watch_panel.js \
  08_Deliverables/desk_china_ladder_models.js \
  08_Deliverables/data_dictionary_meta.json \
  scripts/build_desk_preview.sh \
  scripts/publish_desk_preview.sh \
  .github/workflows/desk-preview-pages.yml \
  2>/dev/null || true

if git diff --cached --quiet; then
  echo "publish_desk_preview: nothing to commit — desk preview already up to date on this branch."
  if command -v gh >/dev/null 2>&1; then
    echo "  Redeploying latest main to Pages…"
    gh workflow run desk-preview-pages.yml --ref main 2>/dev/null || true
    echo "  Watch: gh run watch \$(gh run list --workflow=desk-preview-pages.yml --limit 1 --json databaseId -q '.[0].databaseId')"
  else
    echo "  Trigger manual deploy: GitHub → Actions → Desk preview → Run workflow"
  fi
  exit 0
fi

git commit -m "desk preview: TC + hydration bundle $(date -u +%Y-%m-%dT%H:%MZ)"
git push origin HEAD

echo ""
echo "publish_desk_preview: pushed — GitHub Actions will deploy Pages in ~1–2 min."
echo "  Check: GitHub repo → Actions → Desk preview (GitHub Pages)"
echo "  URL:   GitHub repo → Settings → Pages (private — collaborators + GitHub login)"
echo "  Setup: 08_Deliverables/Desk_Preview_Private_Access_Setup.md (Pro + invite Wes)"