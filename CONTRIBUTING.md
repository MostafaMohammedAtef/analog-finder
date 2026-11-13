# Team rules

These rules exist so that nobody waits for anybody.

## 1. Own your files

| Member | Owns | Never edits |
| --- | --- | --- |
| 1 Terrain | `terrain/`, `out/terrain.json`, `merge.py` | anyone else's lane |
| 2 Sun + temp | `sun/`, `out/sun.json`, `out/temp.json` | anyone else's lane |
| 3 App | `web/` (except `web/results.json`, which merge.py writes) | anyone else's lane |
| 4 Story | `content/`, `docs/`, `README.md` | anyone else's lane |

Shared and frozen at H1: `constants.py`, `data/sites.json`, `CONTRACTS.md`. Changes need everyone's OK at a sync.

## 2. Branches

- One branch per lane: `terrain`, `sun`, `app`, `story`.
- Never push straight to `main`. Open a pull request; any teammate can approve; merge quickly (don't let PRs sit).
- Pull `main` into your branch after every sync: `git pull origin main`.
- Because everyone owns different files, merge conflicts should not happen. If one does, the file's owner resolves it.

## 3. Build against the contract, not against people

- Read [CONTRACTS.md](CONTRACTS.md) before writing any output.
- Run `python scripts/check_contracts.py` before every pull request. GitHub runs it on every PR too, and a red check means the app would break.
- Using an AI assistant? Point it at [CLAUDE.md](CLAUDE.md) first.
- If you need someone's output and it isn't ready, use the mock (`web/mock_results.json`) or `null`.
- Get **one site** working end to end before doing all 13.

## 4. Syncs (15 minutes, all four)

H1 contracts frozen, H6 check-in, H12 one site live in the app, H24 all data real and app online, H36 feature freeze, H46 submit. See [docs/timeline.md](docs/timeline.md).

At each sync, each person says: done / next / blocked. A blocker gets a fix or a fallback before the sync ends.

## 5. Data

- Never commit DEMs or raw downloads (`data/dem/`, `data/raw/` are in `.gitignore`). They are too large for GitHub.
- Do commit the small JSON outputs in `out/` and `web/results.json`.
- Never commit passwords, `.netrc`, or Earthdata tokens.

## 6. Commits

- Small commits with clear messages: `terrain: add Svalbard window`, `app: radar chart`.
- Pair work: credit your teammate with a trailer at the end of the message:
  `Co-authored-by: Name <their-github-email>`

## 7. Honesty

If a number looks too good, check it before showing it. Where a site fails, say so in `content/breaks.json`. The challenge rewards saying where the analogy breaks.
