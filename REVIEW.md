# REVIEW.md

What the reviewer agent (`agents/reviewer.md` in claude-config) checks on every PR to this repo. The three passes run in order, each in full. The last section holds this repo's own rules.

This file is never served: it is not in `.pages-allow`.

## Severity
- **Critical:** it will break something live or publish something it must not. A secret or token, personal data by value in a public repo, a newly served path that shouldn't be, a broken deploy, data loss, a gate bypass.
- **High:** wrong behaviour that will show up. A bug on a path that runs, a broken reference, a diff that does something other than what the PR says, a house rule broken in a way Ty would have to undo.
- **Medium:** it's wrong but contained. An edge case that isn't hit yet, a doc that disagrees with the code, a missing test for a changed behaviour.
- **Low:** clarity, naming, a stale comment.

When unsure between two levels, pick the higher one and say why.

## Pass 1: Bugs
- [ ] Logic: off-by-one, inverted condition, wrong variable, an unreachable branch, loop bounds.
- [ ] Edge cases: empty input, a missing file, a first run, a name with spaces or accents, a timezone (Hanoi is UTC+7; cron is UTC).
- [ ] References resolve: every path, heading anchor, script flag, workflow job name and file named in the diff exists in `files/` or in the base.
- [ ] Shell: quoting, `set -e` interactions, `$?` after a pipe, BSD vs GNU flags (the Mac runs BSD tools).
- [ ] Syntax: YAML, JSON, Python (3.9 on the Mac: no `match`, no `X | Y` types), HTML.
- [ ] The diff does what the PR description says, and nothing it doesn't say.

## Pass 2: Security
- [ ] Secrets by pattern: `ghp_`, `github_pat_`, `sk-`, `sk-ant-`, `AKIA`, `xox[bp]-`, private-key headers, `eyJ…` JWTs (a Supabase **service_role** JWT is always Critical), passwords in URLs, `?token=`/`?key=` in a link.
- [ ] Personal data **by value** in a public repo: a name with money, a phone number, an email address, an account number, an ID number. Referring to where the value lives is fine; the value itself isn't.
- [ ] Anything newly published: a path added to `.pages-allow`, or any new file in a repo still on legacy Pages.
- [ ] Workflow permissions widened (`permissions:`, `pull_request_target`, `secrets: inherit`), or a new third-party action not pinned to a sha.
- [ ] Test fixtures build fake secrets at run time; a token-shaped string typed into a file is a finding even if it's fake.

## Pass 3: House rules
- [ ] **Never by value:** a sensitive value is referenced, not quoted, in any file of a public repo, including `work/` docs.
- [ ] **Artifact mirror contract:** no Cowork preview URL and no artifact id in anything public or anything Ty is shown. (A registry row that records an id on the private Drive mount is the exception.)
- [ ] **Entity separation:** OMNI and ECOPM data, names and numbers never cross into each other's repo or page.
- [ ] **One change per `work/` folder:** the PR names its `work/<yymmdd>-<slug>/`; `intent.md` says accepted; `spec.md` says approved; the diff matches the spec's promise, with nothing extra.
- [ ] **`gate/` untouched** while it is frozen (until 2026-10-05).
- [ ] **One PR per merge command:** nothing in the diff merges or batches PRs (`gh pr merge` in a loop, the merge API).
- [ ] **Verify before you assert:** every number in a doc or page has a source named beside it or in its section.

## Repo-specific rules
Omni-TMDV.

- **The README is the routine's runbook.** It outranks the routine prompt, memory and Drive. A change to what the routine does (sources, schedule, files written, checks) must change the README in the same PR; a README that disagrees with the diff is High. Never add a second copy of the runbook anywhere.
- **The tab contract.** What each tab may hold is the README's "What belongs on each tab" section, read from the base branch's README together with its section-letter rules (A–L across `ops` and `ctrl`, section H included, even though that section's `ops` line lists A–G) (not copied here, so it can't go stale). A new section on `exec`, or a fourth KPI card, that the README doesn't list is High. A PR that changes that README section is itself the place to argue the change. KPI numbers live in the `exec` panel only, never copied into `index.json`.
- **Section letters.** A–L run across `ops` and `ctrl` as one sequence. Adding or moving a section changes the panel, `EXPECTED` in `tools/validate-panels.py`, and every prose "mục X" reference in the same PR; missing any of the three is High.
- **No stylesheet edits from a refresh.** A refresh (a commit the weekly routine makes) writes `data/` only. A PR that changes the routine itself may touch the README and `tools/`, as the runbook rule above requires. A change to any `<style>` block in `index.html` (the base sheet or `apple-layer`) needs its own PR and Ty's say-so; mixed into a data change it is High.
- **Hand-written HTML in panel JSON** must keep its tags balanced (`tools/validate-panels.py`). An unbalanced tag is High: the browser reparents what follows it without any error.
- **Public on purpose, ruled 2026-09-22 by Ty** (recorded in the README, "Confidentiality — ruled 2026-09-22 by Ty"; it covers the whole page as published). Don't widen what is published: a new path in `.pages-allow`, or a new kind of data in a panel, is High and needs Ty. Don't re-litigate the ruling either; a finding that says "this repo should be private" is out of scope.
- **Entity separation.** This is an OMNI repo. Any ECOPM data (a person's or a client's name, a number, or a file from the ECOPM side) is **Critical**. The entity label itself isn't.
- **`data/history.json` is append-only.** A diff that edits or deletes an existing row is High.
- **Elapsed-time numbers.** Every "còn N ngày" / "N ngày" on any tab (the CT1 deadline countdown on `exec`, the decision sheet, the cost-of-delay figures) is recomputed from the run date in code, never typed as a constant (README, "Publishing a refresh" step 4). A hard-coded countdown is High: it's wrong on the live page the day after the refresh that wrote it.
