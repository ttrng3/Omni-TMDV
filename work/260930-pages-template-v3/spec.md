# Spec — re-copy the Pages template at 3f62fe2 (approved)

Status: approved by Ty 30/09 by shipping claude-config PR 11, whose spec orders this
re-copy. Pinned to claude-config 3f62fe2 (PRs 9, 10 and 11; 24/24 Linux tests in CI).

## Change
`.github/workflows/pages.yml` becomes the template at 3f62fe2 minus the optional
workflow_run placeholder comment. Nothing else changes.

## Behaviour changes
- A glob line containing a space is one pattern, never split on spaces. This repo's
  `.pages-allow` has no line with a space, so today's result is unchanged.
- Header comment line 2 says coverage checks every tracked file in a watched area.

## Pass condition (after merge)
The push run shows `mode: live` with configure-pages, upload and deploy green, and the
served files byte-identical to the baseline fetched before merge (a file a routine
changes in between is compared with its copy at the deployed commit).
