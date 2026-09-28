# Spec: readme-one-preview

**Intent:** accepted 2026-09-28 (revised) · **Status:** approved (a README-only change Ty specified; he approves by shipping)

## Requirements
1. `README.md` "One surface, on purpose" becomes "One address, one preview", stating the 26/09 rule (intent, Outcome 1).
2. It says the 23/09 "no artifact" rule is replaced, and that the routine refreshes the preview as its last step (STEP 9) (Outcome 2).
3. It says what `tools/build-fragment.py` is for (Outcome 3).

## Design
Replace README lines 310–321 with one section in Omni-Audit's terms (`docs/audit-refresh.md` "One address, one preview"), adapted to TMDV's facts: the flow line with the preview as the last hop, the rule, the history of the two deletions, the 27/09 skip this section caused, and `build-fragment.py`. No other section changes.

## Conflicts
| Rule (by name) | Touches | Resolution |
|---|---|---|
| Artifact mirror contract: never write the preview URL | the section names the preview | by title (*TMDV Điều hành*) only, never a URL or id; grep-checked |
| Never quote sensitive values in a public repo | none | n/a |

Policy loaded: artifact mirror contract (memory), Omni-Audit's model section, TMDV README.

## Promise
- `grep -n "One address, one preview" README.md` returns 1 line, and `grep -c "Do not recreate one" README.md` returns 0.
- `grep -ciE "claude\.ai/(code/)?artifact/" README.md work/` returns 0 (no preview link or id anywhere in the repo).
- `README.md` returns 404 on Pages (the allowlist keeps it unpublished).
- Next run (Sun 4 Oct): the routine's report doesn't say STEP 9 was skipped because of the README.

## Out of scope
The missing Artifact tool in the routine session (its own intent).
