#!/usr/bin/env bash
# Open GitHub collaborator settings for Whinfell desk reviewers.
# Email invites must be completed in the browser (GitHub API requires usernames).
set -euo pipefail

REPO_URL="https://github.com/clark-cmyk/Whinfell_BUILD_Cousins/settings/access"

echo "Opening GitHub collaborator settings..."
open "$REPO_URL" 2>/dev/null || xdg-open "$REPO_URL" 2>/dev/null || echo "Open manually: $REPO_URL"

cat <<'EOF'

INVITE THESE EMAILS (Read access):
  • wes@whinfellcap.com
  • william@whinfellcap.com

Steps:
  1. Add people
  2. Paste each email → Add to repository
  3. Confirm role: Read

After they accept, share the private Pages URL from Settings → Pages.

EOF

if command -v gh >/dev/null 2>&1; then
  echo "Pending invitations:"
  gh api repos/clark-cmyk/Whinfell_BUILD_Cousins/invitations \
    --jq '.[] | "  - \(if .invitee.login then .invitee.login else "pending" end) (\(.permissions))"' 2>/dev/null \
    || echo "  (none yet — complete invites in browser)"
fi