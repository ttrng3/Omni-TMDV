# Spec — Pages workflow template v2 (approved)

Status: approved by Ty 30/09. The full spec lives in claude-config at
`work/260929-pages-template-fixes/spec.md`, pinned to commit 3f62fe2 (0a63b43 plus the symlink fix, claude-config PR 10, and the glob-space fix, PR 11)
(claude-config PRs 9 and 10; 24/24 Linux tests in CI at 3f62fe2). This file records what it means here.

## Change
`.github/workflows/pages.yml` becomes the template at 3f62fe2, minus the optional
workflow_run placeholder comment (this repo's data is pushed by a routine, which
does trigger push runs). `.pages-allow` changes only its header comment.
README.md (the routine's runbook) gains a `pages.yml` row in "Guards on `main`",
with the rule it implies: a new file under `data/` needs its own `.pages-allow`
line, in its own PR, before the routine writes it; the guards intro mentions it.

## Behaviour changes, all checked against this repo's allowlist
- a. Coverage reads every tracked file in a watched area, not the last diff.
- b. A `*` never matches a leading dot, on published and `!` lines alike. This repo lists `!data/.last-check` explicitly.
- c. A line containing `?` or `[` is a glob. This repo has none.
- d. Line trimming uses parameter expansion instead of xargs, so quotes are taken literally.
- e. `fetch-depth: 50` is gone; the whole-tree check needs no history.
- f. A symlink anywhere in a listed path, a path resolving outside the repo, or a path not written plainly (`./x`, `a//b`) stops the deploy. This repo has none.
- g. Permissions: workflow `contents: read`; build `contents: read` + `pages: read`; deploy `pages: write` + `id-token: write`.

## Pass condition (after merge)
The push run shows `mode: live`, with configure-pages, upload and deploy green,
and the served files byte-identical to the pre-merge baseline. A failure reverts
this PR before any other repo moves.
