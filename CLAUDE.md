# CLAUDE.md — Omni-TMDV

OMNI's TMDV operations dashboard (Vinh · Long An: leasing, land bank, KSNB/QTRR), entity **OMNI**. Live: https://ttrng3.github.io/Omni-TMDV/

**If you are the scheduled routine:** follow the file your prompt names, `README.md`, the runbook. It outranks this file. This file adds no step to a run.

## Commands
- Validate panels, history and cross-references (README "Publishing a refresh", step 3; must pass): `python3 tools/validate-panels.py`
- Build the Cowork preview page: `python3 tools/build-fragment.py` (writes `build/artifact.html`). When the routine refreshes the preview is set by its runbook, not here. Never send `index.html` itself to the preview; Pages does serve it.
- Compare two `data/` trees: `python3 tools/reconcile.py <dir-a> <dir-b>` (exit 0 = same)
- Freshness check, as the daily Action runs it: `python3 .github/scripts/freshness.py`

## Layout
- `index.html` is a renderer holding no data. A refresh writes `data/`, never the stylesheet.
- Data: `data/index.json` (manifest, `generatedUtc`), `data/panels/{exec,ops,ctrl}.json` (tab content), `data/history.json` (append-only trend), `data/.last-check` (heartbeat, not published).
- `.pages-allow` lists what Pages publishes; `.github/workflows/pages.yml` deploys only that. Every tracked file under a watched area needs a `.pages-allow` line (published, or `!` for known but not published); a new kind of file needs Ty's say-so and that line in its own PR first.
- `validate.yml` and `freshness-check.yml` open issues when they fail; `validate.yml` is deliberately not a required check (README "Guards on `main`").
- `REVIEW.md` holds the reviewer's rules.

## Rules
- Changes reach `main` through a PR and Ty's ship. The only direct writes are the ones a routine's prompt and runbook allow.
- The README wins over this file and any memory note. There is no second copy of the runbook; do not make one.
- The tab contract is the README's "What belongs on each tab": `exec` keeps three KPI cards and adds no section.
- Public on purpose (Ty, 2026-09-22, README "Confidentiality"). Do not widen what is published and do not re-litigate the ruling.
- Never write a Cowork preview URL or artifact id, a person's details or a secret into this public repo.
- Entity separation: this is OMNI. Never bring in another company's data, names or numbers.

## Known mistakes
- Every refresh added to `exec` and nothing left, until it was taller than both detail tabs (2026-09-22).
- One stray `</div>` in hand-written panel HTML closed the decisions grid early; the browser reparented the rest silently and it shipped (2026-09-22).
- Trust tags are `.pv.pv` on purpose: `.kpi .v` outranks a bare `.pv`, and a small tag once rendered as a headline (2026-09-22).
- The trend was lost once when each run deleted the last page; `data/history.json` has only grown since (2026-09-22).
- A section added or moved without updating the panel, `EXPECTED` in the validator and every "mục X" reference broke the cross-references (2026-09-22).
- A "còn N ngày" typed as a constant went stale; these are computed from the run date (2026-09-22).
- Revenue here is budget rate × NLA, a ceiling, not cash; the cash-gap KPI card shows "?" until accounting supplies collected figures (2026-09-22).
- The `Database Khách thuê` files are lead logs, not tenant ledgers, and have stale July twins in another folder; a filename match picked the wrong one (2026-09-22).
- The preview once held CSS fixes the repo lacked; a fragment rebuild from the repo would have reverted them (2026-09-23).
- "No artifact link" was read as "no artifact" and the preview was skipped or deleted. The preview must exist; only its URL stays out of sight (2026-09-23, 2026-09-26, 2026-09-27).
- A ToolSearch miss was read as a missing Artifact tool; attached tools never show there, and only an error from the tool itself means it is unavailable (2026-09-27).
