# TMDV Điều hành

Live dashboard: **https://ttrng3.github.io/Omni-TMDV/**

Operations view of the TMDV ecosystem across Eco Central Park (Vinh) and
Eco Retreat (Long An) — commercial leasing, HTXH land bank, community
development, and the KSNB/QTRR control spine. Three tabs: executive summary,
per-unit detail, timeline and control health.

**This file is the runbook.** The weekly routine is told to read it first and
that it outranks the routine's own prompt, stored memory, and any Drive
document. There is deliberately no second copy — a runbook that exists twice
drifts, and the stale copy is the one that gets followed.

## How this repo is the source of truth

```
Google Drive — shared drive "BAN ĐẦU TƯ, TMDV, PTCĐ" (leasing trackers)
   + Outlook, read-only (escalation threads)
        ▼
weekly routine ──writes──▶ data/index.json + data/panels/<tab>.json
                                   │
                                   ▼
                            GitHub Pages
                            (index.html)
```

`index.html` is a **renderer with no data in it** (~18 KB, was ~77 KB). It
fetches `data/` at load — relative first, falling back to the published
`https://ttrng3.github.io/Omni-TMDV/data/` — so the same file works as a Pages
site and from a local copy.

## Sources and surfaces

Everything the job reads and everything it writes, in one place. If a value
here disagrees with a prompt or a Drive note, this table wins.

| What | Where | Access |
| --- | --- | --- |
| Vinh leasing tracker | Shared drive `BAN ĐẦU TƯ, TMDV, PTCĐ` → `1. Thông tin chung / 8. Báo cáo tuần` → `ECP_CT1_Theo dõi chào thuê mặt bằng`, `ECP_CT1_Tiến độ khách`, `Database Khách thuê Vinh.xlsx` | Google Drive connector, read-only |
| Long An leasing tracker | same folder → `ER_Bazaar_Theo dõi chào thuê mặt bằng.xlsx`, `Database Khách thuê LA` | Google Drive connector, read-only |
| Land bank (Trụ cột 2) | same shared drive → `2. ĐẦU TƯ HTXH`, `Theo dõi tiến độ đối tác.xlsx`, `TMDV - Đầu Tư Task list` | Google Drive connector, read-only |
| Escalation threads | OMNI mailbox via Microsoft 365, senders `@dbgroup.com.vn` (thanhlt@, daola@, hientt@) | M365 connector, **read-only — never send or modify** |
| Weekly routine | `trig_01Ff3aQaqt1w2YEpUvo7LmXe` — "TMDV weekly refresh (Drive trackers → GitHub data)", cron `0 11 * * 0` (Sun 18:00 Asia/Saigon), cloud-only, model Opus | claude.ai/code/routines |
| Pages surface | https://ttrng3.github.io/Omni-TMDV/ | public |
| Freshness guard | `.github/workflows/freshness-check.yml`, daily 11:00 Asia/Saigon | opens an issue on this repo |

The three DB Group mailboxes are a different tenant and cannot be scanned
directly by the automation identity. Escalations are picked up from the OMNI
mailbox, which is CC'd on the TMDV threads. Say so on the page — do not let a
narrower scan read as a full one.

### Confidentiality — ruled 2026-09-22 by Ty

The page is marked `Mật: restricted` and carries tenant names, rents, OTL terms
and live disputes, and it is served from a **public** repo. That is a decision,
not an oversight: Ty ruled on 2026-09-22 to keep it public, on a low-traffic URL
with `robots.txt` disallowing crawlers, because the audience needs it without a
login. `robots.txt` discourages indexing; it does not make the URL private, and
a free-plan account cannot run Pages from a private repo. Do not quietly widen
what is published here, and do not re-litigate the ruling on a refresh — if the
sensitivity changes, that is a fresh decision for Ty.

## Layout

| Path | What it is |
| --- | --- |
| `index.html` | Renderer only. Header shell, tabs, tab-switching script. No data. |
| `data/index.json` | `generatedUtc`, `asof`, lead, source-freshness meta, tab labels, panel manifest. |
| `data/panels/<tab>.json` | That tab's content. `exec`, `ops`, `ctrl`. |
| `data/history.json` | The trend. One append-only row per refresh, every value trust-tagged, every row citing its source. |
| `data/.last-check` | Heartbeat. Proves the job ran even when nothing changed. |
| `tools/validate-panels.py` | Tag-balance and section-letter check. **Run before publishing.** |
| `.github/workflows/freshness-check.yml` | Opens an issue if the job stops, or if the trackers go quiet. |
| `.github/workflows/validate.yml` | Runs the two checks above on every push to `data/` or `index.html`, and opens an issue if what was published does not validate. |

The KPI cards live inside the `exec` panel. They are deliberately **not** also
copied into `index.json` — two copies of the same number is how they drift.

## What belongs on each tab

Revised 2026-09-22. The executive tab had grown to 4,344 px — taller than either
detail tab — because every refresh added to it and nothing ever left. It was cut
to 2,009 px; with the decision sheet and collapsed lenses it is 2,643 px
(ops 6,528 · ctrl 3,833) and is still the shortest. Keep it that way.

**`exec` — what gets decided in a meeting. Nothing else.**
verdict · three KPI cards · the trust-tag key · **the five-period trend strip** ·
the next contractual deadline · **the three instrument-trust findings** ·
§01 the **decision sheet** · three **collapsed role lenses** (CFO · Chủ tịch ·
TGĐ) · a collapsed Δ-since-last-issue block.
Three KPI cards, not six: a fourth costs more than it tells, and every number
dropped from here still exists on another tab.

Restructured 2026-09-22 at Ty's request, reading the page as CFO, Chairman and
CEO in turn:

- **KPI cards serve the three readers.** Card 1 is labelled a *ceiling*, not
  cash. Card 3 is the cash gap (`? tỷ — tiền thuê thực thu, chưa đo được`) and
  stays a red "?" until Kế toán supplies invoiced/collected by unit — do not
  fill it from budget rate. WinMart (76,6% of Vinh "đang thu") carries a 4-year
  rent-free OTL; that is why the ceiling cannot be read as cash.
- **§01 is a table, one row per decision**: the ask · money · cost of waiting ·
  options A/B · the page's recommendation (labelled as such, not an approved
  policy) · deadline · who decides. Recompute every "N ngày" from the run date.
- **Role lenses** (collapsed, so the tab stays the shortest): CFO = ceiling →
  contracted-after-free-rent → invoiced → collected bridge plus money-out
  ledger; Chủ tịch = the direction question (revenue line vs. density tool),
  HTXH obligation, and a decision-latency table (days each item has waited);
  TGĐ = team KPI (tracker tab "KPI") vs committed m², pro-rated by day of year,
  plus the team's own missed dates. Per-person KPI is not measurable until the
  tracker records who owns each unit — say so, do not guess.

The trend strip and the instrument-trust block were added 2026-09-22 and are
part of the contract, not decoration. A snapshot cannot answer *"is this getting
better or worse?"*, and that is the question that decides whether the board
intervenes. The instrument-trust block is **not** the risk map: the risk map is
about the business, that block is about whether these numbers can be relied on
at all. Keep them distinct.

**`ops` — the pipeline and the assets.**
A three pillars · B revenue map by value · C unit funnel · D Vinh ·
E the disputed Vinh "khai trương" block · F Long An · G land bank.

**`ctrl` — history, control health, and how much to trust the numbers.**
I operating timeline · J KSNB/QTRR health · K trust layer · L risk map.

The section letters run **A–L across `ops` and `ctrl` as one sequence**; `exec`
has its own numbered series. `tools/validate-panels.py` enforces both the
sequence and, since 2026-09-22, that every prose reference (`"mục E"`) names a
section that exists.

If you add a section you must edit three things in the same change: the panel,
`EXPECTED` in the validator, and any prose pointing at a letter that moved.
Section H was inserted on 2026-09-22 and shifted `ctrl` from H–K to I–L; the
same day's earlier renumber had silently left three `"(mục C)"` references
pointing at the funnel instead of the disputed-openings block, which is why the
reference check now exists.

## The trend series

`data/history.json` is **append-only**. Add one row per refresh; never rewrite
or delete a past row. `validate-panels.py` enforces this against git HEAD and
will fail the build if the series shrinks or an existing row changes.

This exists because the trend was thrown away once already. Before the
2026-09-22 split every period lived inside a 300 KB HTML file that the next run
deleted, so only 14/09 and 22/09 survived in git — the sibling repo
`Omni-sitecheck` kept `data/weeks/` per period, this one kept nothing. Rows
31/08 through 14/09 were reconstructed from the run records under
`93 Knowledge Base/Claude outputs/TMDV/`, and each row cites the file it came
from in `src`. There is no third copy to reconstruct from.

**Every value carries a trust tag**, same vocabulary as the page (`v` = ✓ĐC,
`l` = ~, `a` = GĐ). When a value's tag changes between periods, the delta column
prints *"đổi cơ sở"* instead of subtracting — because the number moved for a
reason the business did not produce. 6,94 → 7,69 on the committed block is
exactly that: 6,94 was carried untouched from 21/08, 22/09 was recomputed per
unit, and only +0,47 was real. Do not let a basis change render as growth.

**It is a table, not a sparkline, on purpose.** Across the five recovered
periods four of the five metrics vary by under 0.2% — they are flat lines — and
the only one that moves does so because of the basis change above. Sparklines
here would draw four dead lines and one fake step. Revisit if real variance ever
appears; until then a table with an explicit delta is the honest form.

## Publishing a refresh

1. Write `data/.last-check` first, every run, even a quiet one.
2. Write only the panels whose numbers actually moved, plus `data/index.json`.
   Append one row to `data/history.json` — every run, including a quiet one. A
   quiet period is data: it is how the 22-day plateau became visible.
3. `python3 tools/validate-panels.py` — it must pass. An unbalanced tag does not
   fail loudly; the browser silently reparents what follows it.
4. Recompute every interval ("còn N ngày") from the run date, in code. The
   30/09 CT1 deadline on the exec tab is a live countdown, not a constant.

## Guards on `main`

Two different failure questions, two different guards — a dashboard can be
stale, or it can be fresh and wrong, and neither guard sees the other's case.

| Guard | Answers | Reacts by |
| --- | --- | --- |
| `freshness-check.yml` (daily) | Did the job run? Are the trackers moving? | Opening a `stale-data` issue |
| `validate.yml` (every push) | Is what we published actually renderable? | Opening a `broken-data` issue |

`validate.yml` is deliberately **not** a required status check. The weekly
routine commits straight to `main` through the GitHub API, and a required check
would block it — trading a visibly broken page for a silently stale one, which
is the worse failure and the one this repo already had. It is loud, not
preventive.

**Branch protection (set 2026-09-22):** force-pushes and branch deletion are
blocked on `main`, for admins too. Ordinary pushes are untouched, so the
routine works exactly as before. The reason the rule includes admins: the
routine pushes with Ty's own credential, so an admin exemption would exempt the
one identity capable of overwriting the data, and the freshness check cannot
see an overwrite — the timestamps would look perfect.

## Why it changed

The weekly routine used to rebuild the whole page, drop a standalone HTML copy
on Drive, and have a second routine mirror that file to GitHub. Every hop
carried the whole document, and a dated `archive/status_*.html` series
accumulated beside it.

Now the routine writes data and the page renders it. A refresh rewrites only the
panel whose numbers actually moved (~8–31 KB) instead of the whole page.

**Retired 2026-09-22 — do not resurrect, and do not read as current:** the
`TMDV GitHub mirror` routine, the Drive handoff at
`93 Knowledge Base/Claude outputs/TMDV/index.html`, the dated
`archive/status_*.html` series, and `20260909_TMDV_Update-Playbook_v1.md` /
`20260909_TMDV_OptionB_runbook_v1.md` (both moved to `_archive/`). A refresh
session that finds one of these and this file in conflict is not looking at
kernel drift — this file is simply newer. Do not halt over it.

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

## What the source trackers actually contain

Audited 2026-09-22 against the live files, so nobody re-derives it or assumes
more than is there.

| Field | `ER_Bazaar` (Long An) | `ECP_CT1_Tiến độ khách` (Vinh) |
| --- | --- | --- |
| Deposit date (`Ngày khách cọc`) | populated | **column exists, 0/63 filled** |
| Agreed rent (`Tiền thuê thực tế` / `Giá thuê chốt`) | populated | **column exists, 0/63 filled** |
| Expected opening (`Dự kiến Khai Trương`) | not present | **8/63 filled** |
| Budget rate | populated | populated (62/63) |
| Free-rent schedule · invoiced · collected | **absent** | **absent** |

Consequences, and they bound what this dashboard can honestly claim:

- **Aging works on Long An, not on Vinh.** Section H measures Vinh by missed
  opening dates instead, which is why only 33% of Vinh's committed block by
  money is measurable at all.
- **No cash bridge is possible from Drive.** Free-rent terms live in email and
  tờ trình; invoiced and collected live in accounting. Anything built from these
  files is *contracted revenue timing*, never cash. Label it that way.
- **`Database Khách thuê Vinh/LA` are lead logs, not contract databases** — 58
  prospects with owner and status, no money in them. Do not read them as a
  tenant ledger.
- Both `Database` files have **stale July twins in a different folder**. Match on
  the parent folder id, never on the filename.

## Data caveats

- Revenue is **budget rate × NLA** — a theoretical ceiling, not cash flow.
- The Vinh tracker has over-summed NLA before (~605 m²). Recompute per unit,
  never from a total cell.
- FX 27.000 đ/USD is an assumption carried from the Vinh file; keep it labelled.
- Trust tags on decision-driving numbers: `✓ĐC` recomputed this run · `~`
  current source, not independently recomputed · `GĐ` assumption/unreconciled.
- A source that could not be read is a **red, not a green**. Mark the panel
  `dữ liệu chưa cập nhật — nguồn không truy cập được dd/mm`, keep the last
  verified values, and say so in the run report.

## Visual standard

Since 2026-09-23 the renderer follows the **Ty Artifact Standard** — the house
Apple-HIG treatment that governs every page Ty builds, not just this one. The skill
`ty-artifact-standard` holds the full rules, and is the only place they live.
It replaced the warm-paper / Playfair treatment that ran from 2026-09-08.

What binds here, in short:

- Page ground `#F2F2F7`, cards `#FFFFFF` at 12 px radius, hairlines
  `1px solid #E5E5EA`. **No drop shadows.**
- System font stack only. **Do not add a webfont link back** — it blocked first
  paint and bought nothing a dashboard needs.
- Ink in three tiers: `#1C1C1E` primary, `#3C3C43` body, `#8E8E93` muted.
  Hierarchy comes from grading one ink, never from a second font colour.
- Semantic accents: blue `#007AFF` active/info, green `#34C759` done, amber
  `#FF9500` outstanding, red `#FF3B30` critical. Pills use a darkened ink of the
  same hue on a tint, because the raw hexes fail contrast at 12 px.
- **Every pill carries a dot and a word.** Amber and green sit 7.1 ΔE apart
  under protanopia — colour alone does not separate them. Do not strip the dot.
- Tables: no vertical rules, no filled header, one hairline per row,
  `font-variant-numeric: tabular-nums` on every figure.
- The `@media print` block and the `beforeprint` hook that expands every
  `<details>` are load-bearing. This page gets photocopied; amber on white
  washes out, and a collapsed lens on paper is a lens nobody reads.

A refresh writes `data/`, never the stylesheet. If a refresh finds itself
editing CSS, something has gone wrong — stop and ask.

## Renderer gotcha

The trust tags are written `class="pv v"`, `"pv l"`, `"pv a"`. Inside a KPI card
the selectors `.kpi .v` and `.kpi .l` outrank a bare `.pv`, so the tag rules are
written **`.pv.pv`** to match on specificity and win on order. Do not simplify
them back to `.pv`: the symptom is a 9.5 px tag rendering as a 30 px headline,
which is how it shipped from 2026-09-08 to 2026-09-22.

## Artifact mirror

The chain is **repo-first**, the same shape KSNB has always used:

    schedule → cloud routine → source → GitHub → Pages → artifact mirrored after

**The repo is the source of truth and Pages is the live surface.** The artifact
at https://claude.ai/artifact/CsyKTf8ToysYHRSPo2macg is a **mirror**, published *after* the repo
is correct, and it is never authoritative. If the two ever disagree, the repo
wins and the artifact is what gets corrected.

How a refresh mirrors it, in this order:

1. Write and verify the repo first. Do not touch the artifact until `main` has
   moved and you have read the commit back.
2. Publish the changed data paths — data/index.json, data/history.json and the changed data/panels/<tab>.json — with the artifact's `url` set.
   Files you omit are kept, so a refresh is a small write.
3. Republish the page only when the **renderer** changed, and then publish the
   `tools/build-fragment.py` output, never `index.html` itself. The artifact
   service wraps what you give it, so a complete document nests inside another,
   the inner `<head>` is discarded, and the page renders **blank with no
   console error**. To tell that apart from the other blank cause, read the
   artifact's `index.html` back and count `<html>` tags: two means it nested,
   one means the markup is fine and it is the same-call publish problem.
4. **A failed mirror must never make you undo or retry the repo write.** Report
   it and stop; the site is already correct.

`tools/reconcile.py` diffs this repo's `data/` against the artifact's copy and
says which side is newer.

**Why the ordering is stated this bluntly.** On 2026-09-23 the TMDV artifact was
found *ahead* of its repo, carrying four fixes that had never been committed,
and the ECOPM artifact was found a whole renderer generation *behind*. Neither
was caught by the freshness guards, because both read data timestamps and the
drift was in the page. Repo-first is what keeps that from recurring.
