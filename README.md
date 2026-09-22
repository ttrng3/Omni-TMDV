# TMDV Điều hành

Live dashboard: **https://ttrng3.github.io/Omni-TMDV/**

Operations view of the TMDV ecosystem across Eco Central Park (Vinh) and
Eco Retreat (Long An) — commercial leasing, HTXH land bank, community
development, and the KSNB/QTRR control spine. Three tabs: executive summary,
per-unit detail, timeline and control health.

## How this repo is the source of truth

```
Google Drive — shared drive "BAN ĐẦU TƯ, TMDV, PTCĐ" (leasing trackers)
   + Outlook, read-only (escalation threads)
        ▼
weekly routine ──writes──▶ data/index.json + data/panels/<tab>.json
                                   │
                    ┌──────────────┴──────────────┐
                    ▼                             ▼
             GitHub Pages                 claude.ai artifact
             (index.html)                 (its own copy of data/)
```

`index.html` is a **renderer with no data in it** (~17 KB, was ~77 KB). It
fetches `data/` at load — relative first, falling back to the published
`https://ttrng3.github.io/Omni-TMDV/data/` — so the same file works as a Pages
site, as an artifact, and from a local copy.

## Why it changed

The weekly routine used to rebuild the whole page, republish the artifact, drop
a standalone HTML copy on Drive, and have a second routine mirror that file to
GitHub. The published page was downstream of the artifact, every hop carried the
whole document, and a dated `archive/status_*.html` series accumulated beside it.

Now the routine writes data and the page renders it. A refresh rewrites only the
panel whose numbers actually moved (~19–27 KB) instead of the whole page.

The split was verified by rendering the old page and the new one and hashing
each tab's text independently:

| tab | chars | hash | tables | rows |
| --- | --- | --- | --- | --- |
| exec | 9,897 | `537c37f` | 1 | 7 |
| ops | 13,347 | `299220d6` | 10 | 87 |
| ctrl | 12,167 | `9b582f7b` | 4 | 48 |

Identical on both. Tab switching re-tested after the panels became dynamic.

## Layout

| Path | What it is |
| --- | --- |
| `index.html` | Renderer only. Header shell, tabs, tab-switching script. No data. |
| `data/index.json` | `generatedUtc`, `asof`, lead, source-freshness meta, tab labels, panel manifest. |
| `data/panels/<tab>.json` | That tab's content. `exec`, `ops`, `ctrl`. |
| `data/.last-check` | Heartbeat. Proves the job ran even when nothing changed. |
| `.github/workflows/freshness-check.yml` | Opens an issue if the job stops, or if the trackers go quiet. |
| `tools/reconcile.py` | Diffs this repo's `data/` against the artifact's copy. Shared, shape-agnostic. |

The 7 KPI cards live inside the `exec` panel. They are deliberately **not** also
copied into `index.json` — two copies of the same number is how they drift.

## Why the heartbeat matters here

The 2026-09-20 run did not fail on logic. It failed in **one second** with
`rate_limit: rejected (five_hour)` — the org spend limit. It wrote nothing, said
nothing, and the mirror routine then dutifully copied the unchanged Drive
handoff to GitHub, so the page looked freshly published on 21/09 while its data
was still as of 14/09.

That is precisely the shape of failure this dashboard could not see before.
`data/.last-check` now records every run; the freshness check reads it
separately from `generatedUtc`, so "the job died" and "the trackers were quiet"
no longer look the same from outside.

## Data caveats

- Revenue is **budget rate × NLA** — a theoretical ceiling, not cash flow.
- The Vinh tracker has over-summed NLA before (~605 m²). Recompute per unit,
  never from a total cell.
- FX 27.000 đ/USD is an assumption carried from the Vinh file; keep it labelled.
- Trust tags on decision-driving numbers: `✓ĐC` recomputed this run · `~`
  current source, not independently recomputed · `GĐ` assumption/unreconciled.
