# Intent: TMDV's README says "one address, one preview", and says honestly that the preview isn't refreshed yet

**Status:** accepted 2026-09-28
**Source:** chat, 2026-09-28 (Ty: "rewrite TMDV's README to 'one address, one preview', like Omni-Audit. The 26/09 rule replaces 23/09.")

**Problem.** `README.md` "One surface, on purpose" (lines 310–321) still carries the 23/09 rule: "there is no claude.ai artifact copy … Do not recreate one." Ty's 26/09 ruling (the artifact mirror contract) replaced it: every Pages pipeline has exactly one Cowork preview, it must exist, and its URL is never written anywhere. The TMDV preview does exist (titled *TMDV Điều hành*). A session reading this README today would conclude it should be deleted, which is the exact mistake made twice before (23/09, 26/09).

A second fact changes what the README can honestly say. **Nothing refreshes the TMDV preview.** The README says nothing in the refresh calls `tools/build-fragment.py`. The pipeline-wiring collector marks the preview "behind": its snapshot dates from 22/09, the repo's data from 27/09. Omni-Audit's wording ("refreshed as the last step of a publish") would be false here.

**Outcome.**
- The section is renamed "One address, one preview" and states the 26/09 rule in Omni-Audit's terms. The Pages URL is the only link. The preview exists, must never be deleted, and its URL is never written in this repo, a Drive doc or a run report.
- It states plainly that the refresh step is **not yet wired** for TMDV, so the preview can lag the page, and it points to the fix as its own change.
- The `build-fragment.py` line says what it's for: deriving the preview's fragment.

**Who and what is affected.** `README.md` only, one section. No code, no routine, no Pages change. `README.md` isn't served now that the allowlist is live.

**Constraints.** No preview URL or id in the repo (public), and no by-value personal data. The PR goes to Ty to ship.

**Decision (Ty, 2026-09-28).** Yes: the TMDV routine gets the mirror step, as its own intent (`work/260928-tmdv-mirror-step/`). This README states the gap until that lands.

**Open questions.** None.
