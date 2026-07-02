# Desk Preview — Private GitHub Pages Access

**Status:** Repo is **private** · Pages **paused** until GitHub Pro is active  
**Owner:** Clark · **Reviewer:** Wes (invite after Pro upgrade)  
**Updated:** 2026-06-30

---

## What changed

| Before | After |
|--------|-------|
| Public repo | **Private** repo (`clark-cmyk/Whinfell_BUILD_Cousins`) |
| Public Pages — anyone with URL | **Private Pages** — GitHub login + repo read access only |
| `latest.json` world-readable | Same URL gated behind GitHub auth |

**Why Pages is offline right now:** GitHub Free does not support Pages on private repositories. The API returns:

> `Your current plan does not support GitHub Pages for this repository.`

Upgrade to **GitHub Pro** (~$4/month personal) to re-enable Pages with private visibility.

---

## Clark checklist (one-time)

### Step 1 — Upgrade to GitHub Pro

1. Open https://github.com/settings/billing/plans
2. Upgrade personal account to **GitHub Pro**
3. Confirm billing is active

### Step 2 — Re-enable private Pages

1. Repo → **Settings** → **Pages**
2. **Build and deployment** → Source: **GitHub Actions** (workflow: `Desk preview (GitHub Pages)`)
3. **GitHub Pages visibility** → **Private** (only people with repo access)
4. Save

### Step 3 — Trigger a deploy

```bash
cd ~/Desktop/Whinfell_BUILD_Cousins
bash scripts/publish_desk_preview.sh
```

Or: GitHub → **Actions** → **Desk preview (GitHub Pages)** → **Run workflow**

### Step 4 — Note the private Pages URL

After first successful deploy, Settings → Pages shows **Visit site**.  
Private sites may use a distinct Pages URL — **copy the URL from Settings**, not an old bookmark.

Legacy public URL (may 404 until re-deployed as private):

`https://clark-cmyk.github.io/Whinfell_BUILD_Cousins/`

### Step 5 — Invite desk reviewers (by email)

Each person needs a **GitHub account** (or must create one when they accept).  
**Read** access is sufficient for private Pages.

| Name | Email to invite |
|------|-----------------|
| Wes | `wes@whinfellcap.com` |
| William | `william@whinfellcap.com` |

**GitHub UI (email invite — API cannot do this on personal repos):**

1. Open: https://github.com/clark-cmyk/Whinfell_BUILD_Cousins/settings/access  
   Or run: `bash scripts/invite_desk_reviewers.sh`
2. Click **Add people**
3. Paste **`wes@whinfellcap.com`** → **Add wes@whinfellcap.com to this repository**
4. Repeat for **`william@whinfellcap.com`**
5. Role: **Read** (default for outside collaborators is fine)

**Terminal (only if you have their GitHub usernames, not emails):**

```bash
gh api repos/clark-cmyk/Whinfell_BUILD_Cousins/collaborators/GITHUB_USERNAME \
  -X PUT \
  -f permission=pull
```

**Check pending invites:**

```bash
gh api repos/clark-cmyk/Whinfell_BUILD_Cousins/invitations --jq '.[] | {email: .invitee.email, login: .invitee.login, permissions}'
```

Each invitee accepts the GitHub email, signs in, then opens the Pages URL.

---

## Reviewer instructions (send to Wes + William after invite)

1. Accept the GitHub collaborator invite (check `wes@whinfellcap.com` / `william@whinfellcap.com` inbox).
2. Create a GitHub account if prompted.
3. Sign in at https://github.com
4. Open the desk URL Clark sends (from repo **Settings → Pages**).
5. If prompted, authorize GitHub Pages access for the private site.
6. Hard-refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows).

**No clone, no terminal, no import step** — Transmission Control auto-hydrates from co-hosted `latest.json` when signed in.

---

## Clark daily publish (unchanged)

After morning chain:

```bash
bash scripts/publish_desk_preview.sh
```

GitHub Actions redeploys in ~1–2 minutes. Only collaborators see the update.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Pages 404 / not found | Confirm GitHub Pro active · Settings → Pages → GitHub Actions source · run workflow |
| Wes sees 404 | Confirm invite accepted · signed into GitHub · using URL from Settings → Pages |
| Wes sees raw HTML / code | Opened blob URL on GitHub — use **Pages URL** or header **Live desk ↗** · not `blob/main/.../Whinfell_Transmission_Control.html` |
| **404 — There isn't a GitHub Pages site here** | Pages was **disabled** — enable once: Settings → Pages → **GitHub Actions** · or `gh api -X POST repos/clark-cmyk/Whinfell_BUILD_Cousins/pages -f build_type=workflow` · then `gh workflow run desk-preview-pages.yml --ref main` |
| `publish_desk_preview` deploy 404 | Same as above — `deploy-pages` fails until Pages is enabled on the repo |
| `latest.json` still public | Repo must stay private · Pages visibility must be **Private** |
| Want to revert to public | `gh repo edit clark-cmyk/Whinfell_BUILD_Cousins --visibility public --accept-visibility-change-consequences` then set Pages visibility Public |

---

## Security notes

- Private Pages is **real** access control (GitHub auth + collaborator list).
- Do not commit secrets to the repo — hydration JSON is desk metrics, not credentials.
- Revoke access: remove collaborator in Settings → Collaborators.

---

*Option 1 locked: private repo + private Pages + invited reviewers.*