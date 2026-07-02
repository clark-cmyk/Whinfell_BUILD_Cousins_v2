# Whinfell BUILD Cousins

Transmission Control desk, data pipeline, and operator documentation.

## Open the desk (Wes / reviewers)

**Do not** open `Whinfell_Transmission_Control.html` via GitHub’s file browser — that shows raw HTML source.

| Use this | URL |
|----------|-----|
| **Live desk (recommended)** | [https://clark-cmyk.github.io/Whinfell_BUILD_Cousins/](https://clark-cmyk.github.io/Whinfell_BUILD_Cousins/) |
| **BasisWatch (standalone)** | [Whinfell_BasisWatch.html](https://clark-cmyk.github.io/Whinfell_BUILD_Cousins/Whinfell_BasisWatch.html) |
| Hydration bundle (auto-loaded on Pages) | [latest.json](https://clark-cmyk.github.io/Whinfell_BUILD_Cousins/data/hydration/latest.json) |

1. Accept the GitHub collaborator invite (read access is enough).
2. Sign in at [github.com](https://github.com).
3. Open the **Live desk** URL above.
4. Hard-refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows).

Private repo: GitHub Pages requires **GitHub Pro** and **Private** visibility. Setup: `08_Deliverables/Desk_Preview_Private_Access_Setup.md`.

## Clark — local + publish

```bash
# Local console
open 08_Deliverables/Whinfell_Transmission_Control.html

# Morning chain + publish to Pages
bash scripts/publish_desk_preview.sh
```

Full manual: `08_Deliverables/Whinfell_Desk_User_Manual_v1.0.md`

## Repo hygiene

```bash
bash scripts/archive_repo_duplicates.sh
```

Moves macOS `" 2"` duplicates and `.crdownload` files into `Archive/repo_cleanup_*`.