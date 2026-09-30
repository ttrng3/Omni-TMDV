# Spec — Pages workflow template v2 (approved)

Status: approved by Ty 30/09. The full spec lives in claude-config at
`work/260929-pages-template-fixes/spec.md`, pinned to commit 0a63b43
(claude-config PR 9, 20/20 Linux tests in CI). This file records what it means here.

## Change
`.github/workflows/pages.yml` becomes the template at 0a63b43, minus the optional
workflow_run placeholder comment (this repo's data is pushed by a routine, which
does trigger push runs). `.pages-allow` changes only its header comment.

## Behaviour changes, all checked against this repo's allowlist
- a. Coverage reads every tracked file in a watched area, not the last diff.
- b. A `*` never matches a leading dot, on published and `!` lines alike. This repo lists `!data/.last-check` explicitly.
- c. A line containing `?` or `[` is a glob. This repo has none.
- d. Line trimming uses parameter expansion instead of xargs, so quotes are taken literally.
- e. `fetch-depth: 50` is gone; the whole-tree check needs no history.
- f. Symlinks and paths resolving outside the repo stop the deploy.
- g. Permissions: workflow `contents: read`; build `contents: read` + `pages: read`; deploy `pages: write` + `id-token: write`.

## Pass condition (after merge)
The push run shows `mode: live`, with configure-pages, upload and deploy green,
and the served files byte-identical to the pre-merge baseline. A failure reverts
this PR before any other repo moves.
